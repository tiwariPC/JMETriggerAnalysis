#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATPackedCandidateCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoGenJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoCaloJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoGenMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoCaloMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATMuonCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h"

#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <unordered_map>

#include <Compression.h>
#include <TTree.h>

class JMETriggerNTuple : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit JMETriggerNTuple(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions&);

 protected:
  void beginJob() override {}
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override {}

  template <typename... Args>
  void addBranch(const std::string&, Args...);

  bool passesTriggerResults_OR(const edm::TriggerResults&, const edm::Event&, const std::vector<std::string>&);
  bool passesTriggerResults_AND(const edm::TriggerResults&, const edm::Event&, const std::vector<std::string>&);

  const std::string TTreeName_;

  const std::vector<std::string> TriggerResultsFilterOR_;
  const std::vector<std::string> TriggerResultsFilterAND_;

  const std::vector<std::string> outputBranchesToBeDropped_;

  std::unordered_map<std::string, std::string>  stringCutObjectSelectors_map_;

  std::unique_ptr<TriggerResultsContainer> triggerResultsContainer_ptr_;
  std::vector<RecoVertexCollectionContainer> v_recoVertexCollectionContainer_;
  std::vector<RecoPFCandidateCollectionContainer> v_recoPFCandidateCollectionContainer_;
  std::vector<PATPackedCandidateCollectionContainer> v_patPackedCandidateCollectionContainer_;
  std::vector<RecoGenJetCollectionContainer> v_recoGenJetCollectionContainer_;
  std::vector<RecoCaloJetCollectionContainer> v_recoCaloJetCollectionContainer_;
  std::vector<RecoPFJetCollectionContainer> v_recoPFJetCollectionContainer_;
  std::vector<PATJetCollectionContainer> v_patJetCollectionContainer_;
  std::vector<RecoGenMETCollectionContainer> v_recoGenMETCollectionContainer_;
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;
  std::vector<PATMETCollectionContainer> v_patMETCollectionContainer_;
  std::vector<PATMuonCollectionContainer> v_patMuonCollectionContainer_;
  std::vector<PATElectronCollectionContainer> v_patElectronCollectionContainer_;

  TTree* ttree_ = nullptr;

  unsigned int run_ = 0;
  unsigned int luminosityBlock_ = 0;
  unsigned long long event_ = 0;

  class FillCollectionConditionsMap {

   public:
    explicit FillCollectionConditionsMap();

    void clear();
    int init(const edm::ParameterSet&);

    struct condition {

      condition(const std::string& a_path, const bool a_accept=false) : path(a_path), accept(a_accept) {}

      const std::string path;
      bool accept;
    };

    bool has(const std::string&) const;
    const condition& at(const std::string&) const;
    bool accept(const std::string&) const;
    int update(const edm::TriggerResults&, const edm::Event&);

   protected:

    std::map<std::string, condition> condMap_;
  };

  FillCollectionConditionsMap fillCollectionConditionMap_;
};

JMETriggerNTuple::JMETriggerNTuple(const edm::ParameterSet& iConfig)
  : TTreeName_(iConfig.getParameter<std::string>("TTreeName"))
  , TriggerResultsFilterOR_(iConfig.getParameter<std::vector<std::string> >("TriggerResultsFilterOR"))
  , TriggerResultsFilterAND_(iConfig.getParameter<std::vector<std::string> >("TriggerResultsFilterAND"))
  , outputBranchesToBeDropped_(iConfig.getParameter<std::vector<std::string> >("outputBranchesToBeDropped")) {

  const auto& TriggerResultsInputTag = iConfig.getParameter<edm::InputTag>("TriggerResults");
  const auto& TriggerResultsCollections = iConfig.getParameter<std::vector<std::string> >("TriggerResultsCollections");

  triggerResultsContainer_ptr_.reset(new TriggerResultsContainer(TriggerResultsCollections, TriggerResultsInputTag.label(), this->consumes<edm::TriggerResults>(TriggerResultsInputTag)));

  // fillCollectionConditions
  fillCollectionConditionMap_.clear();

  if(iConfig.exists("fillCollectionConditions")){

    fillCollectionConditionMap_.init(iConfig.getParameter<edm::ParameterSet>("fillCollectionConditions"));
  }

  // stringCutObjectSelectors
  stringCutObjectSelectors_map_.clear();

  if(iConfig.exists("stringCutObjectSelectors")){

    const edm::ParameterSet& pset_stringCutObjectSelectors = iConfig.getParameter<edm::ParameterSet>("stringCutObjectSelectors");

    const auto& stringCutObjectSelectors_labels = pset_stringCutObjectSelectors.getParameterNamesForType<std::string>();

    for(const auto& label : stringCutObjectSelectors_labels){

      stringCutObjectSelectors_map_[label] = pset_stringCutObjectSelectors.getParameter<std::string>(label);
    }
  }

  // reco::VertexCollection
  v_recoVertexCollectionContainer_.clear();

  if(iConfig.exists("recoVertexCollections")){

    const edm::ParameterSet& pset_recoVertexCollections = iConfig.getParameter<edm::ParameterSet>("recoVertexCollections");

    const auto& inputTagLabels_recoVertexCollections = pset_recoVertexCollections.getParameterNamesForType<edm::InputTag>();

    v_recoVertexCollectionContainer_.reserve(inputTagLabels_recoVertexCollections.size());

    for(const auto& label : inputTagLabels_recoVertexCollections){

      const auto& inputTag = pset_recoVertexCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::VertexCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoVertexCollectionContainer_.emplace_back(RecoVertexCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::Vertex> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoVertexCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::PFCandidateCollection
  v_recoPFCandidateCollectionContainer_.clear();

  if(iConfig.exists("recoPFCandidateCollections")){

    const edm::ParameterSet& pset_recoPFCandidateCollections = iConfig.getParameter<edm::ParameterSet>("recoPFCandidateCollections");

    const auto& inputTagLabels_recoPFCandidateCollections = pset_recoPFCandidateCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFCandidateCollectionContainer_.reserve(inputTagLabels_recoPFCandidateCollections.size());

    for(const auto& label : inputTagLabels_recoPFCandidateCollections){

      const auto& inputTag = pset_recoPFCandidateCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFCandidateCollectionContainer_.emplace_back(RecoPFCandidateCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::PFCandidate> >(inputTag)));
      v_recoPFCandidateCollectionContainer_.back().orderByHighestPt(true);

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoPFCandidateCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // pat::PackedCandidateCollection
  v_patPackedCandidateCollectionContainer_.clear();

  if(iConfig.exists("patPackedCandidateCollections")){

    const edm::ParameterSet& pset_patPackedCandidateCollections = iConfig.getParameter<edm::ParameterSet>("patPackedCandidateCollections");

    const auto& inputTagLabels_patPackedCandidateCollections = pset_patPackedCandidateCollections.getParameterNamesForType<edm::InputTag>();

    v_patPackedCandidateCollectionContainer_.reserve(inputTagLabels_patPackedCandidateCollections.size());

    for(const auto& label : inputTagLabels_patPackedCandidateCollections){

      const auto& inputTag = pset_patPackedCandidateCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::PackedCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patPackedCandidateCollectionContainer_.emplace_back(PATPackedCandidateCollectionContainer(label, inputTag.label(), this->consumes<std::vector<pat::PackedCandidate> >(inputTag)));
      v_patPackedCandidateCollectionContainer_.back().orderByHighestPt(true);

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_patPackedCandidateCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::GenJetCollection
  v_recoGenJetCollectionContainer_.clear();

  if(iConfig.exists("recoGenJetCollections")){

    const edm::ParameterSet& pset_recoGenJetCollections = iConfig.getParameter<edm::ParameterSet>("recoGenJetCollections");

    const auto& inputTagLabels_recoGenJetCollections = pset_recoGenJetCollections.getParameterNamesForType<edm::InputTag>();

    v_recoGenJetCollectionContainer_.reserve(inputTagLabels_recoGenJetCollections.size());

    for(const auto& label : inputTagLabels_recoGenJetCollections){

      const auto& inputTag = pset_recoGenJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::GenJetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoGenJetCollectionContainer_.emplace_back(RecoGenJetCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::GenJet> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoGenJetCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::CaloJetCollection
  v_recoCaloJetCollectionContainer_.clear();

  if(iConfig.exists("recoCaloJetCollections")){

    const edm::ParameterSet& pset_recoCaloJetCollections = iConfig.getParameter<edm::ParameterSet>("recoCaloJetCollections");

    const auto& inputTagLabels_recoCaloJetCollections = pset_recoCaloJetCollections.getParameterNamesForType<edm::InputTag>();

    v_recoCaloJetCollectionContainer_.reserve(inputTagLabels_recoCaloJetCollections.size());

    for(const auto& label : inputTagLabels_recoCaloJetCollections){

      const auto& inputTag = pset_recoCaloJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::CaloJetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoCaloJetCollectionContainer_.emplace_back(RecoCaloJetCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::CaloJet> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoCaloJetCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::PFJetCollection
  v_recoPFJetCollectionContainer_.clear();

  if(iConfig.exists("recoPFJetCollections")){

    const edm::ParameterSet& pset_recoPFJetCollections = iConfig.getParameter<edm::ParameterSet>("recoPFJetCollections");

    const auto& inputTagLabels_recoPFJetCollections = pset_recoPFJetCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFJetCollectionContainer_.reserve(inputTagLabels_recoPFJetCollections.size());

    for(const auto& label : inputTagLabels_recoPFJetCollections){

      const auto& inputTag = pset_recoPFJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFJetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFJetCollectionContainer_.emplace_back(RecoPFJetCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::PFJet> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoPFJetCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // pat::JetCollection
  v_patJetCollectionContainer_.clear();

  if(iConfig.exists("patJetCollections")){

    const edm::ParameterSet& pset_patJetCollections = iConfig.getParameter<edm::ParameterSet>("patJetCollections");

    const auto& inputTagLabels_patJetCollections = pset_patJetCollections.getParameterNamesForType<edm::InputTag>();

    v_patJetCollectionContainer_.reserve(inputTagLabels_patJetCollections.size());

    for(const auto& label : inputTagLabels_patJetCollections){

      const auto& inputTag = pset_patJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::JetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patJetCollectionContainer_.emplace_back(PATJetCollectionContainer(label, inputTag.label(), this->consumes<std::vector<pat::Jet> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_patJetCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::GenMETCollection
  v_recoGenMETCollectionContainer_.clear();

  if(iConfig.exists("recoGenMETCollections")){

    const edm::ParameterSet& pset_recoGenMETCollections = iConfig.getParameter<edm::ParameterSet>("recoGenMETCollections");

    const auto& inputTagLabels_recoGenMETCollections = pset_recoGenMETCollections.getParameterNamesForType<edm::InputTag>();

    v_recoGenMETCollectionContainer_.reserve(inputTagLabels_recoGenMETCollections.size());

    for(const auto& label : inputTagLabels_recoGenMETCollections){

      const auto& inputTag = pset_recoGenMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::GenMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoGenMETCollectionContainer_.emplace_back(RecoGenMETCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::GenMET> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoGenMETCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::CaloMETCollection
  v_recoCaloMETCollectionContainer_.clear();

  if(iConfig.exists("recoCaloMETCollections")){

    const edm::ParameterSet& pset_recoCaloMETCollections = iConfig.getParameter<edm::ParameterSet>("recoCaloMETCollections");

    const auto& inputTagLabels_recoCaloMETCollections = pset_recoCaloMETCollections.getParameterNamesForType<edm::InputTag>();

    v_recoCaloMETCollectionContainer_.reserve(inputTagLabels_recoCaloMETCollections.size());

    for(const auto& label : inputTagLabels_recoCaloMETCollections){

      const auto& inputTag = pset_recoCaloMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::CaloMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoCaloMETCollectionContainer_.emplace_back(RecoCaloMETCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::CaloMET> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoCaloMETCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // reco::PFMETCollection
  v_recoPFMETCollectionContainer_.clear();

  if(iConfig.exists("recoPFMETCollections")){

    const edm::ParameterSet& pset_recoPFMETCollections = iConfig.getParameter<edm::ParameterSet>("recoPFMETCollections");

    const auto& inputTagLabels_recoPFMETCollections = pset_recoPFMETCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFMETCollectionContainer_.reserve(inputTagLabels_recoPFMETCollections.size());

    for(const auto& label : inputTagLabels_recoPFMETCollections){

      const auto& inputTag = pset_recoPFMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFMETCollectionContainer_.emplace_back(RecoPFMETCollectionContainer(label, inputTag.label(), this->consumes<std::vector<reco::PFMET> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_recoPFMETCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // pat::METCollection
  v_patMETCollectionContainer_.clear();

  if(iConfig.exists("patMETCollections")){

    const edm::ParameterSet& pset_patMETCollections = iConfig.getParameter<edm::ParameterSet>("patMETCollections");

    const auto& inputTagLabels_patMETCollections = pset_patMETCollections.getParameterNamesForType<edm::InputTag>();

    v_patMETCollectionContainer_.reserve(inputTagLabels_patMETCollections.size());

    for(const auto& label : inputTagLabels_patMETCollections){

      const auto& inputTag = pset_patMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::METCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patMETCollectionContainer_.emplace_back(PATMETCollectionContainer(label, inputTag.label(), this->consumes<std::vector<pat::MET> >(inputTag)));

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_patMETCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // pat::MuonCollection
  v_patMuonCollectionContainer_.clear();

  if(iConfig.exists("patMuonCollections")){

    const edm::ParameterSet& pset_patMuonCollections = iConfig.getParameter<edm::ParameterSet>("patMuonCollections");

    const auto& inputTagLabels_patMuonCollections = pset_patMuonCollections.getParameterNamesForType<edm::InputTag>();

    v_patMuonCollectionContainer_.reserve(inputTagLabels_patMuonCollections.size());

    for(const auto& label : inputTagLabels_patMuonCollections){

      const auto& inputTag = pset_patMuonCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::MuonCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patMuonCollectionContainer_.emplace_back(PATMuonCollectionContainer(label, inputTag.label(), this->consumes<std::vector<pat::Muon> >(inputTag)));
      v_patMuonCollectionContainer_.back().orderByHighestPt(true);

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_patMuonCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // pat::ElectronCollection
  v_patElectronCollectionContainer_.clear();

  if(iConfig.exists("patElectronCollections")){

    const edm::ParameterSet& pset_patElectronCollections = iConfig.getParameter<edm::ParameterSet>("patElectronCollections");

    const auto& inputTagLabels_patElectronCollections = pset_patElectronCollections.getParameterNamesForType<edm::InputTag>();

    v_patElectronCollectionContainer_.reserve(inputTagLabels_patElectronCollections.size());

    for(const auto& label : inputTagLabels_patElectronCollections){

      const auto& inputTag = pset_patElectronCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::ElectronCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patElectronCollectionContainer_.emplace_back(PATElectronCollectionContainer(label, inputTag.label(), this->consumes<std::vector<pat::Electron> >(inputTag)));
      v_patElectronCollectionContainer_.back().orderByHighestPt(true);

      if(stringCutObjectSelectors_map_.find(label) != stringCutObjectSelectors_map_.end()){

        v_patElectronCollectionContainer_.back().setStringCutObjectSelector(stringCutObjectSelectors_map_.at(label));
      }
    }
  }

  // setup TTree
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if(not fs){

    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fs->make<TTree>(TTreeName_.c_str(), TTreeName_.c_str());

  if(not ttree_){

    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }

  this->addBranch("run", &run_);
  this->addBranch("luminosityBlock", &luminosityBlock_);
  this->addBranch("event", &event_);

  for(const auto& triggerEntry_i : triggerResultsContainer_ptr_->entries()){

    this->addBranch(triggerEntry_i.name, const_cast<bool*>(&triggerEntry_i.accept));
  }

  for(auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_){

    this->addBranch(recoVertexCollectionContainer_i.name()+"_tracksSize", &recoVertexCollectionContainer_i.vec_tracksSize());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_isFake", &recoVertexCollectionContainer_i.vec_isFake());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_chi2", &recoVertexCollectionContainer_i.vec_chi2());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_ndof", &recoVertexCollectionContainer_i.vec_ndof());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_x", &recoVertexCollectionContainer_i.vec_x());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_y", &recoVertexCollectionContainer_i.vec_y());
    this->addBranch(recoVertexCollectionContainer_i.name()+"_z", &recoVertexCollectionContainer_i.vec_z());
  }

  for(auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_){

    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_pdgId", &recoPFCandidateCollectionContainer_i.vec_pdgId());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_pt", &recoPFCandidateCollectionContainer_i.vec_pt());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_eta", &recoPFCandidateCollectionContainer_i.vec_eta());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_phi", &recoPFCandidateCollectionContainer_i.vec_phi());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_mass", &recoPFCandidateCollectionContainer_i.vec_mass());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_vx", &recoPFCandidateCollectionContainer_i.vec_vx());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_vy", &recoPFCandidateCollectionContainer_i.vec_vy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name()+"_vz", &recoPFCandidateCollectionContainer_i.vec_vz());
  }

  for(auto& patPackedCandidateCollectionContainer_i : v_patPackedCandidateCollectionContainer_){

    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_pdgId", &patPackedCandidateCollectionContainer_i.vec_pdgId());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_pt", &patPackedCandidateCollectionContainer_i.vec_pt());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_eta", &patPackedCandidateCollectionContainer_i.vec_eta());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_phi", &patPackedCandidateCollectionContainer_i.vec_phi());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_mass", &patPackedCandidateCollectionContainer_i.vec_mass());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_vx", &patPackedCandidateCollectionContainer_i.vec_vx());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_vy", &patPackedCandidateCollectionContainer_i.vec_vy());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_vz", &patPackedCandidateCollectionContainer_i.vec_vz());
    this->addBranch(patPackedCandidateCollectionContainer_i.name()+"_fromPV", &patPackedCandidateCollectionContainer_i.vec_fromPV());
  }

  for(auto& recoGenJetCollectionContainer_i : v_recoGenJetCollectionContainer_){

    this->addBranch(recoGenJetCollectionContainer_i.name()+"_pt", &recoGenJetCollectionContainer_i.vec_pt());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_eta", &recoGenJetCollectionContainer_i.vec_eta());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_phi", &recoGenJetCollectionContainer_i.vec_phi());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_mass", &recoGenJetCollectionContainer_i.vec_mass());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_chargedHadronEnergyFraction", &recoGenJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_neutralHadronEnergyFraction", &recoGenJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_electronEnergyFraction", &recoGenJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_photonEnergyFraction", &recoGenJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_muonEnergyFraction", &recoGenJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_chargedHadronMultiplicity", &recoGenJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_neutralHadronMultiplicity", &recoGenJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_electronMultiplicity", &recoGenJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_photonMultiplicity", &recoGenJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name()+"_muonMultiplicity", &recoGenJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for(auto& recoCaloJetCollectionContainer_i : v_recoCaloJetCollectionContainer_){

    this->addBranch(recoCaloJetCollectionContainer_i.name()+"_pt", &recoCaloJetCollectionContainer_i.vec_pt());
    this->addBranch(recoCaloJetCollectionContainer_i.name()+"_eta", &recoCaloJetCollectionContainer_i.vec_eta());
    this->addBranch(recoCaloJetCollectionContainer_i.name()+"_phi", &recoCaloJetCollectionContainer_i.vec_phi());
    this->addBranch(recoCaloJetCollectionContainer_i.name()+"_mass", &recoCaloJetCollectionContainer_i.vec_mass());
  }

  for(auto& recoPFJetCollectionContainer_i : v_recoPFJetCollectionContainer_){

    this->addBranch(recoPFJetCollectionContainer_i.name()+"_pt", &recoPFJetCollectionContainer_i.vec_pt());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_eta", &recoPFJetCollectionContainer_i.vec_eta());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_phi", &recoPFJetCollectionContainer_i.vec_phi());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_mass", &recoPFJetCollectionContainer_i.vec_mass());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_chargedHadronEnergyFraction", &recoPFJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_neutralHadronEnergyFraction", &recoPFJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_electronEnergyFraction", &recoPFJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_photonEnergyFraction", &recoPFJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_muonEnergyFraction", &recoPFJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_chargedHadronMultiplicity", &recoPFJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_neutralHadronMultiplicity", &recoPFJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_electronMultiplicity", &recoPFJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_photonMultiplicity", &recoPFJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_muonMultiplicity", &recoPFJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for(auto& patJetCollectionContainer_i : v_patJetCollectionContainer_){

    this->addBranch(patJetCollectionContainer_i.name()+"_pt", &patJetCollectionContainer_i.vec_pt());
    this->addBranch(patJetCollectionContainer_i.name()+"_eta", &patJetCollectionContainer_i.vec_eta());
    this->addBranch(patJetCollectionContainer_i.name()+"_phi", &patJetCollectionContainer_i.vec_phi());
    this->addBranch(patJetCollectionContainer_i.name()+"_mass", &patJetCollectionContainer_i.vec_mass());
    this->addBranch(patJetCollectionContainer_i.name()+"_jesc", &patJetCollectionContainer_i.vec_jesc());
    this->addBranch(patJetCollectionContainer_i.name()+"_chargedHadronEnergyFraction", &patJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name()+"_neutralHadronEnergyFraction", &patJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name()+"_electronEnergyFraction", &patJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name()+"_photonEnergyFraction", &patJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name()+"_muonEnergyFraction", &patJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name()+"_chargedHadronMultiplicity", &patJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name()+"_neutralHadronMultiplicity", &patJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name()+"_electronMultiplicity", &patJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name()+"_photonMultiplicity", &patJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name()+"_muonMultiplicity", &patJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for(auto& recoGenMETCollectionContainer_i : v_recoGenMETCollectionContainer_){

    this->addBranch(recoGenMETCollectionContainer_i.name()+"_pt", &recoGenMETCollectionContainer_i.vec_pt());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_phi", &recoGenMETCollectionContainer_i.vec_phi());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_sumEt", &recoGenMETCollectionContainer_i.vec_sumEt());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_NeutralEMEtFraction", &recoGenMETCollectionContainer_i.vec_NeutralEMEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_NeutralHadEtFraction", &recoGenMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_ChargedEMEtFraction", &recoGenMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_ChargedHadEtFraction", &recoGenMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_MuonEtFraction", &recoGenMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name()+"_InvisibleEtFraction", &recoGenMETCollectionContainer_i.vec_InvisibleEtFraction());
  }

  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_pt", &recoCaloMETCollectionContainer_i.vec_pt());
    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_phi", &recoCaloMETCollectionContainer_i.vec_phi());
    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_sumEt", &recoCaloMETCollectionContainer_i.vec_sumEt());
  }

  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    this->addBranch(recoPFMETCollectionContainer_i.name()+"_pt", &recoPFMETCollectionContainer_i.vec_pt());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_phi", &recoPFMETCollectionContainer_i.vec_phi());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_sumEt", &recoPFMETCollectionContainer_i.vec_sumEt());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_NeutralEMFraction", &recoPFMETCollectionContainer_i.vec_NeutralEMFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_NeutralHadEtFraction", &recoPFMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_ChargedEMEtFraction", &recoPFMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_ChargedHadEtFraction", &recoPFMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_MuonEtFraction", &recoPFMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_Type6EtFraction", &recoPFMETCollectionContainer_i.vec_Type6EtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_Type7EtFraction", &recoPFMETCollectionContainer_i.vec_Type7EtFraction());
  }

  for(auto& patMETCollectionContainer_i : v_patMETCollectionContainer_){

    this->addBranch(patMETCollectionContainer_i.name()+"_Raw_pt", &patMETCollectionContainer_i.vec_Raw_pt());
    this->addBranch(patMETCollectionContainer_i.name()+"_Raw_phi", &patMETCollectionContainer_i.vec_Raw_phi());
    this->addBranch(patMETCollectionContainer_i.name()+"_Raw_sumEt", &patMETCollectionContainer_i.vec_Raw_sumEt());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1_pt", &patMETCollectionContainer_i.vec_Type1_pt());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1_phi", &patMETCollectionContainer_i.vec_Type1_phi());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1_sumEt", &patMETCollectionContainer_i.vec_Type1_sumEt());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1XY_pt", &patMETCollectionContainer_i.vec_Type1XY_pt());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1XY_phi", &patMETCollectionContainer_i.vec_Type1XY_phi());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type1XY_sumEt", &patMETCollectionContainer_i.vec_Type1XY_sumEt());
    this->addBranch(patMETCollectionContainer_i.name()+"_NeutralEMFraction", &patMETCollectionContainer_i.vec_NeutralEMFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_NeutralHadEtFraction", &patMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_ChargedEMEtFraction", &patMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_ChargedHadEtFraction", &patMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_MuonEtFraction", &patMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type6EtFraction", &patMETCollectionContainer_i.vec_Type6EtFraction());
    this->addBranch(patMETCollectionContainer_i.name()+"_Type7EtFraction", &patMETCollectionContainer_i.vec_Type7EtFraction());
  }

  for(auto& patMuonCollectionContainer_i : v_patMuonCollectionContainer_){

    this->addBranch(patMuonCollectionContainer_i.name()+"_pdgId", &patMuonCollectionContainer_i.vec_pdgId());
    this->addBranch(patMuonCollectionContainer_i.name()+"_pt", &patMuonCollectionContainer_i.vec_pt());
    this->addBranch(patMuonCollectionContainer_i.name()+"_eta", &patMuonCollectionContainer_i.vec_eta());
    this->addBranch(patMuonCollectionContainer_i.name()+"_phi", &patMuonCollectionContainer_i.vec_phi());
    this->addBranch(patMuonCollectionContainer_i.name()+"_mass", &patMuonCollectionContainer_i.vec_mass());
    this->addBranch(patMuonCollectionContainer_i.name()+"_vx", &patMuonCollectionContainer_i.vec_vx());
    this->addBranch(patMuonCollectionContainer_i.name()+"_vy", &patMuonCollectionContainer_i.vec_vy());
    this->addBranch(patMuonCollectionContainer_i.name()+"_vz", &patMuonCollectionContainer_i.vec_vz());
    this->addBranch(patMuonCollectionContainer_i.name()+"_dxyPV", &patMuonCollectionContainer_i.vec_dxyPV());
    this->addBranch(patMuonCollectionContainer_i.name()+"_dzPV", &patMuonCollectionContainer_i.vec_dzPV());
    this->addBranch(patMuonCollectionContainer_i.name()+"_id", &patMuonCollectionContainer_i.vec_id());
    this->addBranch(patMuonCollectionContainer_i.name()+"_pfIso", &patMuonCollectionContainer_i.vec_pfIso());
  }

  for(auto& patElectronCollectionContainer_i : v_patElectronCollectionContainer_){

    this->addBranch(patElectronCollectionContainer_i.name()+"_pdgId", &patElectronCollectionContainer_i.vec_pdgId());
    this->addBranch(patElectronCollectionContainer_i.name()+"_pt", &patElectronCollectionContainer_i.vec_pt());
    this->addBranch(patElectronCollectionContainer_i.name()+"_eta", &patElectronCollectionContainer_i.vec_eta());
    this->addBranch(patElectronCollectionContainer_i.name()+"_phi", &patElectronCollectionContainer_i.vec_phi());
    this->addBranch(patElectronCollectionContainer_i.name()+"_mass", &patElectronCollectionContainer_i.vec_mass());
    this->addBranch(patElectronCollectionContainer_i.name()+"_vx", &patElectronCollectionContainer_i.vec_vx());
    this->addBranch(patElectronCollectionContainer_i.name()+"_vy", &patElectronCollectionContainer_i.vec_vy());
    this->addBranch(patElectronCollectionContainer_i.name()+"_vz", &patElectronCollectionContainer_i.vec_vz());
    this->addBranch(patElectronCollectionContainer_i.name()+"_dxyPV", &patElectronCollectionContainer_i.vec_dxyPV());
    this->addBranch(patElectronCollectionContainer_i.name()+"_dzPV", &patElectronCollectionContainer_i.vec_dzPV());
    this->addBranch(patElectronCollectionContainer_i.name()+"_id", &patElectronCollectionContainer_i.vec_id());
    this->addBranch(patElectronCollectionContainer_i.name()+"_pfIso", &patElectronCollectionContainer_i.vec_pfIso());
    this->addBranch(patElectronCollectionContainer_i.name()+"_etaSC", &patElectronCollectionContainer_i.vec_etaSC());
  }

  // settings for output TFile and TTree
  fs->file().SetCompressionAlgorithm(ROOT::ECompressionAlgorithm::kLZ4);
  fs->file().SetCompressionLevel(4);

  for(int idx=0; idx<ttree_->GetListOfBranches()->GetEntries(); ++idx){

    TBranch* br = dynamic_cast<TBranch*>(ttree_->GetListOfBranches()->At(idx));
    if(br){ br->SetBasketSize(1024 * 1024); }
  }

  if(ttree_->GetListOfBranches()->GetEntries() > 0){

    ttree_->SetAutoFlush(-1024 * 1024 * ttree_->GetListOfBranches()->GetEntries());
  }
}

void JMETriggerNTuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  run_ = iEvent.id().run();
  luminosityBlock_ = iEvent.id().luminosityBlock();
  event_ = iEvent.id().event();

  // fill TriggerResultsContainer
  edm::Handle<edm::TriggerResults> triggerResults_handle;
  iEvent.getByToken(triggerResultsContainer_ptr_->token(), triggerResults_handle);

  if(not triggerResults_handle.isValid()){

    edm::LogWarning("JMETriggerNTuple::analyze")
      << "invalid handle for input collection: \"" << triggerResultsContainer_ptr_->inputTagLabel() << "\" (NTuple branches for HLT paths)";

    triggerResultsContainer_ptr_->clear();
  }
  else {

    // exit method for events that do not pass the logical OR of the specified HLT paths (if any)
    if(TriggerResultsFilterOR_.size() > 0){

      if(not this->passesTriggerResults_OR(*triggerResults_handle, iEvent, TriggerResultsFilterOR_)){

        return;
      }
    }

    // exit method for events that do not pass the logical AND of the specified HLT paths (if any)
    if(TriggerResultsFilterAND_.size() > 0){

      if(not this->passesTriggerResults_AND(*triggerResults_handle, iEvent, TriggerResultsFilterAND_)){

        return;
      }
    }

    LogDebug("JMETriggerNTuple::analyze") << "output collections will be saved to TTree";

    // fill TriggerResultsContainer
    triggerResultsContainer_ptr_->fill(*triggerResults_handle, iEvent);

    // update fill-collection conditions
    fillCollectionConditionMap_.update(*triggerResults_handle, iEvent);
  }

  // fill recoVertexCollectionContainers
  for(auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_){

    recoVertexCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoVertexCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoVertexCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::Vertex> > i_handle;
    iEvent.getByToken(recoVertexCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoVertexCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoVertexCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoVertexCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFCandidateCollectionContainers
  for(auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_){

    recoPFCandidateCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoPFCandidateCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoPFCandidateCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::PFCandidate> > i_handle;
    iEvent.getByToken(recoPFCandidateCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFCandidateCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patPackedCandidateCollectionContainers
  for(auto& patPackedCandidateCollectionContainer_i : v_patPackedCandidateCollectionContainer_){

    patPackedCandidateCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(patPackedCandidateCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(patPackedCandidateCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<pat::PackedCandidate> > i_handle;
    iEvent.getByToken(patPackedCandidateCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patPackedCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patPackedCandidateCollectionContainer_i.name() << "_*\")";
    }
    else {

      patPackedCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoGenJetCollectionContainers
  if(not iEvent.isRealData()){

    for(auto& recoGenJetCollectionContainer_i : v_recoGenJetCollectionContainer_){

      recoGenJetCollectionContainer_i.clear();

      if(fillCollectionConditionMap_.has(recoGenJetCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoGenJetCollectionContainer_i.name()))){

        continue;
      }

      edm::Handle<std::vector<reco::GenJet> > i_handle;
      iEvent.getByToken(recoGenJetCollectionContainer_i.token(), i_handle);

      if(not i_handle.isValid()){

        edm::LogWarning("JMETriggerNTuple::analyze")
          << "invalid handle for input collection: \"" << recoGenJetCollectionContainer_i.inputTagLabel()
          << "\" (NTuple branches: \"" << recoGenJetCollectionContainer_i.name() << "_*\")";
      }
      else {

        recoGenJetCollectionContainer_i.fill(*i_handle);
      }
    }
  }

  // fill recoCaloJetCollectionContainers
  for(auto& recoCaloJetCollectionContainer_i : v_recoCaloJetCollectionContainer_){

    recoCaloJetCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoCaloJetCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoCaloJetCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::CaloJet> > i_handle;
    iEvent.getByToken(recoCaloJetCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoCaloJetCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoCaloJetCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoCaloJetCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFJetCollectionContainers
  for(auto& recoPFJetCollectionContainer_i : v_recoPFJetCollectionContainer_){

    recoPFJetCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoPFJetCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoPFJetCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::PFJet> > i_handle;
    iEvent.getByToken(recoPFJetCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFJetCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFJetCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFJetCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patJetCollectionContainers
  for(auto& patJetCollectionContainer_i : v_patJetCollectionContainer_){

    patJetCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(patJetCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(patJetCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<pat::Jet> > i_handle;
    iEvent.getByToken(patJetCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patJetCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patJetCollectionContainer_i.name() << "_*\")";
    }
    else {

      patJetCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoGenMETCollectionContainers
  if(not iEvent.isRealData()){

    for(auto& recoGenMETCollectionContainer_i : v_recoGenMETCollectionContainer_){

      recoGenMETCollectionContainer_i.clear();

      if(fillCollectionConditionMap_.has(recoGenMETCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoGenMETCollectionContainer_i.name()))){

        continue;
      }

      edm::Handle<std::vector<reco::GenMET> > i_handle;
      iEvent.getByToken(recoGenMETCollectionContainer_i.token(), i_handle);

      if(not i_handle.isValid()){

        edm::LogWarning("JMETriggerNTuple::analyze")
          << "invalid handle for input collection: \"" << recoGenMETCollectionContainer_i.inputTagLabel()
          << "\" (NTuple branches: \"" << recoGenMETCollectionContainer_i.name() << "_*\")";
      }
      else { 

        recoGenMETCollectionContainer_i.fill(*i_handle);
      }
    }
  }

  // fill recoCaloMETCollectionContainers
  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    recoCaloMETCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoCaloMETCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoCaloMETCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::CaloMET> > i_handle;
    iEvent.getByToken(recoCaloMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: " << recoCaloMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoCaloMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoCaloMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFMETCollectionContainers
  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    recoPFMETCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(recoPFMETCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(recoPFMETCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<reco::PFMET> > i_handle;
    iEvent.getByToken(recoPFMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patMETCollectionContainers
  for(auto& patMETCollectionContainer_i : v_patMETCollectionContainer_){

    patMETCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(patMETCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(patMETCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<pat::MET> > i_handle;
    iEvent.getByToken(patMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      patMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patMuonCollectionContainers
  for(auto& patMuonCollectionContainer_i : v_patMuonCollectionContainer_){

    patMuonCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(patMuonCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(patMuonCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<pat::Muon> > i_handle;
    iEvent.getByToken(patMuonCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patMuonCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patMuonCollectionContainer_i.name() << "_*\")";
    }
    else {

      patMuonCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patElectronCollectionContainers
  for(auto& patElectronCollectionContainer_i : v_patElectronCollectionContainer_){

    patElectronCollectionContainer_i.clear();

    if(fillCollectionConditionMap_.has(patElectronCollectionContainer_i.name()) and (not fillCollectionConditionMap_.accept(patElectronCollectionContainer_i.name()))){

      continue;
    }

    edm::Handle<std::vector<pat::Electron> > i_handle;
    iEvent.getByToken(patElectronCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patElectronCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patElectronCollectionContainer_i.name() << "_*\")";
    }
    else {

      patElectronCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill TTree
  ttree_->Fill();
}

template <typename... Args>
void JMETriggerNTuple::addBranch(const std::string& branch_name, Args... args){

  if(ttree_){

    if(std::find(outputBranchesToBeDropped_.begin(), outputBranchesToBeDropped_.end(), branch_name) == outputBranchesToBeDropped_.end()){

      if(ttree_->GetBranch(branch_name.c_str())){

        throw cms::Exception("JMETriggerNTuple::addBranch") << "output branch \"" << branch_name
          << "\" already exists (there was an attempt to create another TBranch with the same name)";
      }
      else {

        ttree_->Branch(branch_name.c_str(), args...);
      }
    }
    else {

      edm::LogInfo("JMETriggerNTuple::addBranch") << "output branch \"" << branch_name
        << "\" will not be created (string appears in data member \"outputBranchesToBeDropped\")";
    }
  }
  else {

    edm::LogWarning("JMETriggerNTuple::addBranch") << "pointer to TTree is null, output branch \"" << branch_name << "\" will not be created";
  }
}


bool JMETriggerNTuple::passesTriggerResults_OR(const edm::TriggerResults& triggerResults, const edm::Event& iEvent, const std::vector<std::string>& paths){

  if(paths.size() == 0){

    edm::LogWarning("JMETriggerNTuple::passesTriggerResults_OR") << "input error: empty list of paths for event selection, will return True";

    return true;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if(triggerResults.size() != triggerNames.size()){

    edm::LogWarning("JMETriggerNTuple::passesTriggerResults_OR") << "input error: size of TriggerResults ("
      << triggerResults.size() << ") and TriggerNames (" << triggerNames.size() << ") differ, exiting function";

    return false;
  }

  for(unsigned int idx=0; idx<triggerResults.size(); ++idx){

    if(triggerResults.at(idx).accept() == true){

      const auto& triggerName = triggerNames.at(idx);

      if(std::find(paths.begin(), paths.end(), triggerName) != paths.end()){

        LogDebug("JMETriggerNTuple::passesTriggerResults_OR") << "event accepted by path \"" << triggerName << "\"";

        return true;
      }
      else {

        const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

        if(std::find(paths.begin(), paths.end(), triggerName_unv) != paths.end()){

          LogDebug("JMETriggerNTuple::passesTriggerResults_OR") << "event accepted by path \"" << triggerName_unv << "\"";

          return true;
        }
      }
    }
  }

  return false;
}

bool JMETriggerNTuple::passesTriggerResults_AND(const edm::TriggerResults& triggerResults, const edm::Event& iEvent, const std::vector<std::string>& paths){

  if(paths.size() == 0){

    edm::LogWarning("JMETriggerNTuple::passesTriggerResults_AND") << "input error: empty list of paths for event selection, will return True";

    return true;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if(triggerResults.size() != triggerNames.size()){

    edm::LogWarning("JMETriggerNTuple::passesTriggerResults_AND") << "input error: size of TriggerResults ("
      << triggerResults.size() << ") and TriggerNames (" << triggerNames.size() << ") differ, exiting function";

    return false;
  }

  for(unsigned int idx=0; idx<triggerResults.size(); ++idx){

    if(triggerResults.at(idx).accept() == false){

      const auto& triggerName = triggerNames.at(idx);

      if(std::find(paths.begin(), paths.end(), triggerName) != paths.end()){

        LogDebug("JMETriggerNTuple::passesTriggerResults_AND") << "event not accepted by path \"" << triggerName << "\"";

        return false;
      }
      else {

        const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

        if(std::find(paths.begin(), paths.end(), triggerName_unv) != paths.end()){

          LogDebug("JMETriggerNTuple::passesTriggerResults_AND") << "event not accepted by path \"" << triggerName_unv << "\"";

          return false;
        }
      }
    }
  }

  return true;
}

JMETriggerNTuple::FillCollectionConditionsMap::FillCollectionConditionsMap(){

  this->clear();
}

int JMETriggerNTuple::FillCollectionConditionsMap::init(const edm::ParameterSet& pset){

  this->clear();

  const auto& pset_strings = pset.getParameterNamesForType<std::string>();

  for(const auto& name : pset_strings){

    if(not this->has(name)){

      condMap_.insert({name, condition(pset.getParameter<std::string>(name))});
    }
  }

  return 0;
}

void JMETriggerNTuple::FillCollectionConditionsMap::clear(){

  condMap_.clear();
}

bool JMETriggerNTuple::FillCollectionConditionsMap::has(const std::string& name) const {

  return (condMap_.find(name) != condMap_.end());
}

const JMETriggerNTuple::FillCollectionConditionsMap::condition& JMETriggerNTuple::FillCollectionConditionsMap::at(const std::string& name) const {

  if(not this->has(name)){

    throw cms::Exception("LogicError") << "internal map has no entry associated to key \"" << name << "\"";
  }

  return condMap_.at(name);
}

bool JMETriggerNTuple::FillCollectionConditionsMap::accept(const std::string& name) const {

  if(not this->has(name)){

    throw cms::Exception("LogicError") << "internal map has no entry associated to key \"" << name << "\"";
  }

  return this->at(name).accept;
}

int JMETriggerNTuple::FillCollectionConditionsMap::update(const edm::TriggerResults& triggerResults, const edm::Event& iEvent){

  for(auto& map_entry : condMap_){

    map_entry.second.accept = false;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if(triggerResults.size() != triggerNames.size()){

    edm::LogWarning("InputError") << "size of TriggerResults (" << triggerResults.size()
      << ") and TriggerNames (" << triggerNames.size() << ") differ, exiting function";

    return 1;
  }

  for(unsigned int idx=0; idx<triggerResults.size(); ++idx){

    LogDebug("FillCollectionConditionsMap::update") << "path = " << triggerNames.at(idx) << ", accept = " << triggerResults.at(idx).accept();

    // since default value of condition::accept is false,
    // the value needs to be changed only for accepted paths
    if(triggerResults.at(idx).accept()){

      const auto& triggerName = triggerNames.at(idx);
      const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

      for(auto& map_entry : condMap_){

        // require match either full name or name without version
        if((map_entry.second.path == triggerName_unv) || (map_entry.second.path == triggerName)){

          map_entry.second.accept = triggerResults.at(idx).accept();

	  LogDebug("FillCollectionConditionsMap::update") << "triggerResults entry \"" << triggerNames.at(idx)
            << "\" matches condition \"" << map_entry.second.path << "\" for collection \"" << map_entry.first
            << "\" (accept=" << map_entry.second.accept << ")";
        }
      }
    }
  }

  return 0;
}

void JMETriggerNTuple::fillDescriptions(edm::ConfigurationDescriptions& descriptions){

  edm::ParameterSetDescription desc;
  desc.setUnknown();
//  desc.add<std::string>("TTreeName", "TTreeName")->setComment("Name of TTree");
//  desc.add<std::vector<std::string> >("TriggerResultsFilterOR")->setComment("List of HLT paths (without version) used in OR to select events in the output TTree");
//  desc.add<std::vector<std::string> >("TriggerResultsFilterAND")->setComment("List of HLT paths (without version) used in AND to select events in the output TTree");
//  desc.add<std::vector<std::string> >("outputBranchesToBeDropped")->setComment("Names of branches not to be included in the output TTree");
//  desc.add<edm::InputTag>("TriggerResults", edm::InputTag("TriggerResults"))->setComment("edm::InputTag for edm::TriggerResults");
//  desc.add<std::vector<std::string> >("TriggerResultsCollections")->setComment("List of HLT paths (without version) to be saved in the output TTree");

//  edm::ParameterSetDescription recoCaloMETCollections;
//  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("JMETriggerNTuple", desc);
}

DEFINE_FWK_MODULE(JMETriggerNTuple);
