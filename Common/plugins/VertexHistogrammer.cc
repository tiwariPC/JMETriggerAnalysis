#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "TH1D.h"

class VertexHistogrammer : public edm::EDAnalyzer {

 public:
  explicit VertexHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  edm::EDGetToken vertices_token_;

  edm::Service<TFileService> fs_;

  TH1D *h_vertex_x_;
  TH1D *h_vertex_y_;
  TH1D *h_vertex_z_;
  TH1D *h_vertex_normChi2_;
  TH1D *h_vertex_ndof_;
  TH1D *h_vertex_nTracks_;

  TH1D *h_track_pt_;
  TH1D *h_track_eta_;
  TH1D *h_track_phi_;
  TH1D *h_track_dxy_;
  TH1D *h_track_dz_;
};

VertexHistogrammer::VertexHistogrammer(const edm::ParameterSet& iConfig)
  : vertices_token_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("src"))){

  h_vertex_x_ = fs_->make<TH1D>("vertex_x", "vertex_x", 500, -1, 1);
  h_vertex_y_ = fs_->make<TH1D>("vertex_y", "vertex_y", 500, -1, 1);
  h_vertex_z_ = fs_->make<TH1D>("vertex_z", "vertex_z", 600, -20, 20);
  h_vertex_normChi2_ = fs_->make<TH1D>("vertex_normChi2", "vertex_normChi2", 600, 0, 20);
  h_vertex_ndof_ = fs_->make<TH1D>("vertex_ndof", "vertex_ndof", 600, 0, 20);
  h_vertex_nTracks_ = fs_->make<TH1D>("vertex_nTracks", "vertex_nTracks", 600, 0, 20);

  h_track_pt_ = fs_->make<TH1D>("track_pt", "track_pt", 500, 0, 5.);
  h_track_eta_ = fs_->make<TH1D>("track_eta", "track_eta", 500, -5., 5.);
  h_track_phi_ = fs_->make<TH1D>("track_phi", "track_phi", 600, -3., 3.);
  h_track_dxy_ = fs_->make<TH1D>("track_dxy", "track_dxy", 600, -1., 1.);
  h_track_dz_ = fs_->make<TH1D>("track_dz", "track_dz", 600, -1., 1.);
}

void VertexHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertices_token_, vertices);

  if(vertices.isValid()){

    for(const auto& vtx : *vertices){

      h_vertex_x_->Fill(vtx.x());
      h_vertex_y_->Fill(vtx.y());
      h_vertex_z_->Fill(vtx.z());
      h_vertex_normChi2_->Fill(vtx.normalizedChi2());
      h_vertex_ndof_->Fill(vtx.ndof());
      h_vertex_nTracks_->Fill(vtx.nTracks());

      if(vtx.hasRefittedTracks()){

        for(const auto& trk : vtx.refittedTracks()){

          h_track_pt_->Fill(trk.pt());
          h_track_eta_->Fill(trk.eta());
          h_track_phi_->Fill(trk.phi());
          h_track_dxy_->Fill(trk.dxy(vtx.position()));
          h_track_dz_->Fill(trk.dz(vtx.position()));
        }
      }
      else {

        for(std::vector<reco::TrackBaseRef>::const_iterator trk_it = vtx.tracks_begin(); trk_it != vtx.tracks_end(); ++trk_it){

          h_track_pt_->Fill((*trk_it)->pt());
          h_track_eta_->Fill((*trk_it)->eta());
          h_track_phi_->Fill((*trk_it)->phi());
          h_track_dxy_->Fill((*trk_it)->dxy(vtx.position()));
          h_track_dz_->Fill((*trk_it)->dz(vtx.position()));
        }
      }
    }
  }
  else {

    edm::LogWarning("Input") << "invalid VertexCollection";
  }
}

void VertexHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  edm::ParameterSetDescription desc;
//  desc.setUnknown();
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of input reco::VertexCollection");
  descriptions.add("VertexHistogrammer", desc);
}

DEFINE_FWK_MODULE(VertexHistogrammer);
