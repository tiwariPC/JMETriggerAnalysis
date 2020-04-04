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
#include "DataFormats/L1TGlobal/interface/GlobalLogicParser.h"

#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"

#include <string>
#include <vector>
#include <map>
#include <algorithm>

#define LogTrace(X) std::cout << std::endl

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

  HLTPrescaleProvider hltPrescaleProvider_;
};

HLTPrinter::HLTPrinter(const edm::ParameterSet& iConfig)
  : processName_(""),
    initFailed_(false),
    skipRun_(false),
    hltPrescaleProvider_(iConfig, consumesCollector(), *this) {
  auto const triggerResultsInputTag(iConfig.getParameter<edm::InputTag>("triggerResults"));

  if (triggerResultsInputTag.process().empty()) {
    edm::LogError("Input") << "process not specified in HLT TriggerResults InputTag \""
                           << triggerResultsInputTag.encode() << "\" -> plugin will not produce DQM outputs";
    initFailed_ = true;
    return;
  } else {
    processName_ = triggerResultsInputTag.process();

    triggerResultsToken_ = consumes<edm::TriggerResults>(triggerResultsInputTag);
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
  if (hltPrescaleProvider_.init(iRun, iSetup, processName_, hltChanged)) {
    LogTrace("") << "[HLTPrinter::dqmBeginRun] HLTPrescaleProvider initialized [processName() = "
                 << hltPrescaleProvider_.hltConfigProvider().processName() << ", tableName() = " << hltPrescaleProvider_.hltConfigProvider().tableName()
                 << ", size() = " << hltPrescaleProvider_.hltConfigProvider().size() << "]";
  } else {
    edm::LogError("Input") << "initialization of HLTPrescaleProvider failed for Run=" << iRun.id() << " (process=\""
                           << processName_ << "\") -> plugin will not produce DQM outputs for this run";
    skipRun_ = true;
    return;
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

  auto const& l1GlobalUtils = hltPrescaleProvider_.l1tGlobalUtil();

  std::cout <<"l1 menu "<<l1GlobalUtils.gtTriggerMenuName()<<" version "<<l1GlobalUtils.gtTriggerMenuVersion()<<" comment "<<std::endl;
  std::cout <<"hlt name "<<hltPrescaleProvider_.hltConfigProvider().tableName()<<std::endl;

  auto const psColumn(hltPrescaleProvider_.prescaleSet(iEvent, iSetup));

  auto const& triggerNames(hltPrescaleProvider_.hltConfigProvider().triggerNames());
  for (auto const& iPathName : triggerNames) {

    auto const iPathNameUnv(iPathName.substr(0, iPathName.rfind("_v")));
    if(iPathNameUnv != "HLT_PFJet40" and iPathNameUnv != "HLT_PFJet200" and iPathNameUnv != "HLT_PFJet550"){ continue; }

    const uint iPathIndex(hltPrescaleProvider_.hltConfigProvider().triggerIndex(iPathName));
    if (iPathIndex >= triggerResults->size()) {
      edm::LogError("Logic") << "[HLTPrinter::analyze]       "
                             << "index associated to path \"" << iPathName << "\" (" << iPathIndex
                             << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                             << ") -> plugin will not fill bin associated to this path in HLT-Menu MonitorElement";
      continue;
    }

    LogTrace("") << "[HLTPrinter::analyze]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex;

    LogTrace("") << "[HLTPrinter::analyze]       moduleLabels";

    int hltL1TSeedModuleIndex(-1), hltPrescaleModuleIndex(-1), hltPathLastModuleIndex(-1);
    auto const lastModuleExecutedInPath(hltPrescaleProvider_.hltConfigProvider().moduleLabel(iPathIndex, triggerResults->index(iPathIndex)));
    auto const& moduleLabels(hltPrescaleProvider_.hltConfigProvider().moduleLabels(iPathIndex));
    for(size_t idx=0; idx<moduleLabels.size(); ++idx){
      auto const& moduleLabel(moduleLabels.at(idx));

      if(moduleLabel == lastModuleExecutedInPath){
        hltPathLastModuleIndex = idx;
      }

      if((hltPrescaleProvider_.hltConfigProvider().moduleEDMType(moduleLabel) != "EDFilter") or (moduleLabel == "hltTriggerType") or (moduleLabel == "hltBoolEnd")){
        continue;
      }

      if(moduleLabel.find("hltL1", 0) == 0){
        if((hltL1TSeedModuleIndex < 0) and (hltPrescaleModuleIndex < 0)){
          hltL1TSeedModuleIndex = idx;
        }
        else if(hltL1TSeedModuleIndex >= 0){
          throw cms::Exception("InputError") << "found more than one match for L1T-Seed module of HLT-Path"
            << " (1st match = \"" << moduleLabels.at(hltL1TSeedModuleIndex) << "\", 2nd match = \"" << moduleLabel << "\")"
            << ", HLT-Path = \"" << iPathName << "\"";
        }
        else {
          throw cms::Exception("InputError") << "found L1T-Seed module of HLT-Path after its HLT-Prescale module"
            << " (L1T-Seed module = \"" << moduleLabel << ", HLT-Prescale module = " << moduleLabels.at(hltPrescaleModuleIndex) << "\")"
            << ", HLT-Path = \"" << iPathName << "\"";
        }
      }

      if(moduleLabel.find("hltPre", 0) == 0){
        if((hltL1TSeedModuleIndex >= 0) and (hltPrescaleModuleIndex < 0)){
          hltPrescaleModuleIndex = idx;
        }
        else if(hltPrescaleModuleIndex >= 0){
          throw cms::Exception("InputError") << "found more than one match for HLT-Prescale module of HLT-Path"
            << " (1st match = \"" << moduleLabels.at(hltPrescaleModuleIndex) << "\", 2nd match = \"" << moduleLabel << "\")"
            << ", HLT-Path = \"" << iPathName << "\"";
        }
        else {
          throw cms::Exception("InputError") << "found HLT-Prescale module of HLT-Path before its L1T-Seed module"
            << " (HLT-Prescale module = \"" << moduleLabel << "\"), HLT-Path = \"" << iPathName << "\"";
        }
      }

      LogTrace("") << "[HLTPrinter::analyze]         " << moduleLabel << " " << hltPrescaleProvider_.hltConfigProvider().moduleEDMType(moduleLabel);
    }

    if(hltPathLastModuleIndex < 0){
      throw cms::Exception("InputError") << "failed to find last module executed in the HLT-Path: " << iPathName;
    }
    else if(hltL1TSeedModuleIndex < 0){
      throw cms::Exception("InputError") << "failed to find L1T-Seed module of HLT-Path: " << iPathName;
    }
    else if(hltPrescaleModuleIndex < 0){
      throw cms::Exception("InputError") << "failed to find HLT-Prescale module of HLT-Path: " << iPathName;
    }

    LogTrace("") << "[HLTPrinter::analyze]         "
      << "hltL1TSeedModuleIndex = " << hltL1TSeedModuleIndex << ", \"" << moduleLabels.at(hltL1TSeedModuleIndex) << "\")"
      << ", hltPrescaleModuleIndex = " << hltPrescaleModuleIndex << ", \"" << moduleLabels.at(hltPrescaleModuleIndex) << "\")"
      << ", hltPathLastModuleIndex = (" << hltPathLastModuleIndex << ", \"" << moduleLabels.at(hltPathLastModuleIndex) << "\")";

    auto const l1tAccept(hltL1TSeedModuleIndex < hltPathLastModuleIndex);
    auto const hltPrescaleApplied(hltPrescaleProvider_.rejectedByHLTPrescaler(*triggerResults, iPathIndex));
    auto const hltAccept(triggerResults->accept(iPathIndex));

    bool l1tAcceptFromL1GU(false);
    bool l1tPrescaleApplied(false);
    LogTrace("") << "[HLTPrinter::analyze]       hltL1TSeeds";
    auto const& hltL1TSeeds(hltPrescaleProvider_.hltConfigProvider().hltL1TSeeds(iPathIndex));
    for(auto tmp : hltL1TSeeds){
      if (tmp.empty()) {
        throw cms::Exception("FailModule") << "name of L1T seed is empty.";
      }
      else if (tmp != "L1GlobalDecision") {
        // breakdown of the L1T seed expression (ref: HLTL1Seed plugin)

        // check also the logical expression - add/remove spaces if needed
        // use GlobalLogicParser ctor with (non-const) std::string&
        auto l1AlgoLogicParser = GlobalLogicParser(tmp);
        l1tAcceptFromL1GU = l1AlgoLogicParser.expressionResult();
        for(auto tmp_l1s : l1AlgoLogicParser.expressionSeedsOperandList()){
          auto const& tmp_l1s_name(tmp_l1s.tokenName);

          bool decInitial(false);
          auto const decInitialIsValid(l1GlobalUtils.getInitialDecisionByName(tmp_l1s_name, decInitial));

          bool decInterm(false);
          auto const decIntermIsValid(l1GlobalUtils.getIntermDecisionByName(tmp_l1s_name, decInterm));

          bool decFinal(false);
          auto const decFinalIsValid(l1GlobalUtils.getFinalDecisionByName(tmp_l1s_name, decFinal));

          if((not l1tPrescaleApplied) and decInitialIsValid and decFinalIsValid){
            l1tPrescaleApplied = (decInitial != decFinal);
          }

          LogTrace("") << "[HLTPrinter::analyze]         " << tmp_l1s_name
            << " [ " << (decInitialIsValid and decInitial) << " "
            << (decIntermIsValid and decInterm) << " "
            << (decFinalIsValid and decFinal) << " ]";
        }
      }
      else {
        throw cms::Exception("FailModule") << "HLT-Path \"" << iPathName << "\" seeded at L1T by \"L1GlobalDecision\" (case not supported by this plugin).";
      }
      LogTrace("") << "[HLTPrinter::analyze]       " << tmp << " l1tPrescaleApplied=" << l1tPrescaleApplied;
    }

    if(l1tAccept != l1tAcceptFromL1GU){
      throw cms::Exception("InputError") << "return value of L1T-Seed module of HLT-Path ("
        << l1tAccept << ") conflicts with information from HLTPrescaleProvider::l1tGlobalUtil ("
        << l1tAcceptFromL1GU << "): " << iPathName;
    }

    LogTrace("") << "[HLTPrinter::analyze]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName << "\") = " << iPathIndex
                 << " l1tAccept=" << l1tAccept
                 << " l1tPrescaleApplied=" << l1tPrescaleApplied
                 << " hltPrescaleApplied=" << hltPrescaleApplied
                 << " hltAccept=" << hltAccept;
  }
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
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults::HLT"));
  descriptions.add("hltPrinter", desc);
}

DEFINE_FWK_MODULE(HLTPrinter);
