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

  TTree* ttree_ = nullptr;

  unsigned int run_;
  unsigned int luminosityBlock_;
  unsigned long long event_;

//!! triggers

//!! muons
//!! electrons
//!! online PF
//!! offline PF
//!! online jets
//!! offline jets

  std::vector<RecoPFCandidateCollectionContainer> v_recoPFCandidateCollectionContainer_;
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;
};

NTuplizer::NTuplizer(const edm::ParameterSet& iConfig){

//!!  src_hlt_        = consumes<edm::TriggerResults>            (edm::InputTag("TriggerResults::HLT2"));

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

//!!  /* HIGH LEVEL TRIGGER ------------------------------------------ */
//!!
//!!  edm::Handle<edm::TriggerResults > hltResults;
//!!  iEvent.getByToken(src_hlt_, hltResults);
//!!
//!!  fill_HLT(HLT, *hltResults, iEvent);
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* PRIMARY VERTEX ---------------------------------------------- */
//!!
//!!  edm::Handle<edm::View<reco::Vertex> > recoVtxs;
//!!  iEvent.getByToken(src_pvtx_, recoVtxs);
//!!
//!!  const int pvN(recoVtxs->size());
//!!
//!!  if(pvN == 0){
//!!
//!!    throw cms::Exception("InputError") << "@@@ NTuplizer::analyze -- empty 'vertex_src' collection";
//!!  }
//!!
//!!  const reco::Vertex& vertex = *recoVtxs->begin();
//!!
//!!  fill_PVertex(PVTX, vertex);
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* MUON -------------------------------------------------------- */
//!!
//!!  edm::Handle<edm::View<pat::Muon> > patMuons;
//!!  iEvent.getByToken(src_muon_, patMuons);
//!!
//!!  MUO.reserve(patMuons->size());
//!!  for(edm::View<pat::Muon>::const_iterator iMuo = patMuons->begin();
//!!      iMuo != patMuons->end(); ++iMuo){
//!!
//!!    MUO.emplace_back(llj::Muon());
//!!    fill_Muon(MUO.back(), *iMuo);
//!!  }
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* ELECTRON ---------------------------------------------------- */
//!!
//!!  edm::Handle<edm::View<pat::Electron> > patElecs;
//!!  iEvent.getByToken(src_elec_, patElecs);
//!!
//!!  ELE.reserve(patElecs->size());
//!!  for(edm::View<pat::Electron>::const_iterator iEle = patElecs->begin();
//!!      iEle != patElecs->end(); ++iEle){
//!!
//!!    ELE.emplace_back(llj::Electron());
//!!    fill_Electron(ELE.back(), *iEle);
//!!  }
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* JET --------------------------------------------------------- */
//!!
//!!  /* AK04 jet */
//!!  edm::Handle<edm::View<pat::Jet> > patJetsAK04;
//!!  iEvent.getByToken(src_jetAK04_,   patJetsAK04);
//!!
//!!  JET_AK04.reserve(patJetsAK04->size());
//!!  for(edm::View<pat::Jet>::const_iterator iJetAK04 = patJetsAK04->begin();
//!!       iJetAK04 != patJetsAK04->end();  ++iJetAK04){
//!!
//!!    JET_AK04.emplace_back(llj::Jet());
//!!    fill_Jet(JET_AK04.back(), *iJetAK04);
//!!  }
//!!
//!!  /* AK08 jet */
//!!  edm::Handle<edm::View<pat::Jet> > patJetsAK08;
//!!  iEvent.getByToken(src_jetAK08_,   patJetsAK08);
//!!
//!!  JET_AK08.reserve(patJetsAK08->size());
//!!  for(edm::View<pat::Jet>::const_iterator iJetAK08 = patJetsAK08->begin();
//!!       iJetAK08 != patJetsAK08->end();  ++iJetAK08){
//!!
//!!    JET_AK08.emplace_back(llj::MergedJet());
//!!    fill_MergedJet(JET_AK08.back(), *iJetAK08);
//!!  }
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* MET --------------------------------------------------------- */
//!!
//!!  /* Corrected */
//!!  edm::Handle<edm::View<pat::MET> > patMETsCorrd;
//!!  iEvent.getByToken(src_met_Corrd_, patMETsCorrd);
//!!
//!!  const pat::MET& patMET_Corrd = patMETsCorrd->front();
//!!
//!!  fill_MET(MET_Corrd, patMET_Corrd);
//!!
//!!  /* PUPPI */
//!!  edm::Handle<edm::View<pat::MET> > patMETsPUPPI;
//!!  iEvent.getByToken(src_met_PUPPI_, patMETsPUPPI);
//!!
//!!  const pat::MET& patMET_PUPPI = patMETsPUPPI->front();
//!!
//!!  fill_MET(MET_PUPPI, patMET_PUPPI);
//!!
//!!  /* ------------------------------------------------------------- */
//!!
//!!  /* EVENT INFO -------------------------------------------------- */
//!!
//!!  EVT.weight       = mc_weight;
//!!  EVT.XWGTUP       = xwgtup;
//!!  EVT.weightSYS    = weightSYS_vec;
//!!
//!!  EVT.pdf_scalePDF = pdf_scalePDF;
//!!  EVT.pdf_id1      = pdf_id1;
//!!  EVT.pdf_id2      = pdf_id2;
//!!  EVT.pdf_x1       = pdf_x1;
//!!  EVT.pdf_x2       = pdf_x2;
//!!  EVT.pdf_xPDF1    = pdf_xPDF1;
//!!  EVT.pdf_xPDF2    = pdf_xPDF2;
//!!
//!!  EVT.MCPileupBX0  = mcPU_bx0;
//!!
//!!  EVT.pvN          = pvN;
//!!
//!!  EVT.Event        = iEvent.id().event();
//!!  EVT.LumiBlock    = iEvent.id().luminosityBlock();
//!!  EVT.Run          = iEvent.id().run();
//!!
//!!  if(add_ecal_flags_){
//!!
//!!    edm::Handle<bool>     dupECALClusters;
//!!    iEvent.getByToken(src_dupECALClusters_, dupECALClusters);
//!!    EVT.dupECALClusters = *dupECALClusters;
//!!
//!!    edm::Handle<edm::EDCollection<DetId> >  hitsNotReplaced;
//!!    iEvent.getByToken(src_hitsNotReplaced_, hitsNotReplaced);
//!!    EVT.hitsNotReplaced = bool(hitsNotReplaced->size());
//!!  }

  // fill TTree
  ttree_->Fill();
}

//!!void NTuplizer::fill_HLT(llj::HLT& hlt_, const edm::TriggerResults& trg_, const edm::Event& evt_) const {
//!!
//!!  const std::vector<std::string>& trgNames = evt_.triggerNames(trg_).triggerNames();
//!!
//!!  for(unsigned int i=0; i<trg_.size(); ++i){
//!!#ifndef CP_HLT_
//!!#define CP_HLT_(PATH) \
//!!    if(trgNames.at(i).find(std::string(#PATH)+"_v") != std::string::npos) hlt_.PATH = trg_.at(i).accept();
//!!#endif
//!!
//!!#ifdef CP_HLT_
//!!       CP_HLT_(Mu45_eta2p1);
//!!       CP_HLT_(Mu40_eta2p1_PFJet200_PFJet50);
//!!       CP_HLT_(Mu50_IsoVVVL_PFHT400);
//!!       CP_HLT_(Mu50);
//!!       CP_HLT_(TkMu50);
//!!       CP_HLT_(IsoMu20);
//!!       CP_HLT_(IsoTkMu20);
//!!       CP_HLT_(IsoMu22);
//!!       CP_HLT_(IsoTkMu22); 
//!!       CP_HLT_(IsoMu24);  
//!!       CP_HLT_(IsoTkMu24); 
//!!       CP_HLT_(IsoMu27);  
//!!       CP_HLT_(IsoTkMu27);
//!!
//!!       CP_HLT_(Ele115_CaloIdVT_GsfTrkIdT);
//!!       CP_HLT_(Ele105_CaloIdVT_GsfTrkIdT);
//!!       CP_HLT_(Ele50_CaloIdVT_GsfTrkIdT_PFJet165);
//!!       CP_HLT_(Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50);
//!!       CP_HLT_(Ele50_IsoVVVL_PFHT400);
//!!       CP_HLT_(Ele22_eta2p1_WPLoose_Gsf);
//!!       CP_HLT_(Ele25_eta2p1_WPTight_Gsf);       
//!!       CP_HLT_(Ele27_WPTight_Gsf);       
//!!       CP_HLT_(Ele27_eta2p1_WPLoose_Gsf);
//!!       CP_HLT_(Ele27_eta2p1_WPTight_Gsf);
//!!       CP_HLT_(Ele30_WPTight_Gsf);    
//!!       CP_HLT_(Ele30_eta2p1_WPTight_Gsf);
//!!       CP_HLT_(Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ);
//!!       CP_HLT_(Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ);
//!!
//!!       CP_HLT_(Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ);
//!!       CP_HLT_(Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ);
//!!       CP_HLT_(Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL);
//!!       CP_HLT_(Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ);
//!!       CP_HLT_(Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL);
//!!
//!!       CP_HLT_(AK8PFJet400_TrimMass30);
//!!       CP_HLT_(PFMET170_NoiseCleaned);
//!!       CP_HLT_(PFMET120_BTagCSV_p067);
//!!       CP_HLT_(PFHT300_PFMET110);
//!!       CP_HLT_(PFHT800);
//!!       CP_HLT_(PFHT900);
//!!#endif
//!!  }
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_PVertex(llj::PVertex& pv_, const reco::Vertex& vtx_) const {
//!!
//!!  pv_.isFake = vtx_.isFake();
//!!  pv_.chi2   = vtx_.chi2();
//!!  pv_.nDOF   = vtx_.ndof();
//!!  pv_.vx     = vtx_.x();
//!!  pv_.vy     = vtx_.y();
//!!  pv_.vz     = vtx_.z();
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_Lepton(llj::Lepton& lepton_, const reco::Candidate& recoLepton_) const {
//!!
//!!  fill_Particle(lepton_, recoLepton_);
//!!
//!!  if(recoLepton_.isMuon() == recoLepton_.isElectron()){
//!!
//!!    throw cms::Exception("InputError") << "@@@ NTuplizer::fill_Lepton() -- Lepton Candidate flavor not univocally defined.";
//!!  }
//!!  else if(recoLepton_.isMuon()){
//!!
//!!    const pat::Muon* patLep = static_cast<const pat::Muon*>(&recoLepton_);
//!!    if(!patLep){
//!!
//!!      throw cms::Exception("LogicError") << "@@@ NTuplizer::fill_Lepton() -- Failed static_cast from reco::Candidate to pat::Muon";
//!!    }
//!!
//!!    lepton_.pdgID  = patLep->pdgId();
//!!    lepton_.charge = patLep->charge();
//!!    lepton_.vx     = patLep->vx();
//!!    lepton_.vy     = patLep->vy();
//!!    lepton_.vz     = patLep->vz();
//!!    lepton_.dxyPV  = patLep->hasUserFloat("dxyPV") ? patLep->userFloat("dxyPV") : -9999.;
//!!    lepton_.dzPV   = patLep->hasUserFloat ("dzPV") ? patLep->userFloat ("dzPV") : -9999.;
//!!    lepton_.dB     = patLep->dB();
//!!    lepton_.SIP3D  = patLep->hasUserFloat("SIP3D") ? patLep->userFloat("SIP3D") : -9999.;
//!!
//!!    lepton_.IDLooseHZZ  = patLep->hasUserInt("IDLooseHZZ") ? patLep->userInt("IDLooseHZZ") : -1;
//!!    lepton_.IDTightHZZ  = patLep->hasUserInt("IDTightHZZ") ? patLep->userInt("IDTightHZZ") : -1;
//!!
//!!    lepton_.pfIso       = patLep->hasUserFloat("PFIso")       ? patLep->userFloat("PFIso")       : -9999.;
//!!
//!!    lepton_.pfIsoR03    = patLep->hasUserFloat("PFIsoR03")    ? patLep->userFloat("PFIsoR03")    : -9999.;
//!!    lepton_.pfIsoR03_CH = patLep->hasUserFloat("PFIsoR03_CH") ? patLep->userFloat("PFIsoR03_CH") : -9999.;
//!!    lepton_.pfIsoR03_NH = patLep->hasUserFloat("PFIsoR03_NH") ? patLep->userFloat("PFIsoR03_NH") : -9999.;
//!!    lepton_.pfIsoR03_Ph = patLep->hasUserFloat("PFIsoR03_Ph") ? patLep->userFloat("PFIsoR03_Ph") : -9999.;
//!!    lepton_.pfIsoR03_PU = patLep->hasUserFloat("PFIsoR03_PU") ? patLep->userFloat("PFIsoR03_PU") : -9999.;
//!!    lepton_.pfIsoR03_rA = patLep->hasUserFloat("PFIsoR03_rA") ? patLep->userFloat("PFIsoR03_rA") : -9999.;
//!!
//!!    lepton_.pfIsoR04    = patLep->hasUserFloat("PFIsoR04")    ? patLep->userFloat("PFIsoR04")    : -9999.;
//!!    lepton_.pfIsoR04_CH = patLep->hasUserFloat("PFIsoR04_CH") ? patLep->userFloat("PFIsoR04_CH") : -9999.;
//!!    lepton_.pfIsoR04_NH = patLep->hasUserFloat("PFIsoR04_NH") ? patLep->userFloat("PFIsoR04_NH") : -9999.;
//!!    lepton_.pfIsoR04_Ph = patLep->hasUserFloat("PFIsoR04_Ph") ? patLep->userFloat("PFIsoR04_Ph") : -9999.;
//!!    lepton_.pfIsoR04_PU = patLep->hasUserFloat("PFIsoR04_PU") ? patLep->userFloat("PFIsoR04_PU") : -9999.;
//!!    lepton_.pfIsoR04_rA = patLep->hasUserFloat("PFIsoR04_rA") ? patLep->userFloat("PFIsoR04_rA") : -9999.;
//!!  }
//!!  else if(recoLepton_.isElectron()){
//!!
//!!    pat::Electron const* patLep = static_cast<pat::Electron const*>(&recoLepton_);
//!!    if(!patLep){
//!!
//!!      throw cms::Exception("LogicError") << "@@@ NTuplizer::fill_Lepton() -- Failed static_cast from reco::Candidate to pat::Electron";
//!!    }
//!!
//!!    lepton_.pdgID  = patLep->pdgId();
//!!    lepton_.charge = patLep->charge();
//!!    lepton_.vx     = patLep->vx();
//!!    lepton_.vy     = patLep->vy();
//!!    lepton_.vz     = patLep->vz();
//!!    lepton_.dxyPV  = patLep->hasUserFloat("dxyPV") ? patLep->userFloat("dxyPV") : -9999.;
//!!    lepton_.dzPV   = patLep->hasUserFloat ("dzPV") ? patLep->userFloat ("dzPV") : -9999.;
//!!    lepton_.dB     = patLep->dB();
//!!    lepton_.SIP3D  = patLep->hasUserFloat("SIP3D") ? patLep->userFloat("SIP3D") : -9999.;
//!!
//!!    lepton_.IDLooseHZZ  = patLep->hasUserInt("IDLooseHZZ") ? patLep->userInt("IDLooseHZZ") : -1;
//!!    lepton_.IDTightHZZ  = patLep->hasUserInt("IDTightHZZ") ? patLep->userInt("IDTightHZZ") : -1;
//!!
//!!    lepton_.pfIso       = patLep->hasUserFloat("PFIso")       ? patLep->userFloat("PFIso")       : -9999.;
//!!
//!!    lepton_.pfIsoR03    = patLep->hasUserFloat("PFIsoR03")    ? patLep->userFloat("PFIsoR03")    : -9999.;
//!!    lepton_.pfIsoR03_CH = patLep->hasUserFloat("PFIsoR03_CH") ? patLep->userFloat("PFIsoR03_CH") : -9999.;
//!!    lepton_.pfIsoR03_NH = patLep->hasUserFloat("PFIsoR03_NH") ? patLep->userFloat("PFIsoR03_NH") : -9999.;
//!!    lepton_.pfIsoR03_Ph = patLep->hasUserFloat("PFIsoR03_Ph") ? patLep->userFloat("PFIsoR03_Ph") : -9999.;
//!!    lepton_.pfIsoR03_PU = patLep->hasUserFloat("PFIsoR03_PU") ? patLep->userFloat("PFIsoR03_PU") : -9999.;
//!!    lepton_.pfIsoR03_rA = patLep->hasUserFloat("PFIsoR03_rA") ? patLep->userFloat("PFIsoR03_rA") : -9999.;
//!!
//!!    lepton_.pfIsoR04    = patLep->hasUserFloat("PFIsoR04")    ? patLep->userFloat("PFIsoR04")    : -9999.;
//!!    lepton_.pfIsoR04_CH = patLep->hasUserFloat("PFIsoR04_CH") ? patLep->userFloat("PFIsoR04_CH") : -9999.;
//!!    lepton_.pfIsoR04_NH = patLep->hasUserFloat("PFIsoR04_NH") ? patLep->userFloat("PFIsoR04_NH") : -9999.;
//!!    lepton_.pfIsoR04_Ph = patLep->hasUserFloat("PFIsoR04_Ph") ? patLep->userFloat("PFIsoR04_Ph") : -9999.;
//!!    lepton_.pfIsoR04_PU = patLep->hasUserFloat("PFIsoR04_PU") ? patLep->userFloat("PFIsoR04_PU") : -9999.;
//!!    lepton_.pfIsoR04_rA = patLep->hasUserFloat("PFIsoR04_rA") ? patLep->userFloat("PFIsoR04_rA") : -9999.;
//!!  }
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_Muon(llj::Muon& muon_, const pat::Muon& patMuon_) const {
//!!
//!!  fill_Lepton(muon_, patMuon_);
//!!
//!!  muon_.isGlobalMuon       = patMuon_.isGlobalMuon();
//!!  muon_.isTrackerMuon      = patMuon_.isTrackerMuon();
//!!  muon_.isPFMuon           = patMuon_.isPFMuon();
//!!
//!!  muon_.IDLoose            = patMuon_.hasUserInt("IDLoose")      ? patMuon_.userInt("IDLoose")      : false;
//!!  muon_.IDMedium           = patMuon_.hasUserInt("IDMedium")     ? patMuon_.userInt("IDMedium")     : false;
//!!  muon_.IDMedium2016       = patMuon_.hasUserInt("IDMedium2016") ? patMuon_.userInt("IDMedium2016") : false;
//!!  muon_.IDTight            = patMuon_.hasUserInt("IDTight")      ? patMuon_.userInt("IDTight")      : false;
//!!  muon_.IDSoft             = patMuon_.hasUserInt("IDSoft")       ? patMuon_.userInt("IDSoft")       : false;
//!!  muon_.IDHighPt           = patMuon_.hasUserInt("IDHighPt")     ? patMuon_.userInt("IDHighPt")     : false;
//!!
//!!  muon_.globalTrack_normalizedChi2              = patMuon_.globalTrack().isNonnull() ? patMuon_.globalTrack()->normalizedChi2() : -9999.;
//!!  muon_.globalTrack_numberOfValidMuonHits       = patMuon_.globalTrack().isNonnull() ? patMuon_.globalTrack()->hitPattern().numberOfValidMuonHits() : -1;
//!!  muon_.numberOfMatchedStations                 = patMuon_.numberOfMatchedStations();
//!!  muon_.innerTrack_trackerLayersWithMeasurement = patMuon_.innerTrack().isNonnull() ? patMuon_.innerTrack()->hitPattern().trackerLayersWithMeasurement() : -1;
//!!  muon_.innerTrack_numberOfValidPixelHits       = patMuon_.innerTrack().isNonnull() ? patMuon_.innerTrack()->hitPattern().numberOfValidPixelHits() : -1;
//!!  muon_.innerTrack_validFraction                = patMuon_.innerTrack().isNonnull() ? patMuon_.innerTrack()->validFraction() : -9999.;
//!!  muon_.combinedQuality_chi2LocalPosition       = patMuon_.combinedQuality().chi2LocalPosition;
//!!  muon_.combinedQuality_trkKink                 = patMuon_.combinedQuality().trkKink;
//!!  muon_.segmentCompatibility                    = muon::segmentCompatibility(patMuon_);
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_Electron(llj::Electron& elec_, const pat::Electron& patElec_) const {
//!!
//!!  fill_Lepton(elec_, patElec_);
//!!
//!!  elec_.etSC             = patElec_.superCluster()->energy() * sin(patElec_.superCluster()->position().theta());
//!!  elec_.etaSC            = patElec_.superCluster()->eta();
//!!  elec_.dEtaIn           = patElec_.deltaEtaSuperClusterTrackAtVtx();
//!!  elec_.dPhiIn           = patElec_.deltaPhiSuperClusterTrackAtVtx();
//!!  elec_.sigmaIEtaIEta    = patElec_.full5x5_sigmaIetaIeta();
//!!  elec_.HoverE           = patElec_.hadronicOverEm();
//!!  elec_.ecalEnergy       = patElec_.ecalEnergy();
//!!  elec_.eSCoverP         = patElec_.eSuperClusterOverP();
//!!  elec_.passConvVeto     = patElec_.passConversionVeto();
//!!  elec_.missingHits      = patElec_.gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
//!!
//!!  elec_.mvaGPu           = patElec_.hasUserFloat("mvaGPu") ? patElec_.userFloat("mvaGPu") : -9999.;
//!!  elec_.mvaHZZ           = patElec_.hasUserFloat("mvaHZZ") ? patElec_.userFloat("mvaHZZ") : -9999.;
//!!
//!!  elec_.IDcutBased       = patElec_.hasUserInt("IDcutBased")       ? patElec_.userInt("IDcutBased")       : -1;
//!!  elec_.IDcutBased_noIso = patElec_.hasUserInt("IDcutBased_noIso") ? patElec_.userInt("IDcutBased_noIso") : -1;
//!!  elec_.IDmvaGPu         = patElec_.hasUserInt("IDmvaGPu")         ? patElec_.userInt("IDmvaGPu")         : -1;
//!!  elec_.IDmvaHZZ         = patElec_.hasUserInt("IDmvaHZZ")         ? patElec_.userInt("IDmvaHZZ")         : -1;
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_Jet(llj::Jet& jet_, const pat::Jet& patJet_) const {
//!!
//!!  fill_Particle(jet_, patJet_);
//!!
//!!  jet_.isPFJet      = patJet_.isPFJet();
//!!  jet_.partonFlavor = patJet_.partonFlavour();
//!!  jet_.hadronFlavor = patJet_.hadronFlavour();
//!!
//!!  jet_.nDaughters   = int(patJet_.numberOfDaughters());
//!!
//!!  const float jec0 = patJet_.jecFactor("Uncorrected") ? 1./patJet_.jecFactor("Uncorrected") : 1.;
//!!
//!!  jet_.JEC    = PATJetUserFloat(patJet_, "JEC"   , jec0);
//!!  jet_.JECUnc = PATJetUserFloat(patJet_, "JECUnc", 0.);
//!!  jet_.JER    = PATJetUserFloat(patJet_, "JER"   , 1.);
//!!  jet_.JERup  = PATJetUserFloat(patJet_, "JERup" , 1.);
//!!  jet_.JERdn  = PATJetUserFloat(patJet_, "JERdn" , 1.);
//!!
//!!  jet_. chargedMultiplicity = patJet_.isPFJet() ? patJet_. chargedMultiplicity() : -9999;
//!!  jet_. neutralMultiplicity = patJet_.isPFJet() ? patJet_. neutralMultiplicity() : -9999;
//!!  jet_.    muonMultiplicity = patJet_.isPFJet() ? patJet_.    muonMultiplicity() : -9999;
//!!  jet_.electronMultiplicity = patJet_.isPFJet() ? patJet_.electronMultiplicity() : -9999;
//!!  jet_.  photonMultiplicity = patJet_.isPFJet() ? patJet_.  photonMultiplicity() : -9999;
//!!
//!!  jet_.CHef       = patJet_.isPFJet() ? patJet_.chargedHadronEnergyFraction() : -9999.;
//!!  jet_.CEef       = patJet_.isPFJet() ? patJet_.chargedEmEnergyFraction()     : -9999.;
//!!  jet_.NHef       = patJet_.isPFJet() ? patJet_.neutralHadronEnergyFraction() : -9999.;
//!!  jet_.NEef       = patJet_.isPFJet() ? patJet_.neutralEmEnergyFraction()     : -9999.;
//!!  jet_.MUef       = patJet_.isPFJet() ? patJet_.muonEnergyFraction()          : -9999.;
//!!
//!!  jet_.jetCharge  = patJet_.jetCharge();
//!!  jet_.puIDmva    = PATJetUserFloat(patJet_, "puIDmva", -9999.);
//!!
//!!  jet_.btagJP     = patJet_.bDiscriminator("pfJetProbabilityBJetTags");
//!!  jet_.btagCSV    = patJet_.bDiscriminator("pfCombinedSecondaryVertexV2BJetTags");
//!!  jet_.btagCSVIVF = patJet_.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
//!!  jet_.btagHBB    = patJet_.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags");
//!!
//!!  jet_.tau1       = PATJetUserFloat(patJet_, "tau1"  , -9999.);
//!!  jet_.tau2       = PATJetUserFloat(patJet_, "tau2"  , -9999.);
//!!  jet_.tau3       = PATJetUserFloat(patJet_, "tau3"  , -9999.);
//!!
//!!  jet_.ecf_1e2    = PATJetUserFloat(patJet_, "ECF1e2", -9999.);
//!!  jet_.ecf_1e3    = PATJetUserFloat(patJet_, "ECF1e3", -9999.);
//!!  jet_.ecf_2e3    = PATJetUserFloat(patJet_, "ECF2e3", -9999.);
//!!  jet_.ecf_3e3    = PATJetUserFloat(patJet_, "ECF3e3", -9999.);
//!!  jet_.ecf_1e4    = PATJetUserFloat(patJet_, "ECF1e4", -9999.);
//!!  jet_.ecf_2e4    = PATJetUserFloat(patJet_, "ECF2e4", -9999.);
//!!  jet_.ecf_6e4    = PATJetUserFloat(patJet_, "ECF6e4", -9999.);
//!!
//!!  const reco::GenJet* genjet_ref = patJet_.genJet();
//!!  if(genjet_ref){
//!!
//!!    jet_.genjet_pt  = genjet_ref->pt();
//!!    jet_.genjet_eta = genjet_ref->eta();
//!!    jet_.genjet_phi = genjet_ref->phi();
//!!    jet_.genjet_M   = genjet_ref->mass();
//!!  }
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_MergedJet(llj::MergedJet& mjet_, const pat::Jet& patMergedJet_) const {
//!!
//!!  fill_Jet(mjet_, patMergedJet_);
//!!
//!!  mjet_.Msoftdrop       = PATJetUserFloat(patMergedJet_, "Msoftdrop"          , -9999.);
//!!  mjet_.Mfiltered       = PATJetUserFloat(patMergedJet_, "Mfiltered"          , -9999.);
//!!  mjet_.Mpruned         = PATJetUserFloat(patMergedJet_, "Mpruned"            , -9999.);
//!!  mjet_.Mtrimmed        = PATJetUserFloat(patMergedJet_, "Mtrimmed"           , -9999.);
//!!
//!!  mjet_.puppi_pt        = PATJetUserFloat(patMergedJet_, "PuppiPt"            , -9999.);
//!!  mjet_.puppi_eta       = PATJetUserFloat(patMergedJet_, "PuppiEta"           , -9999.);
//!!  mjet_.puppi_phi       = PATJetUserFloat(patMergedJet_, "PuppiPhi"           , -9999.);
//!!  mjet_.puppi_M         = PATJetUserFloat(patMergedJet_, "PuppiMass"          , -9999.);
//!!  mjet_.puppi_Msoftdrop = PATJetUserFloat(patMergedJet_, "PuppiSoftDropMass"  , -9999.);
//!!  mjet_.puppi_tau1      = PATJetUserFloat(patMergedJet_, "PuppiTau1"          , -9999.);
//!!  mjet_.puppi_tau2      = PATJetUserFloat(patMergedJet_, "PuppiTau2"          , -9999.);
//!!  mjet_.puppi_tau3      = PATJetUserFloat(patMergedJet_, "PuppiTau3"          , -9999.);
//!!  mjet_.puppi_ecf_1e2   = PATJetUserFloat(patMergedJet_, "PuppiECF1e2"        , -9999.);
//!!  mjet_.puppi_ecf_1e3   = PATJetUserFloat(patMergedJet_, "PuppiECF1e3"        , -9999.);
//!!  mjet_.puppi_ecf_2e3   = PATJetUserFloat(patMergedJet_, "PuppiECF2e3"        , -9999.);
//!!  mjet_.puppi_ecf_3e3   = PATJetUserFloat(patMergedJet_, "PuppiECF3e3"        , -9999.);
//!!  mjet_.puppi_ecf_1e4   = PATJetUserFloat(patMergedJet_, "PuppiECF1e4"        , -9999.);
//!!  mjet_.puppi_ecf_2e4   = PATJetUserFloat(patMergedJet_, "PuppiECF2e4"        , -9999.);
//!!  mjet_.puppi_ecf_6e4   = PATJetUserFloat(patMergedJet_, "PuppiECF6e4"        , -9999.);
//!!
//!!  mjet_.SD_tau1         = PATJetUserFloat(patMergedJet_, "SoftDropTau1"       , -9999.);
//!!  mjet_.SD_tau2         = PATJetUserFloat(patMergedJet_, "SoftDropTau2"       , -9999.);
//!!  mjet_.SD_tau3         = PATJetUserFloat(patMergedJet_, "SoftDropTau3"       , -9999.);
//!!  mjet_.SD_ecf_1e2      = PATJetUserFloat(patMergedJet_, "SoftDropECF1e2"     , -9999.);
//!!  mjet_.SD_ecf_1e3      = PATJetUserFloat(patMergedJet_, "SoftDropECF1e3"     , -9999.);
//!!  mjet_.SD_ecf_2e3      = PATJetUserFloat(patMergedJet_, "SoftDropECF2e3"     , -9999.);
//!!  mjet_.SD_ecf_3e3      = PATJetUserFloat(patMergedJet_, "SoftDropECF3e3"     , -9999.);
//!!  mjet_.SD_ecf_1e4      = PATJetUserFloat(patMergedJet_, "SoftDropECF1e4"     , -9999.);
//!!  mjet_.SD_ecf_2e4      = PATJetUserFloat(patMergedJet_, "SoftDropECF2e4"     , -9999.);
//!!  mjet_.SD_ecf_6e4      = PATJetUserFloat(patMergedJet_, "SoftDropECF6e4"     , -9999.);
//!!
//!!  mjet_.puppiSD_tau1    = PATJetUserFloat(patMergedJet_, "PuppiSoftDropTau1"  , -9999.);
//!!  mjet_.puppiSD_tau2    = PATJetUserFloat(patMergedJet_, "PuppiSoftDropTau2"  , -9999.);
//!!  mjet_.puppiSD_tau3    = PATJetUserFloat(patMergedJet_, "PuppiSoftDropTau3"  , -9999.);
//!!  mjet_.puppiSD_ecf_1e2 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF1e2", -9999.);
//!!  mjet_.puppiSD_ecf_1e3 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF1e3", -9999.);
//!!  mjet_.puppiSD_ecf_2e3 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF2e3", -9999.);
//!!  mjet_.puppiSD_ecf_3e3 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF3e3", -9999.);
//!!  mjet_.puppiSD_ecf_1e4 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF1e4", -9999.);
//!!  mjet_.puppiSD_ecf_2e4 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF2e4", -9999.);
//!!  mjet_.puppiSD_ecf_6e4 = PATJetUserFloat(patMergedJet_, "PuppiSoftDropECF6e4", -9999.);
//!!
//!!  if(patMergedJet_.nSubjetCollections() > 0){
//!!
//!!    mjet_.subjets0.reserve (patMergedJet_.subjets(0).size());
//!!    for(unsigned int i=0; i<patMergedJet_.subjets(0).size(); ++i){
//!!
//!!      pat::Jet const* patSubj = static_cast<pat::Jet const*>(&*patMergedJet_.subjets(0).at(i));
//!!      if(!patSubj){ throw cms::Exception("LogicError") << "@@@ Failed static_cast from daughter of pat::Jet to pat::Jet"; }
//!!
//!!      llj::Jet ntpSubj;
//!!      fill_Jet(ntpSubj, *patSubj);
//!!      mjet_.subjets0.emplace_back(ntpSubj);
//!!    }
//!!  }
//!!
//!!  if(patMergedJet_.nSubjetCollections() > 1){
//!!
//!!    mjet_.subjets1.reserve (patMergedJet_.subjets(1).size());
//!!    for(unsigned int i=0; i<patMergedJet_.subjets(1).size(); ++i){
//!!
//!!      pat::Jet const* patSubj = static_cast<pat::Jet const*>(&*patMergedJet_.subjets(1).at(i));
//!!      if(!patSubj){ throw cms::Exception("LogicError") << "@@@ Failed static_cast from daughter of pat::Jet to pat::Jet"; }
//!!
//!!      llj::Jet ntpSubj;
//!!      fill_Jet(ntpSubj, *patSubj);
//!!      mjet_.subjets1.emplace_back(ntpSubj);
//!!    }
//!!  }
//!!
//!!  return;
//!!}
//!!
//!!void NTuplizer::fill_MET(llj::MET& met_, const pat::MET& patMet_) const {
//!!
//!!  met_.pt     = patMet_.pt();
//!!  met_.phi    = patMet_.phi();
//!!  met_.sumEt  = patMet_.sumEt();
//!!  met_.mEtSig = patMet_.mEtSig();
//!!  met_.signif = patMet_.significance();
//!!
//!!  return;
//!!}
//!!
//!!float NTuplizer::PATJetUserFloat(const pat::Jet& pat_jet, const std::string& fkey, const float val0) const {
//!!
//!!  return pat_jet.hasUserFloat(fkey) ? pat_jet.userFloat(fkey) : val0;
//!!}

void NTuplizer::beginJob(){

  edm::Service<TFileService> fileService;

  if(not fileService){

    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fileService->make<TTree>("Events", "Events");

  if(not ttree_){

    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }

  ttree_->Branch("run", &run_);
  ttree_->Branch("luminosityBlock", &luminosityBlock_);
  ttree_->Branch("event", &event_);

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
//!!  desc.add<edm::InputTag>("hltMet", edm::InputTag("hltMet", "", "HLT2"))->setComment("HLT collection \"hltMet\"");
  desc.setUnknown();
//!!  edm::ParameterSetDescription recoCaloMETCollections;
//!!  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("jmeTriggerNTuplizer", desc);
}

DEFINE_FWK_MODULE(NTuplizer);
