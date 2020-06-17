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
#include "DataFormats/L1TParticleFlow/interface/PFJet.h"

#include <memory>

#include <TH1D.h>

class L1TrackHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit L1TrackHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

 private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag tracks_tag_;
  const edm::EDGetTokenT<l1t::PFTrackCollection> tracks_token_;

  TH1D *h_track_mult_ = nullptr;
  TH1D *h_track_pt_ = nullptr;
  TH1D *h_track_pt_2_ = nullptr;
  TH1D *h_track_eta_ = nullptr;
  TH1D *h_track_phi_ = nullptr;
};

L1TrackHistogrammer::L1TrackHistogrammer(const edm::ParameterSet& iConfig)
  : tracks_tag_(iConfig.getParameter<edm::InputTag>("src"))
  , tracks_token_(consumes<l1t::PFTrackCollection>(tracks_tag_)) {

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if(not fs){
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_track_mult_ = fs->make<TH1D>("track_mult", "track_mult", 240, 0, 12000.);
  h_track_pt_ = fs->make<TH1D>("track_pt", "track_pt", 600, 0, 5.);
  h_track_pt_2_ = fs->make<TH1D>("track_pt_2", "track_pt_2", 600, 0, 600.);
  h_track_eta_ = fs->make<TH1D>("track_eta", "track_eta", 600, -5., 5.);
  h_track_phi_ = fs->make<TH1D>("track_phi", "track_phi", 600, -3., 3.);
}

void L1TrackHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  auto const& tracks(iEvent.getHandle(tracks_token_));

  if(tracks.isValid()){
    h_track_mult_->Fill(tracks->size());
    for(auto const& trk : *tracks){
      h_track_pt_->Fill(trk.pt());
      h_track_pt_2_->Fill(trk.pt());
      h_track_eta_->Fill(trk.eta());
      h_track_phi_->Fill(trk.phi());
      // h_track_dz_->Fill(trk.dz(vtx.position()));
    }
  }
  else {
    edm::LogWarning("Input") << "invalid handle to l1t::PFTrackCollection : " << tracks_tag_.encode();
  }
}

void L1TrackHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of l1t::PFTrackCollection");
  descriptions.add("L1TrackHistogrammer", desc);
}

DEFINE_FWK_MODULE(L1TrackHistogrammer);
