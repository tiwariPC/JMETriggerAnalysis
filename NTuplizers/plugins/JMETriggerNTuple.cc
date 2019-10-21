#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDAnalyzer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <FWCore/ServiceRegistry/interface/Service.h>
#include <CommonTools/UtilAlgos/interface/TFileService.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATPackedCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATMuonCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h>

#include <string>
#include <vector>
#include <memory>
#include <algorithm>

#include <TTree.h>

class JMETriggerNTuple : public edm::EDAnalyzer {

 public:
  explicit JMETriggerNTuple(const edm::ParameterSet&);
  virtual ~JMETriggerNTuple() {}

  static void fillDescriptions(edm::ConfigurationDescriptions&);

 protected:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  template <typename... Args>
  void addBranch(const std::string&, Args...);

  const std::string TTreeName_;

  const std::vector<std::string> HLTPathsFilterOR_;

  const std::vector<std::string> outputBranchesToBeDropped_;

  TTree* ttree_ = nullptr;

  unsigned int run_;
  unsigned int luminosityBlock_;
  unsigned long long event_;

  std::unique_ptr<TriggerResultsContainer> triggerResultsContainer_ptr_;
  std::vector<RecoVertexCollectionContainer> v_recoVertexCollectionContainer_;
  std::vector<RecoPFCandidateCollectionContainer> v_recoPFCandidateCollectionContainer_;
  std::vector<PATPackedCandidateCollectionContainer> v_patPackedCandidateCollectionContainer_;
  std::vector<RecoPFJetCollectionContainer> v_recoPFJetCollectionContainer_;
  std::vector<PATJetCollectionContainer> v_patJetCollectionContainer_;
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;
  std::vector<PATMETCollectionContainer> v_patMETCollectionContainer_;
  std::vector<PATMuonCollectionContainer> v_patMuonCollectionContainer_;
  std::vector<PATElectronCollectionContainer> v_patElectronCollectionContainer_;
};

JMETriggerNTuple::JMETriggerNTuple(const edm::ParameterSet& iConfig)
  : TTreeName_(iConfig.getParameter<std::string>("TTreeName"))
  , HLTPathsFilterOR_(iConfig.getParameter<std::vector<std::string> >("HLTPathsFilterOR"))
  , outputBranchesToBeDropped_(iConfig.getParameter<std::vector<std::string> >("outputBranchesToBeDropped")) {

  const auto& TriggerResultsInputTag = iConfig.getParameter<edm::InputTag>("TriggerResults");
  const auto& HLTPathsWithoutVersion = iConfig.getParameter<std::vector<std::string> >("HLTPathsWithoutVersion");

  triggerResultsContainer_ptr_.reset(new TriggerResultsContainer(HLTPathsWithoutVersion, TriggerResultsInputTag.label(), this->consumes<edm::TriggerResults>(TriggerResultsInputTag)));

  // reco::VertexCollection
  v_recoVertexCollectionContainer_.clear();

  if(iConfig.exists("recoVertexCollections")){

    const edm::ParameterSet& pset_recoVertexCollections = iConfig.getParameter<edm::ParameterSet>("recoVertexCollections");

    const auto& inputTagLabels_recoVertexCollections = pset_recoVertexCollections.getParameterNamesForType<edm::InputTag>();

    v_recoVertexCollectionContainer_.reserve(inputTagLabels_recoVertexCollections.size());

    for(const std::string& label : inputTagLabels_recoVertexCollections){

      const auto& inputTag = pset_recoVertexCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::VertexCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoVertexCollectionContainer_.emplace_back(RecoVertexCollectionContainer(label, inputTag.label(), this->consumes<reco::VertexCollection>(inputTag)));
    }
  }

  // reco::PFCandidateCollection
  v_recoPFCandidateCollectionContainer_.clear();

  if(iConfig.exists("recoPFCandidateCollections")){

    const edm::ParameterSet& pset_recoPFCandidateCollections = iConfig.getParameter<edm::ParameterSet>("recoPFCandidateCollections");

    const auto& inputTagLabels_recoPFCandidateCollections = pset_recoPFCandidateCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFCandidateCollectionContainer_.reserve(inputTagLabels_recoPFCandidateCollections.size());

    for(const std::string& label : inputTagLabels_recoPFCandidateCollections){

      const auto& inputTag = pset_recoPFCandidateCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFCandidateCollectionContainer_.emplace_back(RecoPFCandidateCollectionContainer(label, inputTag.label(), this->consumes<reco::PFCandidateCollection>(inputTag)));
      v_recoPFCandidateCollectionContainer_.back().orderByHighestPt(true);
    }
  }

  // pat::PackedCandidateCollection
  v_patPackedCandidateCollectionContainer_.clear();

  if(iConfig.exists("patPackedCandidateCollections")){

    const edm::ParameterSet& pset_patPackedCandidateCollections = iConfig.getParameter<edm::ParameterSet>("patPackedCandidateCollections");

    const auto& inputTagLabels_patPackedCandidateCollections = pset_patPackedCandidateCollections.getParameterNamesForType<edm::InputTag>();

    v_patPackedCandidateCollectionContainer_.reserve(inputTagLabels_patPackedCandidateCollections.size());

    for(const std::string& label : inputTagLabels_patPackedCandidateCollections){

      const auto& inputTag = pset_patPackedCandidateCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::PackedCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patPackedCandidateCollectionContainer_.emplace_back(PATPackedCandidateCollectionContainer(label, inputTag.label(), this->consumes<pat::PackedCandidateCollection>(inputTag)));
      v_patPackedCandidateCollectionContainer_.back().orderByHighestPt(true);
    }
  }

  // reco::PFJetCollection
  v_recoPFJetCollectionContainer_.clear();

  if(iConfig.exists("recoPFJetCollections")){

    const edm::ParameterSet& pset_recoPFJetCollections = iConfig.getParameter<edm::ParameterSet>("recoPFJetCollections");

    const auto& inputTagLabels_recoPFJetCollections = pset_recoPFJetCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFJetCollectionContainer_.reserve(inputTagLabels_recoPFJetCollections.size());

    for(const std::string& label : inputTagLabels_recoPFJetCollections){

      const auto& inputTag = pset_recoPFJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFJetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFJetCollectionContainer_.emplace_back(RecoPFJetCollectionContainer(label, inputTag.label(), this->consumes<reco::PFJetCollection>(inputTag)));
    }
  }

  // pat::JetCollection
  v_patJetCollectionContainer_.clear();

  if(iConfig.exists("patJetCollections")){

    const edm::ParameterSet& pset_patJetCollections = iConfig.getParameter<edm::ParameterSet>("patJetCollections");

    const auto& inputTagLabels_patJetCollections = pset_patJetCollections.getParameterNamesForType<edm::InputTag>();

    v_patJetCollectionContainer_.reserve(inputTagLabels_patJetCollections.size());

    for(const std::string& label : inputTagLabels_patJetCollections){

      const auto& inputTag = pset_patJetCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::JetCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patJetCollectionContainer_.emplace_back(PATJetCollectionContainer(label, inputTag.label(), this->consumes<pat::JetCollection>(inputTag)));
    }
  }

  // reco::CaloMETCollection
  v_recoCaloMETCollectionContainer_.clear();

  if(iConfig.exists("recoCaloMETCollections")){

    const edm::ParameterSet& pset_recoCaloMETCollections = iConfig.getParameter<edm::ParameterSet>("recoCaloMETCollections");

    const auto& inputTagLabels_recoCaloMETCollections = pset_recoCaloMETCollections.getParameterNamesForType<edm::InputTag>();

    v_recoCaloMETCollectionContainer_.reserve(inputTagLabels_recoCaloMETCollections.size());

    for(const std::string& label : inputTagLabels_recoCaloMETCollections){

      const auto& inputTag = pset_recoCaloMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::CaloMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoCaloMETCollectionContainer_.emplace_back(RecoCaloMETCollectionContainer(label, inputTag.label(), this->consumes<reco::CaloMETCollection>(inputTag)));
    }
  }

  // reco::PFMETCollection
  v_recoPFMETCollectionContainer_.clear();

  if(iConfig.exists("recoPFMETCollections")){

    const edm::ParameterSet& pset_recoPFMETCollections = iConfig.getParameter<edm::ParameterSet>("recoPFMETCollections");

    const auto& inputTagLabels_recoPFMETCollections = pset_recoPFMETCollections.getParameterNamesForType<edm::InputTag>();

    v_recoPFMETCollectionContainer_.reserve(inputTagLabels_recoPFMETCollections.size());

    for(const std::string& label : inputTagLabels_recoPFMETCollections){

      const auto& inputTag = pset_recoPFMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding reco::PFMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFMETCollectionContainer_.emplace_back(RecoPFMETCollectionContainer(label, inputTag.label(), this->consumes<reco::PFMETCollection>(inputTag)));
    }
  }

  // pat::METCollection
  v_patMETCollectionContainer_.clear();

  if(iConfig.exists("patMETCollections")){

    const edm::ParameterSet& pset_patMETCollections = iConfig.getParameter<edm::ParameterSet>("patMETCollections");

    const auto& inputTagLabels_patMETCollections = pset_patMETCollections.getParameterNamesForType<edm::InputTag>();

    v_patMETCollectionContainer_.reserve(inputTagLabels_patMETCollections.size());

    for(const std::string& label : inputTagLabels_patMETCollections){

      const auto& inputTag = pset_patMETCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::METCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patMETCollectionContainer_.emplace_back(PATMETCollectionContainer(label, inputTag.label(), this->consumes<pat::METCollection>(inputTag)));
    }
  }

  // pat::MuonCollection
  v_patMuonCollectionContainer_.clear();

  if(iConfig.exists("patMuonCollections")){

    const edm::ParameterSet& pset_patMuonCollections = iConfig.getParameter<edm::ParameterSet>("patMuonCollections");

    const auto& inputTagLabels_patMuonCollections = pset_patMuonCollections.getParameterNamesForType<edm::InputTag>();

    v_patMuonCollectionContainer_.reserve(inputTagLabels_patMuonCollections.size());

    for(const std::string& label : inputTagLabels_patMuonCollections){

      const auto& inputTag = pset_patMuonCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::MuonCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patMuonCollectionContainer_.emplace_back(PATMuonCollectionContainer(label, inputTag.label(), this->consumes<pat::MuonCollection>(inputTag)));
      v_patMuonCollectionContainer_.back().orderByHighestPt(true);
    }
  }

  // pat::ElectronCollection
  v_patElectronCollectionContainer_.clear();

  if(iConfig.exists("patElectronCollections")){

    const edm::ParameterSet& pset_patElectronCollections = iConfig.getParameter<edm::ParameterSet>("patElectronCollections");

    const auto& inputTagLabels_patElectronCollections = pset_patElectronCollections.getParameterNamesForType<edm::InputTag>();

    v_patElectronCollectionContainer_.reserve(inputTagLabels_patElectronCollections.size());

    for(const std::string& label : inputTagLabels_patElectronCollections){

      const auto& inputTag = pset_patElectronCollections.getParameter<edm::InputTag>(label);

      LogDebug("JMETriggerNTuple::JMETriggerNTuple") << "adding pat::ElectronCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patElectronCollectionContainer_.emplace_back(PATElectronCollectionContainer(label, inputTag.label(), this->consumes<pat::ElectronCollection>(inputTag)));
      v_patElectronCollectionContainer_.back().orderByHighestPt(true);
    }
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

    const auto& triggerNames = iEvent.triggerNames(*triggerResults_handle).triggerNames();

    triggerResultsContainer_ptr_->fill(*triggerResults_handle, triggerNames);
  }

  // exit method for events that do not pass the logical OR of the specified HLT paths (if any)
  if(HLTPathsFilterOR_.size() > 0){

    bool keep_event(false);

    for(const auto& triggerEntry_i : triggerResultsContainer_ptr_->entries()){

      if(std::find(HLTPathsFilterOR_.begin(), HLTPathsFilterOR_.end(), triggerEntry_i.name) != HLTPathsFilterOR_.end()){

        if(triggerEntry_i.accept){

          LogDebug("JMETriggerNTuple::analyze") << "event fired HLT path \"" << triggerEntry_i.name << "\", output collections will be saved to TTree";

          keep_event = true;
          break;
        }
      }
    }

    // if none of the specified HLT paths is fired, return
    if(not keep_event){

      return;
    }
  }

  // fill recoVertexCollectionContainers
  for(auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_){

    edm::Handle<reco::VertexCollection> i_handle;
    iEvent.getByToken(recoVertexCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoVertexCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoVertexCollectionContainer_i.name() << "_*\")";

      recoVertexCollectionContainer_i.clear();
    }
    else {

      recoVertexCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFCandidateCollectionContainers
  for(auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_){

    edm::Handle<reco::PFCandidateCollection> i_handle;
    iEvent.getByToken(recoPFCandidateCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFCandidateCollectionContainer_i.name() << "_*\")";

      recoPFCandidateCollectionContainer_i.clear();
    }
    else {

      recoPFCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patPackedCandidateCollectionContainers
  for(auto& patPackedCandidateCollectionContainer_i : v_patPackedCandidateCollectionContainer_){

    edm::Handle<pat::PackedCandidateCollection> i_handle;
    iEvent.getByToken(patPackedCandidateCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patPackedCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patPackedCandidateCollectionContainer_i.name() << "_*\")";

      patPackedCandidateCollectionContainer_i.clear();
    }
    else {

      patPackedCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFJetCollectionContainers
  for(auto& recoPFJetCollectionContainer_i : v_recoPFJetCollectionContainer_){

    edm::Handle<reco::PFJetCollection> i_handle;
    iEvent.getByToken(recoPFJetCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFJetCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFJetCollectionContainer_i.name() << "_*\")";

      recoPFJetCollectionContainer_i.clear();
    }
    else {

      recoPFJetCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patJetCollectionContainers
  for(auto& patJetCollectionContainer_i : v_patJetCollectionContainer_){

    edm::Handle<pat::JetCollection> i_handle;
    iEvent.getByToken(patJetCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patJetCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patJetCollectionContainer_i.name() << "_*\")";

      patJetCollectionContainer_i.clear();
    }
    else {

      patJetCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoCaloMETCollectionContainers
  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    edm::Handle<reco::CaloMETCollection> i_handle;
    iEvent.getByToken(recoCaloMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: " << recoCaloMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoCaloMETCollectionContainer_i.name() << "_*\")";

      recoCaloMETCollectionContainer_i.clear();
    }
    else {

      recoCaloMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoPFMETCollectionContainers
  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    edm::Handle<reco::PFMETCollection> i_handle;
    iEvent.getByToken(recoPFMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << recoPFMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFMETCollectionContainer_i.name() << "_*\")";

      recoPFMETCollectionContainer_i.clear();
    }
    else {

      recoPFMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patMETCollectionContainers
  for(auto& patMETCollectionContainer_i : v_patMETCollectionContainer_){

    edm::Handle<pat::METCollection> i_handle;
    iEvent.getByToken(patMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patMETCollectionContainer_i.name() << "_*\")";

      patMETCollectionContainer_i.clear();
    }
    else {

      patMETCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patMuonCollectionContainers
  for(auto& patMuonCollectionContainer_i : v_patMuonCollectionContainer_){

    edm::Handle<pat::MuonCollection> i_handle;
    iEvent.getByToken(patMuonCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patMuonCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patMuonCollectionContainer_i.name() << "_*\")";

      patMuonCollectionContainer_i.clear();
    }
    else {

      patMuonCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill patElectronCollectionContainers
  for(auto& patElectronCollectionContainer_i : v_patElectronCollectionContainer_){

    edm::Handle<pat::ElectronCollection> i_handle;
    iEvent.getByToken(patElectronCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("JMETriggerNTuple::analyze")
        << "invalid handle for input collection: \"" << patElectronCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patElectronCollectionContainer_i.name() << "_*\")";

      patElectronCollectionContainer_i.clear();
    }
    else {

      patElectronCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill TTree
  ttree_->Fill();
}

void JMETriggerNTuple::beginJob(){

  edm::Service<TFileService> fileService;

  if(not fileService){

    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fileService->make<TTree>(TTreeName_.c_str(), TTreeName_.c_str());

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

  for(auto& recoPFJetCollectionContainer_i : v_recoPFJetCollectionContainer_){

    this->addBranch(recoPFJetCollectionContainer_i.name()+"_pt", &recoPFJetCollectionContainer_i.vec_pt());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_eta", &recoPFJetCollectionContainer_i.vec_eta());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_phi", &recoPFJetCollectionContainer_i.vec_phi());
    this->addBranch(recoPFJetCollectionContainer_i.name()+"_mass", &recoPFJetCollectionContainer_i.vec_mass());
  }

  for(auto& patJetCollectionContainer_i : v_patJetCollectionContainer_){

    this->addBranch(patJetCollectionContainer_i.name()+"_pt", &patJetCollectionContainer_i.vec_pt());
    this->addBranch(patJetCollectionContainer_i.name()+"_eta", &patJetCollectionContainer_i.vec_eta());
    this->addBranch(patJetCollectionContainer_i.name()+"_phi", &patJetCollectionContainer_i.vec_phi());
    this->addBranch(patJetCollectionContainer_i.name()+"_mass", &patJetCollectionContainer_i.vec_mass());
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
}

template <typename... Args>
void JMETriggerNTuple::addBranch(const std::string& branch_name, Args... args){

  if(ttree_){

    if(std::find(outputBranchesToBeDropped_.begin(), outputBranchesToBeDropped_.end(), branch_name) == outputBranchesToBeDropped_.end()){

      ttree_->Branch(branch_name.c_str(), args...);
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

void JMETriggerNTuple::fillDescriptions(edm::ConfigurationDescriptions& descriptions){

  edm::ParameterSetDescription desc;
  desc.setUnknown();
//  desc.add<std::string>("TTreeName", "TTreeName")->setComment("Name of TTree");
//  desc.add<std::vector<std::string> >("HLTPathsFilterOR")->setComment("List of HLT paths (without version) used in OR to select events in the output TTree");
//  desc.add<std::vector<std::string> >("outputBranchesToBeDropped")->setComment("Names of branches not to be included in the output TTree");
//  desc.add<edm::InputTag>("TriggerResults", edm::InputTag("TriggerResults"))->setComment("edm::InputTag for edm::TriggerResults");
//  desc.add<std::vector<std::string> >("HLTPathsWithoutVersion")->setComment("List of HLT paths (without version) to be saved in the output TTree");

//  edm::ParameterSetDescription recoCaloMETCollections;
//  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("jmeTriggerNTuple", desc);
}

DEFINE_FWK_MODULE(JMETriggerNTuple);
