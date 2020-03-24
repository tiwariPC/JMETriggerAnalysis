#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <string>
#include <vector>
#include <map>
#include <algorithm>

class HLTPrinter : public edm::EDAnalyzer {
public:
  explicit HLTPrinter(const edm::ParameterSet&);
  ~HLTPrinter() override = default;
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  bool skipStreamByName(const std::string& streamName) const;
  bool skipPathMonitorElement(const std::string& pathName) const;
  bool skipModuleByEDMType(const std::string& moduleEDMType) const;
  bool skipModuleByType(const std::string& moduleType) const;

  std::string processName_;
  bool initFailed_;
  bool skipRun_;

  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  edm::EDGetTokenT<trigger::TriggerEvent> triggerSummaryTokenAOD_;
  edm::EDGetTokenT<trigger::TriggerEventWithRefs> triggerSummaryTokenRAW_;

  HLTConfigProvider hltConfigProvider_;
};

HLTPrinter::HLTPrinter(const edm::ParameterSet& iConfig)
    : processName_(""),
      initFailed_(false),
      skipRun_(false) {
  auto const triggerResultsInputTag(iConfig.getParameter<edm::InputTag>("triggerResults"));

  if (triggerResultsInputTag.process().empty()) {
    edm::LogError("Input") << "process not specified in HLT TriggerResults InputTag \""
                           << triggerResultsInputTag.encode() << "\" -> plugin will not produce DQM outputs";
    initFailed_ = true;
    return;
  } else {
    processName_ = triggerResultsInputTag.process();

    triggerResultsToken_ = consumes<edm::TriggerResults>(triggerResultsInputTag);

    auto triggerSummaryAODInputTag(iConfig.getParameter<edm::InputTag>("triggerSummaryAOD"));
    if (triggerSummaryAODInputTag.process().empty()) {
      triggerSummaryAODInputTag =
          edm::InputTag(triggerSummaryAODInputTag.label(), triggerSummaryAODInputTag.instance(), processName_);
    } else if (triggerSummaryAODInputTag.process() != processName_) {
      edm::LogWarning("Input") << "edm::TriggerResults process name '" << processName_
                               << "' differs from trigger::TriggerEvent process name '"
                               << triggerSummaryAODInputTag.process() << "' -> plugin will not produce DQM outputs";
      initFailed_ = true;
      return;
    }
    triggerSummaryTokenAOD_ = consumes<trigger::TriggerEvent>(triggerSummaryAODInputTag);

    auto triggerSummaryRAWInputTag(iConfig.getParameter<edm::InputTag>("triggerSummaryRAW"));
    if (triggerSummaryRAWInputTag.process().empty()) {
      triggerSummaryRAWInputTag =
          edm::InputTag(triggerSummaryRAWInputTag.label(), triggerSummaryRAWInputTag.instance(), processName_);
    } else if (triggerSummaryRAWInputTag.process() != processName_) {
      edm::LogWarning("Input") << "edm::TriggerResults process name '" << processName_
                               << "' differs from trigger::TriggerEventWithRefs process name '"
                               << triggerSummaryRAWInputTag.process() << "' -> plugin will not produce DQM outputs";
      initFailed_ = true;
      return;
    }
    triggerSummaryTokenRAW_ = mayConsume<trigger::TriggerEventWithRefs>(triggerSummaryRAWInputTag);
  }
}

void HLTPrinter::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
  if (initFailed_) {
    return;
  }

  LogTrace("")
      << "[HLTPrinter] "
      << "----------------------------------------------------------------------------------------------------";
  LogTrace("") << "[HLTPrinter::dqmBeginRun] Run = " << iRun.id();

  // reset data members holding information from the previous run
  skipRun_ = false;

  bool hltChanged(true);
  if (hltConfigProvider_.init(iRun, iSetup, processName_, hltChanged)) {
    LogTrace("") << "[HLTPrinter::dqmBeginRun] HLTConfigProvider initialized [processName() = "
                 << hltConfigProvider_.processName() << ", tableName() = " << hltConfigProvider_.tableName()
                 << ", size() = " << hltConfigProvider_.size() << "]";
  } else {
    edm::LogError("Input") << "initialization of HLTConfigProvider failed for Run=" << iRun.id() << " (process=\""
                           << processName_ << "\") -> plugin will not produce DQM outputs for this run";
    skipRun_ = true;
    return;
  }

  if (skipRun_ or initFailed_) {
    return;
  }

  auto hltMenuName(hltConfigProvider_.tableName());
  std::replace(hltMenuName.begin(), hltMenuName.end(), '/', '_');
  std::replace(hltMenuName.begin(), hltMenuName.end(), '.', '_');
  while (hltMenuName.front() == '_') {
    hltMenuName.erase(0, 1);
  }

  auto const& triggerNames(hltConfigProvider_.triggerNames());

  LogTrace("") << "[HLTPrinter::bookHistograms] HLTConfigProvider::size() = " << hltConfigProvider_.size()
               << ", HLTConfigProvider::triggerNames().size() = " << triggerNames.size();

  for (auto const& istream : hltConfigProvider_.streamNames()) {
    LogTrace("") << "[HLTPrinter::bookHistograms] Stream = \"" << istream << "\"";

    if (not this->skipStreamByName(istream)) {
      auto const& dsets(hltConfigProvider_.streamContent(istream));
      for (auto const& idset : dsets) {
        const std::vector<std::string>& dsetPathNames = hltConfigProvider_.datasetContent(idset);
        LogTrace("") << "[HLTPrinter::bookHistograms]   Dataset = \"" << idset << "\"";
        const std::string meDatasetName(idset);
        for (size_t idxPath = 0; idxPath < dsetPathNames.size(); ++idxPath) {
          auto const& iPathName(dsetPathNames.at(idxPath));
          if (std::find(triggerNames.begin(), triggerNames.end(), iPathName) == triggerNames.end()) {
            continue;
          }
          if (this->skipPathMonitorElement(iPathName)) {
            continue;
          }
          LogTrace("") << "[HLTPrinter::bookHistograms]     Path = \"" << iPathName << "\"";
          auto const& moduleLabels(hltConfigProvider_.moduleLabels(iPathName));
          std::vector<std::string> mePath_binLabels;
          mePath_binLabels.reserve(moduleLabels.size());
          for (size_t iMod = 0; iMod < moduleLabels.size(); ++iMod) {
            auto const& moduleLabel(moduleLabels.at(iMod));
            if (this->skipModuleByEDMType(hltConfigProvider_.moduleEDMType(moduleLabel)) or
                this->skipModuleByType(hltConfigProvider_.moduleType(moduleLabel))) {
              LogTrace("") << "[HLTPrinter::bookHistograms]       [-] Module = \"" << moduleLabel << "\"";
              continue;
            }
            LogTrace("") << "[HLTPrinter::bookHistograms]       [bin=" << mePath_binLabels.size() + 1
                         << "] Module = \"" << moduleLabel << "\"";
            mePath_binLabels.emplace_back(moduleLabel);
          }

          if (mePath_binLabels.empty()) {
            continue;
          }

          const std::string mePathName(idset + "_" + iPathName);
        }
      }
    }
  }
}

void HLTPrinter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (skipRun_ or initFailed_) {
    return;
  }

  LogTrace("") << "[HLTPrinter::analyze] --------------------------------------------------------";
  LogTrace("") << "[HLTPrinter::analyze] Run = " << iEvent.id().run()
               << ", LuminosityBlock = " << iEvent.id().luminosityBlock() << ", Event = " << iEvent.id().event();

  edm::Handle<edm::TriggerResults> triggerResults;
  iEvent.getByToken(triggerResultsToken_, triggerResults);

  if (not triggerResults.isValid()) {
    edm::LogWarning("Input") << "invalid handle to edm::TriggerResults (InputTag: \"triggerResults\")"
                             << " -> plugin will not fill DQM outputs for this event";
    return;
  }

  // fill MonitorElement: HLT-Menu (bin: path)
    auto const& triggerNames(hltConfigProvider_.triggerNames());
    for (auto const& iPathName : triggerNames) {
      const uint pathIndex(hltConfigProvider_.triggerIndex(iPathName));
      if (pathIndex >= triggerResults->size()) {
        edm::LogError("Logic") << "[HLTPrinter::analyze]       "
                               << "index associated to path \"" << iPathName << "\" (" << pathIndex
                               << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                               << ") -> plugin will not fill bin associated to this path in HLT-Menu MonitorElement";
        continue;
      }
      auto const pathAccept(triggerResults->accept(pathIndex));
    }

  edm::Handle<trigger::TriggerEvent> triggerEventAOD;
  iEvent.getByToken(triggerSummaryTokenAOD_, triggerEventAOD);

  edm::Handle<trigger::TriggerEventWithRefs> triggerEventRAW;

  bool useTriggerEventAOD(true);
  if (not triggerEventAOD.isValid()) {
    useTriggerEventAOD = false;
    edm::LogInfo("Input") << "invalid handle to trigger::TriggerEvent (InputTag: \"triggerSummaryAOD\"),"
                          << " will attempt to access trigger::TriggerEventWithRefs (InputTag: \"triggerSummaryRAW\")";

    iEvent.getByToken(triggerSummaryTokenRAW_, triggerEventRAW);
    if (not triggerEventRAW.isValid()) {
      edm::LogWarning("Input") << "invalid handle to trigger::TriggerEventWithRefs (InputTag: \"triggerSummaryRAW\")"
                               << " -> plugin will not fill DQM outputs for this event";
      return;
    }
  }

  auto const triggerEventSize(useTriggerEventAOD ? triggerEventAOD->sizeFilters() : triggerEventRAW->size());
  LogTrace("") << "[HLTPrinter::analyze] useTriggerEventAOD = " << useTriggerEventAOD
               << ", triggerEventSize = " << triggerEventSize;

  // fill MonitorElements for PrimaryDatasets and Paths
  // loop over Streams
  for (auto const& istream : hltConfigProvider_.streamNames()) {
    LogTrace("") << "[HLTPrinter::analyze]   Stream = \"" << istream << "\"";
    auto const& dsets(hltConfigProvider_.streamContent(istream));
    // loop over PrimaryDatasets in Stream
    for (auto const& idset : dsets) {
      LogTrace("") << "[HLTPrinter::analyze]     Dataset = \"" << idset << "\"";
      const std::string meDatasetName(idset);
      auto const& dsetPathNames(hltConfigProvider_.datasetContent(idset));
      // loop over Paths in PrimaryDataset
      for (auto const& iPathName : dsetPathNames) {
        const uint pathIndex(hltConfigProvider_.triggerIndex(iPathName));
        if (pathIndex >= triggerResults->size()) {
          edm::LogError("Logic") << "[HLTPrinter::analyze]       "
                                 << "index associated to path \"" << iPathName << "\" (" << pathIndex
                                 << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                                 << ") -> plugin will not fill DQM info related to this path";
          continue;
        }
        auto const pathAccept(triggerResults->accept(pathIndex));
        LogTrace("") << "[HLTPrinter::analyze]       "
                     << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                     << "\") = " << pathIndex << ", Accept = " << pathAccept;
        // fill MonitorElement: Path (bin: filter)
              unsigned indexLastFilterPathModules(triggerResults->index(pathIndex) + 1);
              LogTrace("") << "[HLTPrinter::analyze]         "
                           << "indexLastFilterPathModules = " << indexLastFilterPathModules;

              // identify module corresponding to last filter executed in the path
              while (indexLastFilterPathModules > 0) {
                --indexLastFilterPathModules;
                const std::string& labelLastFilterPathModules(
                    hltConfigProvider_.moduleLabel(pathIndex, indexLastFilterPathModules));
                const uint indexLastFilterFilters =
                    useTriggerEventAOD
                        ? triggerEventAOD->filterIndex(edm::InputTag(labelLastFilterPathModules, "", processName_))
                        : triggerEventRAW->filterIndex(edm::InputTag(labelLastFilterPathModules, "", processName_));
                LogTrace("") << "[HLTPrinter::analyze]           "
                             << "indexLastFilterPathModules = " << indexLastFilterPathModules
                             << ", labelLastFilterPathModules = " << labelLastFilterPathModules
                             << ", indexLastFilterFilters = " << indexLastFilterFilters
                             << " (triggerEventSize = " << triggerEventSize << ")";
                if (indexLastFilterFilters < triggerEventSize) {
                  if (this->skipModuleByType(hltConfigProvider_.moduleType(labelLastFilterPathModules))) {
                    continue;
                  }
                  break;
                }
              }

              // number of modules in the path
              const unsigned sizeModulesPath(hltConfigProvider_.size(pathIndex));
              LogTrace("") << "[HLTPrinter::analyze]         "
                           << "-> selected indexLastFilterPathModules = " << indexLastFilterPathModules
                           << " (HLTConfigProvider::size(" << pathIndex << ") = " << sizeModulesPath << ")";
              if (indexLastFilterPathModules >= sizeModulesPath) {
                edm::LogError("Logic") << " selected index (" << indexLastFilterPathModules
                                       << ") for last filter of path \"" << iPathName
                                       << "\" is inconsistent with number of modules in the path (" << sizeModulesPath
                                       << ")";
                continue;
              }
              // store decision of previous filter
              bool previousFilterAccept(true);
              for (size_t modIdx = 0; modIdx < sizeModulesPath; ++modIdx) {
                // each filter-bin is filled, with a 0 or 1, only when all previous filters in the path have passed
                if (not previousFilterAccept) {
                  break;
                }
                // consider only selected EDFilter modules
                auto const& moduleLabel(hltConfigProvider_.moduleLabel(pathIndex, modIdx));
                if (this->skipModuleByEDMType(hltConfigProvider_.moduleEDMType(moduleLabel)) or
                    this->skipModuleByType(hltConfigProvider_.moduleType(moduleLabel))) {
                  continue;
                }
                // index of the module in the path [0,sizeModulesPath)
                const unsigned slotModule(hltConfigProvider_.moduleIndex(pathIndex, moduleLabel));
                bool filterAccept(false);
                if (slotModule < indexLastFilterPathModules) {
                  filterAccept = true;
                } else if (slotModule == indexLastFilterPathModules) {
                  filterAccept = pathAccept;
                }
                LogTrace("") << "[HLTPrinter::analyze]         "
                             << "HLTConfigProvider::moduleLabel(" << pathIndex << ", " << modIdx << ") = \""
                             << moduleLabel << "\", HLTConfigProvider::moduleIndex(" << pathIndex << ", \""
                             << moduleLabel << "\") = " << slotModule << ", filterAccept = " << filterAccept
                             << ", previousFilterAccept = " << previousFilterAccept;
                previousFilterAccept = filterAccept;
              }
      }
    }
  }
}

bool HLTPrinter::skipStreamByName(const std::string& streamName) const {
  if ((streamName.find("Physics") != std::string::npos) || (streamName.find("Scouting") != std::string::npos) ||
      (streamName.find("Parking") != std::string::npos) || (streamName == "A")) {
    return false;
  }
  return true;
}

bool HLTPrinter::skipPathMonitorElement(const std::string& pathName) const {
  if ((pathName.find("HLT_") == std::string::npos) || (pathName.find("HLT_Physics") != std::string::npos) ||
      (pathName.find("HLT_Random") != std::string::npos)) {
    return true;
  }
  return false;
}

bool HLTPrinter::skipModuleByEDMType(const std::string& moduleEDMType) const {
  return (moduleEDMType != "EDFilter");
}

bool HLTPrinter::skipModuleByType(const std::string& moduleType) const { return (moduleType == "HLTBool"); }

void HLTPrinter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("triggerResults::HLT"));
  desc.add<edm::InputTag>("triggerSummaryAOD", edm::InputTag("hltTriggerSummaryAOD::HLT"));
  desc.add<edm::InputTag>("triggerSummaryRAW", edm::InputTag("hltTriggerSummaryRAW::HLT"));
  descriptions.add("hltPrinter", desc);
}

DEFINE_FWK_MODULE(HLTPrinter);
