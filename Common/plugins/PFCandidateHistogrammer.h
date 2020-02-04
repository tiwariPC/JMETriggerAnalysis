#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"

#include <memory>

#include <TH1D.h>

template <typename PFCandType>
class PFCandidateHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit PFCandidateHistogrammer(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions&);

 private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<std::vector<PFCandType>> pfCands_token_;

  const StringCutObjectSelector<PFCandType> stringCutSelector_;

  TH1D *h_pfcand_mult_;
  TH1D *h_pfcand_mult_X_;
  TH1D *h_pfcand_mult_h_;
  TH1D *h_pfcand_mult_e_;
  TH1D *h_pfcand_mult_mu_;
  TH1D *h_pfcand_mult_gamma_;
  TH1D *h_pfcand_mult_h0_;
  TH1D *h_pfcand_mult_hHF_;
  TH1D *h_pfcand_mult_egammaHF_;
  TH1D *h_pfcand_particleId_;
  TH1D *h_pfcand_pt_;
  TH1D *h_pfcand_eta_;
  TH1D *h_pfcand_phi_;
  TH1D *h_pfcand_mass_;
  TH1D *h_pfcand_vx_;
  TH1D *h_pfcand_vy_;
  TH1D *h_pfcand_vz_;
};

template <typename PFCandType>
PFCandidateHistogrammer<PFCandType>::PFCandidateHistogrammer(const edm::ParameterSet& iConfig)
  : pfCands_token_(consumes<std::vector<PFCandType>>(iConfig.getParameter<edm::InputTag>("src")))
  , stringCutSelector_(iConfig.getParameter<std::string>("cut")){

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if(not fs){

    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_pfcand_mult_ = fs->make<TH1D>("pfcand_mult", "pfcand_mult", 240, 0, 12000);
  h_pfcand_mult_X_ = fs->make<TH1D>("pfcand_mult_X", "pfcand_mult_X", 240, 0, 7200);
  h_pfcand_mult_h_ = fs->make<TH1D>("pfcand_mult_h", "pfcand_mult_h", 240, 0, 7200);
  h_pfcand_mult_e_ = fs->make<TH1D>("pfcand_mult_e", "pfcand_mult_e", 240, 0, 7200);
  h_pfcand_mult_mu_ = fs->make<TH1D>("pfcand_mult_mu", "pfcand_mult_mu", 240, 0, 1200);
  h_pfcand_mult_gamma_ = fs->make<TH1D>("pfcand_mult_gamma", "pfcand_mult_gamma", 240, 0, 7200);
  h_pfcand_mult_h0_ = fs->make<TH1D>("pfcand_mult_h0", "pfcand_mult_h0", 240, 0, 7200);
  h_pfcand_mult_hHF_ = fs->make<TH1D>("pfcand_mult_hHF", "pfcand_mult_hHF", 240, 0, 7200);
  h_pfcand_mult_egammaHF_ = fs->make<TH1D>("pfcand_mult_egammaHF", "pfcand_mult_egammaHF", 240, 0, 7200);
  h_pfcand_particleId_ = fs->make<TH1D>("pfcand_particleId", "pfcand_particleId", 8, 0, 8);
  h_pfcand_pt_ = fs->make<TH1D>("pfcand_pt", "pfcand_pt", 600, 0, 5.);
  h_pfcand_eta_ = fs->make<TH1D>("pfcand_eta", "pfcand_eta", 600, -5., 5.);
  h_pfcand_phi_ = fs->make<TH1D>("pfcand_phi", "pfcand_phi", 600, -3., 3.);
  h_pfcand_mass_ = fs->make<TH1D>("pfcand_mass", "pfcand_mass", 240, 0, 240.);
  h_pfcand_vx_ = fs->make<TH1D>("pfcand_vx", "pfcand_vx", 240, -0.1, 0.1);
  h_pfcand_vy_ = fs->make<TH1D>("pfcand_vy", "pfcand_vy", 240, -0.1, 0.1);
  h_pfcand_vz_ = fs->make<TH1D>("pfcand_vz", "pfcand_vz", 240, -30, 30);
}

template <typename PFCandType>
void PFCandidateHistogrammer<PFCandType>::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  auto const& pfCands = iEvent.get(pfCands_token_);

  uint pfcand_mult(0), pfcand_mult_X(0), pfcand_mult_h(0), pfcand_mult_e(0), \
       pfcand_mult_mu(0), pfcand_mult_gamma(0), pfcand_mult_h0(0),\
       pfcand_mult_hHF(0), pfcand_mult_egammaHF(0);

  for(auto const& pfc : pfCands){

    if(not stringCutSelector_(pfc)){ continue; }

    ++pfcand_mult;

    const auto abs_pdgId(std::abs(pfc.pdgId()));

    uint pid(0);

    if(abs_pdgId == 211){
      ++pfcand_mult_h;
      pid = 1;
    }
    else if(abs_pdgId == 11){
      ++pfcand_mult_e;
      pid = 2;
    }
    else if(abs_pdgId == 13){
      ++pfcand_mult_mu;
      pid = 3;
    }
    else if(abs_pdgId == 22){
      ++pfcand_mult_gamma;
      pid = 4;
    }
    else if(abs_pdgId == 130){
      ++pfcand_mult_h0;
      pid = 5;
    }
    else if(abs_pdgId == 1){
      ++pfcand_mult_hHF;
      pid = 6;
    }
    else if(abs_pdgId == 2){
      ++pfcand_mult_egammaHF;
      pid = 7;
    }
    else {
      ++pfcand_mult_X;
      pid = 0;
    }

    h_pfcand_particleId_->Fill(pid + 0.5);
    h_pfcand_pt_->Fill(pfc.pt());
    h_pfcand_eta_->Fill(pfc.eta());
    h_pfcand_phi_->Fill(pfc.phi());
    h_pfcand_mass_->Fill(pfc.mass());
    h_pfcand_vx_->Fill(pfc.vx());
    h_pfcand_vy_->Fill(pfc.vy());
    h_pfcand_vz_->Fill(pfc.vz());
  }

  h_pfcand_mult_->Fill(pfcand_mult);
  h_pfcand_mult_X_->Fill(pfcand_mult_X);
  h_pfcand_mult_h_->Fill(pfcand_mult_h);
  h_pfcand_mult_e_->Fill(pfcand_mult_e);
  h_pfcand_mult_mu_->Fill(pfcand_mult_mu);
  h_pfcand_mult_gamma_->Fill(pfcand_mult_gamma);
  h_pfcand_mult_h0_->Fill(pfcand_mult_h0);
  h_pfcand_mult_hHF_->Fill(pfcand_mult_hHF);
  h_pfcand_mult_egammaHF_->Fill(pfcand_mult_egammaHF);
}

template <typename PFCandType>
void PFCandidateHistogrammer<PFCandType>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of collection of PF candidates");
  desc.add<std::string>("cut", "")->setComment("argument of StringCutObjectSelector for PF candidate selection");
  descriptions.add(defaultModuleLabel<PFCandidateHistogrammer<PFCandType>>(), desc);
}
