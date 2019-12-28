#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "TH1D.h"

class TrackHistogrammer : public edm::EDAnalyzer {

 public:
  explicit TrackHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  edm::EDGetToken tracks_token_;

  edm::Service<TFileService> fs_;

  TH1D *h_track_pt_;
  TH1D *h_track_eta_;
  TH1D *h_track_phi_;
  TH1D *h_track_outerPt_;
  TH1D *h_track_outerEta_;
  TH1D *h_track_outerPhi_;
};

TrackHistogrammer::TrackHistogrammer(const edm::ParameterSet& iConfig)
  : tracks_token_(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("src"))){

  h_track_pt_ = fs_->make<TH1D>("track_pt", "track_pt", 500, 0, 5.);
  h_track_eta_ = fs_->make<TH1D>("track_eta", "track_eta", 500, -5., 5.);
  h_track_phi_ = fs_->make<TH1D>("track_phi", "track_phi", 600, -3., 3.);

  h_track_outerPt_ = fs_->make<TH1D>("track_outerPt", "track_outerPt", 500, 0, 5.);
  h_track_outerEta_ = fs_->make<TH1D>("track_outerEta", "track_outerEta", 500, -5., 5.);
  h_track_outerPhi_ = fs_->make<TH1D>("track_outerPhi", "track_outerPhi", 600, -3., 3.);
}

void TrackHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(tracks_token_, tracks);

  if(tracks.isValid()){

    for(const auto& trk : *tracks){

      h_track_pt_->Fill(trk.pt());
      h_track_eta_->Fill(trk.eta());
      h_track_phi_->Fill(trk.phi());

      h_track_outerPt_->Fill(trk.outerPt());
      h_track_outerEta_->Fill(trk.outerEta());
      h_track_outerPhi_->Fill(trk.outerPhi());
    }
  }
  else {

    edm::LogWarning("Input") << "invalid TrackCollection";
  }
}

void TrackHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  edm::ParameterSetDescription desc;
//  desc.setUnknown();
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of input reco::TrackCollection");
  descriptions.add("TrackHistogrammer", desc);
}

DEFINE_FWK_MODULE(TrackHistogrammer);
