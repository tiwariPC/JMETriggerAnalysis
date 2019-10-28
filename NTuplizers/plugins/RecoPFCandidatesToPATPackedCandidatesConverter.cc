#include <memory>
#include <utility>

#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>

#include <DataFormats/PatCandidates/interface/PackedCandidate.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

class RecoPFCandidatesToPATPackedCandidatesConverter : public edm::EDProducer {

 public:
  explicit RecoPFCandidatesToPATPackedCandidatesConverter(const edm::ParameterSet&);
  virtual ~RecoPFCandidatesToPATPackedCandidatesConverter() {}

 private:
  void produce(edm::Event&, const edm::EventSetup&);

  edm::EDGetTokenT<pat::PackedCandidateCollection> src_;
};

RecoPFCandidatesToPATPackedCandidatesConverter::RecoPFCandidatesToPATPackedCandidatesConverter(const edm::ParameterSet& iConfig){

  src_ = consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("src"));

  produces<reco::PFCandidateCollection>();
}

void RecoPFCandidatesToPATPackedCandidatesConverter::produce(edm::Event& iEvent,const edm::EventSetup& iSetup){

  edm::Handle<pat::PackedCandidateCollection> packedCands_;
  iEvent.getByToken(src_, packedCands_);

  std::unique_ptr<reco::PFCandidateCollection> recoPFCands(new reco::PFCandidateCollection());

  reco::PFCandidate dummy;
  for(int iCand=0; iCand<int(packedCands_->size()); ++iCand){

    reco::PFCandidate intPFCand(packedCands_->at(iCand).charge(),packedCands_->at(iCand).p4(), dummy.translatePdgIdToType(packedCands_->at(iCand).pdgId()));
    recoPFCands->push_back(intPFCand);
  }

  iEvent.put(std::move(recoPFCands));

  return;
}

DEFINE_FWK_MODULE(RecoPFCandidatesToPATPackedCandidatesConverter);
