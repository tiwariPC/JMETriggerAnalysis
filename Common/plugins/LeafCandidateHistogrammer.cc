#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include <memory>

#include <TH1D.h>

class LeafCandidateHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit LeafCandidateHistogrammer(const edm::ParameterSet &);
  static void fillDescriptions(edm::ConfigurationDescriptions &);

private:
  void analyze(const edm::Event &, const edm::EventSetup &) override;

  const edm::InputTag leafCands_tag_;
  const edm::EDGetTokenT<edm::View<reco::LeafCandidate>> leafCands_token_;

  const StringCutObjectSelector<reco::LeafCandidate> stringCutSelector_;

  TH1D *h_leafcand_mult_ = nullptr;
  TH1D *h_leafcand_pt_ = nullptr;
  TH1D *h_leafcand_pt_2_ = nullptr;
  TH1D *h_leafcand_eta_ = nullptr;
  TH1D *h_leafcand_phi_ = nullptr;
  TH1D *h_leafcand_mass_ = nullptr;
};

LeafCandidateHistogrammer::LeafCandidateHistogrammer(const edm::ParameterSet &iConfig)
    : leafCands_tag_(iConfig.getParameter<edm::InputTag>("src")),
      leafCands_token_(consumes<edm::View<reco::LeafCandidate>>(leafCands_tag_)),
      stringCutSelector_(iConfig.getParameter<std::string>("cut")) {
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_leafcand_mult_ = fs->make<TH1D>("leafcand_mult", "leafcand_mult", 240, 0, 12000);
  h_leafcand_pt_ = fs->make<TH1D>("leafcand_pt", "leafcand_pt", 600, 0, 5.);
  h_leafcand_pt_2_ = fs->make<TH1D>("leafcand_pt_2", "leafcand_pt_2", 600, 0, 600);
  h_leafcand_eta_ = fs->make<TH1D>("leafcand_eta", "leafcand_eta", 600, -5., 5.);
  h_leafcand_phi_ = fs->make<TH1D>("leafcand_phi", "leafcand_phi", 600, -3., 3.);
  h_leafcand_mass_ = fs->make<TH1D>("leafcand_mass", "leafcand_mass", 240, 0, 240.);
}

void LeafCandidateHistogrammer::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
  auto const &leafCands_handle(iEvent.getHandle(leafCands_token_));

  if (leafCands_handle.isValid()) {
    uint leafcand_mult(0);

    for (auto const &leafc : *leafCands_handle) {
      if (not stringCutSelector_(leafc)) {
        continue;
      }

      ++leafcand_mult;

      h_leafcand_pt_->Fill(leafc.pt());
      h_leafcand_pt_2_->Fill(leafc.pt());
      h_leafcand_eta_->Fill(leafc.eta());
      h_leafcand_phi_->Fill(leafc.phi());
      h_leafcand_mass_->Fill(leafc.mass());
    }

    h_leafcand_mult_->Fill(leafcand_mult);
  } else {
    edm::LogWarning("Input") << "invalid handle to input collection : " << leafCands_tag_.encode();
  }
}

void LeafCandidateHistogrammer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("particleFlow"))->setComment("edm::InputTag of reco::LeafCandidate collection");
  desc.add<std::string>("cut", "")->setComment("string selector for reco::LeafCandidate collection");
  descriptions.add("leafCandidateHistogrammer", desc);
}

DEFINE_FWK_MODULE(LeafCandidateHistogrammer);
