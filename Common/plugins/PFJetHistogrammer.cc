#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJet.h"

#include <memory>

#include <TH1D.h>

class PFJetHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit PFJetHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

 private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag jets_tag_;
  const edm::EDGetTokenT<reco::PFJetCollection> jets_token_;

  TH1D *h_jet_mult_ = nullptr;
  TH1D *h_jet_pt_ = nullptr;
  TH1D *h_jet_eta_ = nullptr;
  TH1D *h_jet_phi_ = nullptr;
};

PFJetHistogrammer::PFJetHistogrammer(const edm::ParameterSet& iConfig)
  : jets_tag_(iConfig.getParameter<edm::InputTag>("src"))
  , jets_token_(consumes<reco::PFJetCollection>(jets_tag_)) {

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if(not fs){
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_jet_mult_ = fs->make<TH1D>("jet_mult", "jet_mult", 50, 0, 50.);
  h_jet_pt_ = fs->make<TH1D>("jet_pt", "jet_pt", 600, 0, 600.);
  h_jet_eta_ = fs->make<TH1D>("jet_eta", "jet_eta", 600, -5., 5.);
  h_jet_phi_ = fs->make<TH1D>("jet_phi", "jet_phi", 600, -3., 3.);
}

void PFJetHistogrammer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  auto const& jets(iEvent.getHandle(jets_token_));

  if(jets.isValid()){
    h_jet_mult_->Fill(jets->size());
    for(auto const& jet : *jets){
      h_jet_pt_->Fill(jet.pt());
      h_jet_eta_->Fill(jet.eta());
      h_jet_phi_->Fill(jet.phi());
    }
  }
  else {
    edm::LogWarning("Input") << "invalid handle to reco::PFJetCollection : " << jets_tag_.encode();
  }
}

void PFJetHistogrammer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of reco::PFJetCollection");
  descriptions.add("pfJetHistogrammer", desc);
}

DEFINE_FWK_MODULE(PFJetHistogrammer);
