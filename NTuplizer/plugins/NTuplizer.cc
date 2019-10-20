#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDAnalyzer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/ServiceRegistry/interface/Service.h>
#include <CommonTools/UtilAlgos/interface/TFileService.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <JMETriggerAnalysis/NTuplizer/interface/TriggerResultsContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/PATPackedCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFMETCollectionContainer.h>

#include <string>
#include <vector>
#include <memory>
#include <algorithm>

#include <TTree.h>

class NTuplizer : public edm::EDAnalyzer {

 public:
  explicit NTuplizer(const edm::ParameterSet&);
  virtual ~NTuplizer() {}

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
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;

//!! muons
//!! electrons
//!! offline PF
//!! online jets
//!! offline jets
};

NTuplizer::NTuplizer(const edm::ParameterSet& iConfig)
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

      LogDebug("NTuplizer::NTuplizer") << "adding reco::VertexCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

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

      LogDebug("NTuplizer::NTuplizer") << "adding reco::PFCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFCandidateCollectionContainer_.emplace_back(RecoPFCandidateCollectionContainer(label, inputTag.label(), this->consumes<reco::PFCandidateCollection>(inputTag)));
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

      LogDebug("NTuplizer::NTuplizer") << "adding pat::PackedCandidateCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_patPackedCandidateCollectionContainer_.emplace_back(PATPackedCandidateCollectionContainer(label, inputTag.label(), this->consumes<pat::PackedCandidateCollection>(inputTag)));
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

      LogDebug("NTuplizer::NTuplizer") << "adding reco::CaloMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

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

      LogDebug("NTuplizer::NTuplizer") << "adding reco::PFMETCollection \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_recoPFMETCollectionContainer_.emplace_back(RecoPFMETCollectionContainer(label, inputTag.label(), this->consumes<reco::PFMETCollection>(inputTag)));
    }
  }
}

void NTuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  run_ = iEvent.id().run();
  luminosityBlock_ = iEvent.id().luminosityBlock();
  event_ = iEvent.id().event();

  // fill TriggerResultsContainer
  edm::Handle<edm::TriggerResults> triggerResults_handle;
  iEvent.getByToken(triggerResultsContainer_ptr_->token(), triggerResults_handle);

  if(not triggerResults_handle.isValid()){

    edm::LogWarning("NTuplizer::analyze")
      << "invalid handle for input collection: \"" << triggerResultsContainer_ptr_->inputTagLabel() << "\" (NTuple branches for HLT paths)";
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

          LogDebug("NTuplizer::analyze") << "event fired HLT path \"" << triggerEntry_i.name << "\", output collections will be saved to TTree";

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

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoVertexCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoVertexCollectionContainer_i.name() << "_*\")";
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

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoPFCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFCandidateCollectionContainer_i.name() << "_*\")";
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

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << patPackedCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << patPackedCandidateCollectionContainer_i.name() << "_*\")";
    }
    else {

      patPackedCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  // fill recoCaloMETCollectionContainers
  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    edm::Handle<reco::CaloMETCollection> i_handle;
    iEvent.getByToken(recoCaloMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: " << recoCaloMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoCaloMETCollectionContainer_i.name() << "_*\")";
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

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoPFMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFMETCollectionContainer_i.fill(*i_handle);

//!!      for(uint idx=0; idx<recoPFMETCollectionContainer_i.vec_pt().size(); ++idx){
//!!
//!!
//!!<< " PHI=" << i_handle->at(idx).phi()
//!!<< " VX=" << i_handle->at(idx).vx()
//!!<< " VY=" << i_handle->at(idx).vy()
//!!<< " VZ=" << i_handle->at(idx).vz();
//!!      }

    }
  }

  // fill TTree
  ttree_->Fill();
}

void NTuplizer::beginJob(){

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

  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_pt", &recoCaloMETCollectionContainer_i.vec_pt());
    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_phi", &recoCaloMETCollectionContainer_i.vec_phi());
    this->addBranch(recoCaloMETCollectionContainer_i.name()+"_sumEt", &recoCaloMETCollectionContainer_i.vec_sumEt());
  }

  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    this->addBranch(recoPFMETCollectionContainer_i.name()+"_pt", &recoPFMETCollectionContainer_i.vec_pt());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_phi", &recoPFMETCollectionContainer_i.vec_phi());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_sumEt", &recoPFMETCollectionContainer_i.vec_sumEt());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_photonEtFraction", &recoPFMETCollectionContainer_i.vec_photonEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_neutralHadronEtFraction", &recoPFMETCollectionContainer_i.vec_neutralHadronEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_electronEtFraction", &recoPFMETCollectionContainer_i.vec_electronEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_chargedHadronEtFraction", &recoPFMETCollectionContainer_i.vec_chargedHadronEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_muonEtFraction", &recoPFMETCollectionContainer_i.vec_muonEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_HFHadronEtFraction", &recoPFMETCollectionContainer_i.vec_HFHadronEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name()+"_HFEMEtFraction", &recoPFMETCollectionContainer_i.vec_HFEMEtFraction());
  }
}

template <typename... Args>
void NTuplizer::addBranch(const std::string& branch_name, Args... args){

  if(ttree_){

    if(std::find(outputBranchesToBeDropped_.begin(), outputBranchesToBeDropped_.end(), branch_name) == outputBranchesToBeDropped_.end()){

      ttree_->Branch(branch_name.c_str(), args...);
    }
    else {

      edm::LogInfo("NTuplizer::addBranch") << "output branch \"" << branch_name
        << "\" will not be created (string appears in data member \"outputBranchesToBeDropped\")";
    }
  }
  else {

    edm::LogWarning("NTuplizer::addBranch") << "pointer to TTree is null, output branch \"" << branch_name << "\" will not be created";
  }
}

void NTuplizer::fillDescriptions(edm::ConfigurationDescriptions& descriptions){

  edm::ParameterSetDescription desc;
  desc.setUnknown();
//  desc.add<std::string>("TTreeName", "TTreeName")->setComment("Name of TTree");
//  desc.add<std::vector<std::string> >("HLTPathsFilterOR")->setComment("List of HLT paths (without version) used in OR to select events in the output TTree");
//  desc.add<std::vector<std::string> >("outputBranchesToBeDropped")->setComment("Names of branches not to be included in the output TTree");
//  desc.add<edm::InputTag>("TriggerResults", edm::InputTag("TriggerResults"))->setComment("edm::InputTag for edm::TriggerResults");
//  desc.add<std::vector<std::string> >("HLTPathsWithoutVersion")->setComment("List of HLT paths (without version) to be saved in the output TTree");

//  edm::ParameterSetDescription recoCaloMETCollections;
//  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("jmeTriggerNTuplizer", desc);
}

DEFINE_FWK_MODULE(NTuplizer);
