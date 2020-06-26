#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/L1TCorrelator/interface/TkPrimaryVertex.h"
#include "DataFormats/L1TParticleFlow/interface/PFTrack.h"

#include <memory>

#include <TH1D.h>

class L1TPFTrackHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit L1TPFTrackHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

 private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag pfTracks_tag_;
  const edm::EDGetTokenT<l1t::PFTrackCollection> pfTracks_token_;

  TH1D *h_pfTrack_mult_ = nullptr;
  TH1D *h_pfTrack_pt_ = nullptr;
  TH1D *h_pfTrack_pt_2_ = nullptr;
  TH1D *h_pfTrack_eta_ = nullptr;
  TH1D *h_pfTrack_phi_ = nullptr;
};

L1TPFTrackHistogrammer::L1TPFTrackHistogrammer(const edm::ParameterSet& iConfig)
  : pfTracks_tag_(iConfig.getParameter<edm::InputTag>("src"))
  , pfTracks_token_(consumes<l1t::PFTrackCollection>(pfTracks_tag_)) {

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if(not fs){
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_pfTrack_mult_ = fs->make<TH1D>("pfTrack_mult", "pfTrack_mult", 240, 0, 12000.);
  h_pfTrack_pt_ = fs->make<TH1D>("pfTrack_pt", "pfTrack_pt", 600, 0, 5.);
  h_pfTrack_pt_2_ = fs->make<TH1D>("pfTrack_pt_2", "pfTrack_pt_2", 600, 0, 600.);
  h_pfTrack_eta_ = fs->make<TH1D>("pfTrack_eta", "pfTrack_eta", 600, -5., 5.);
  h_pfTrack_phi_ = fs->make<TH1D>("pfTrack_phi", "pfTrack_phi", 600, -3., 3.);
}

void L1TPFTrackHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  auto const& pfTracks(iEvent.getHandle(pfTracks_token_));

  if(pfTracks.isValid()){
    h_pfTrack_mult_->Fill(pfTracks->size());
    for(auto const& trk : *pfTracks){
      h_pfTrack_pt_->Fill(trk.pt());
      h_pfTrack_pt_2_->Fill(trk.pt());
      h_pfTrack_eta_->Fill(trk.eta());
      h_pfTrack_phi_->Fill(trk.phi());
    }
  }
  else {
    edm::LogWarning("Input") << "invalid handle to l1t::PFTrackCollection : " << pfTracks_tag_.encode();
  }
}

void L1TPFTrackHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of l1t::PFTrackCollection");
  descriptions.add("l1tPFTrackHistogrammer", desc);
}

DEFINE_FWK_MODULE(L1TPFTrackHistogrammer);
