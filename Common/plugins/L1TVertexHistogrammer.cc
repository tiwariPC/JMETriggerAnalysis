#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/L1TCorrelator/interface/TkPrimaryVertex.h"

#include <memory>

#include <TH1D.h>

class L1TVertexHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit L1TVertexHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag vertices_tag_;
  const edm::EDGetTokenT<l1t::TkPrimaryVertexCollection> vertices_token_;

  TH1D* h_vertex_mult_ = nullptr;
  TH1D* h_vertex_z_ = nullptr;
  TH1D* h_vertex0_z_ = nullptr;
  TH1D* h_vertex_sum_ = nullptr;
  TH1D* h_vertex0_sum_ = nullptr;
};

L1TVertexHistogrammer::L1TVertexHistogrammer(const edm::ParameterSet& iConfig)
    : vertices_tag_(iConfig.getParameter<edm::InputTag>("src")),
      vertices_token_(consumes<l1t::TkPrimaryVertexCollection>(vertices_tag_)) {
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_vertex_mult_ = fs->make<TH1D>("vertex_mult", "vertex_mult", 200, 0, 200);

  h_vertex_z_ = fs->make<TH1D>("vertex_z", "vertex_z", 120, -30, 30);
  h_vertex_sum_ = fs->make<TH1D>("vertex_sum", "vertex_sum", 90, 0, 900);
  h_vertex0_z_ = fs->make<TH1D>("vertex0_z", "vertex0_z", 120, -30, 30);
  h_vertex0_sum_ = fs->make<TH1D>("vertex0_sum", "vertex0_sum", 90, 0, 900);
}

void L1TVertexHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& vertices(iEvent.getHandle(vertices_token_));

  if (vertices.isValid()) {
    h_vertex_mult_->Fill(vertices->size());

    for (uint idx = 0; idx < vertices->size(); ++idx) {
      auto const& vtx(vertices->at(idx));

      if (idx == 0) {
        h_vertex0_z_->Fill(vtx.zvertex());
        h_vertex0_sum_->Fill(vtx.sum());
      }

      h_vertex_z_->Fill(vtx.zvertex());
      h_vertex_sum_->Fill(vtx.sum());
    }
  } else {
    edm::LogWarning("Input") << "invalid handle to l1t::TkPrimaryVertexCollection : " << vertices_tag_.encode();
  }
}

void L1TVertexHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of l1t::TkPrimaryVertexCollection");
  descriptions.add("l1tVertexHistogrammer", desc);
}

DEFINE_FWK_MODULE(L1TVertexHistogrammer);
