#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDAnalyzer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/ServiceRegistry/interface/Service.h>
#include <CommonTools/UtilAlgos/interface/TFileService.h>
#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include <SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h>
#include <SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <DataFormats/Common/interface/EDCollection.h>
#include <DataFormats/Candidate/interface/Candidate.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include <DataFormats/PatCandidates/interface/Jet.h>
#include <DataFormats/PatCandidates/interface/MET.h>

#include <JMETriggerAnalysis/NTuplizer/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFCandidateCollectionContainer.h>
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

  const std::string TTreeName_;

  TTree* ttree_ = nullptr;

  unsigned int run_;
  unsigned int luminosityBlock_;
  unsigned long long event_;

//!! triggers

//!! muons
//!! electrons
//!! offline PF
//!! online jets
//!! offline jets

  std::vector<RecoVertexCollectionContainer> v_recoVertexCollectionContainer_;
  std::vector<RecoPFCandidateCollectionContainer> v_recoPFCandidateCollectionContainer_;
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;
};

NTuplizer::NTuplizer(const edm::ParameterSet& iConfig) : TTreeName_("Events") {

//!!  src_hlt_        = consumes<edm::TriggerResults>            (edm::InputTag("TriggerResults::HLT2"));

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

  for(auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_){

    edm::Handle<reco::VertexCollection> i_handle;
    iEvent.getByToken(recoVertexCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoVertexCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoVertexCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoVertexCollectionContainer_i.clear();
      recoVertexCollectionContainer_i.fill(*i_handle);
    }
  }

  for(auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_){

    edm::Handle<reco::PFCandidateCollection> i_handle;
    iEvent.getByToken(recoPFCandidateCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoPFCandidateCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFCandidateCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFCandidateCollectionContainer_i.clear();
      recoPFCandidateCollectionContainer_i.fill(*i_handle);
    }
  }

  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    edm::Handle<reco::CaloMETCollection> i_handle;
    iEvent.getByToken(recoCaloMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: " << recoCaloMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoCaloMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoCaloMETCollectionContainer_i.clear();
      recoCaloMETCollectionContainer_i.fill(*i_handle);
    }
  }

  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    edm::Handle<reco::PFMETCollection> i_handle;
    iEvent.getByToken(recoPFMETCollectionContainer_i.token(), i_handle);

    if(not i_handle.isValid()){

      edm::LogWarning("NTuplizer::analyze")
        << "invalid handle for input collection: \"" << recoPFMETCollectionContainer_i.inputTagLabel()
        << "\" (NTuple branches: \"" << recoPFMETCollectionContainer_i.name() << "_*\")";
    }
    else {

      recoPFMETCollectionContainer_i.clear();
      recoPFMETCollectionContainer_i.fill(*i_handle);

//!!      for(uint idx=0; idx<recoPFMETCollectionContainer_i.vec_pt().size(); ++idx){
//!!
//!!
//!!	<< " PHI=" << i_handle->at(idx).phi()
//!!	<< " VX=" << i_handle->at(idx).vx()
//!!	<< " VY=" << i_handle->at(idx).vy()
//!!	<< " VZ=" << i_handle->at(idx).vz();
//!!      }

    }
  }

  // fill TTree
  ttree_->Fill();
}

//!!void NTuplizer::fill_HLT(llj::HLT& hlt_, const edm::TriggerResults& trg_, const edm::Event& evt_) const {
//!!
//!!  const std::vector<std::string>& trgNames = evt_.triggerNames(trg_).triggerNames();
//!!
//!!  for(unsigned int i=0; i<trg_.size(); ++i){
//!!    if(trgNames.at(i).find(std::string(#PATH)+"_v") != std::string::npos) hlt_.PATH = trg_.at(i).accept();
//!!  }
//!!
//!!  return;
//!!}

void NTuplizer::beginJob(){

  edm::Service<TFileService> fileService;

  if(not fileService){

    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fileService->make<TTree>(TTreeName_.c_str(), TTreeName_.c_str());

  if(not ttree_){

    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }

  ttree_->Branch("run", &run_);
  ttree_->Branch("luminosityBlock", &luminosityBlock_);
  ttree_->Branch("event", &event_);

  for(auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_){

    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_tracksSize").c_str(), &recoVertexCollectionContainer_i.vec_tracksSize());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_isFake").c_str(), &recoVertexCollectionContainer_i.vec_isFake());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_chi2").c_str(), &recoVertexCollectionContainer_i.vec_chi2());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_ndof").c_str(), &recoVertexCollectionContainer_i.vec_ndof());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_x").c_str(), &recoVertexCollectionContainer_i.vec_x());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_y").c_str(), &recoVertexCollectionContainer_i.vec_y());
    ttree_->Branch((recoVertexCollectionContainer_i.name()+"_z").c_str(), &recoVertexCollectionContainer_i.vec_z());
  }

  for(auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_){

    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_pdgId").c_str(), &recoPFCandidateCollectionContainer_i.vec_pdgId());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_pt").c_str(), &recoPFCandidateCollectionContainer_i.vec_pt());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_eta").c_str(), &recoPFCandidateCollectionContainer_i.vec_eta());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_phi").c_str(), &recoPFCandidateCollectionContainer_i.vec_phi());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_mass").c_str(), &recoPFCandidateCollectionContainer_i.vec_mass());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_vx").c_str(), &recoPFCandidateCollectionContainer_i.vec_vx());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_vy").c_str(), &recoPFCandidateCollectionContainer_i.vec_vy());
    ttree_->Branch((recoPFCandidateCollectionContainer_i.name()+"_vz").c_str(), &recoPFCandidateCollectionContainer_i.vec_vz());
  }

  for(auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_){

    ttree_->Branch((recoCaloMETCollectionContainer_i.name()+"_pt").c_str(), &recoCaloMETCollectionContainer_i.vec_pt());
    ttree_->Branch((recoCaloMETCollectionContainer_i.name()+"_phi").c_str(), &recoCaloMETCollectionContainer_i.vec_phi());
    ttree_->Branch((recoCaloMETCollectionContainer_i.name()+"_sumEt").c_str(), &recoCaloMETCollectionContainer_i.vec_sumEt());
  }

  for(auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_){

    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_pt").c_str(), &recoPFMETCollectionContainer_i.vec_pt());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_phi").c_str(), &recoPFMETCollectionContainer_i.vec_phi());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_sumEt").c_str(), &recoPFMETCollectionContainer_i.vec_sumEt());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_photonEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_photonEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_neutralHadronEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_neutralHadronEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_electronEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_electronEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_chargedHadronEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_chargedHadronEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_muonEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_muonEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_HFHadronEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_HFHadronEtFraction());
    ttree_->Branch((recoPFMETCollectionContainer_i.name()+"_HFEMEtFraction").c_str(), &recoPFMETCollectionContainer_i.vec_HFEMEtFraction());
  }
}

void NTuplizer::fillDescriptions(edm::ConfigurationDescriptions& descriptions){

  edm::ParameterSetDescription desc;
//  desc.add<edm::InputTag>("hltMet", edm::InputTag("hltMet", "", "HLT2"))->setComment("HLT collection \"hltMet\"");
  desc.setUnknown();
//  edm::ParameterSetDescription recoCaloMETCollections;
//  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("jmeTriggerNTuplizer", desc);
}

DEFINE_FWK_MODULE(NTuplizer);
