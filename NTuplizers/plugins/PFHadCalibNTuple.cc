#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowReco/interface/PFSimParticle.h"
#include "DataFormats/ParticleFlowReco/interface/PFSimParticleFwd.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementTrack.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include <TFile.h>
#include <TTree.h>

class PFHadCalibNTuple : public edm::one::EDAnalyzer<edm::one::SharedResources> {

public:
  explicit PFHadCalibNTuple(edm::ParameterSet const&);
  ~PFHadCalibNTuple() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void analyze(const edm::Event &, const edm::EventSetup &) override;

  edm::EDGetTokenT<reco::GenParticleCollection> const genPartsToken_;
  edm::EDGetTokenT<reco::PFSimParticleCollection> const pfSimPartsToken_;
  edm::EDGetTokenT<reco::PFCandidateCollection> const recoPFCandsToken_;

  TTree* ttree_ = nullptr;

  /// Min pt for charged hadrons
  double const ptMin_;

  /// Min p for charged hadrons
  double const pMin_;

  /// Min hcal raw energy for charged hadrons
  double const hcalMin_;

  /// Max ecal raw energy to define a MIP
  double const ecalMax_;

  /// Min number of pixel hits for charged hadrons
  uint const nPixelHitsMin_;

  /// Min number of tracker hits for charged hadrons
  std::vector<uint> const nTrackerHitsMin_;
  std::vector<double> const nTrackerHitsMinEtaMax_;

  /// use PFBlockElements to find tracks associated to PFChargedHadron
  bool const usePFBlockElements_;

  /// name of TTree
  std::string const ttreeName_;

  /// Number of tracks after cuts
  std::vector<uint> nCh;
  std::vector<uint> nEv;

  std::vector<float> true_energy_;
  std::vector<float> true_eta_;
  std::vector<float> true_phi_;
  std::vector<float> true_dr_;
  std::vector<bool> true_isCharged_;
  std::vector<float> pfc_ecal_;
  std::vector<float> pfc_hcal_;
  std::vector<float> pfc_eta_;
  std::vector<float> pfc_phi_;
  std::vector<float> pfc_charge_;
  std::vector<float> pfc_id_;
  std::vector<float> trackRef_p_;

  void reset_variables();
};

PFHadCalibNTuple::PFHadCalibNTuple(const edm::ParameterSet& iConfig)
  : genPartsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles")))
  , pfSimPartsToken_(consumes<reco::PFSimParticleCollection>(iConfig.getParameter<edm::InputTag>("pfSimParticles")))
  , recoPFCandsToken_(consumes<reco::PFCandidateCollection>(iConfig.getParameter<edm::InputTag>("recoPFCandidates")))
  , ptMin_(iConfig.getParameter<double>("ptMin"))
  , pMin_(iConfig.getParameter<double>("pMin"))
  , hcalMin_(iConfig.getParameter<double>("hcalMin"))
  , ecalMax_(iConfig.getParameter<double>("ecalMax"))
  , nPixelHitsMin_(iConfig.getParameter<uint>("nPixelHitsMin"))
  , nTrackerHitsMin_(iConfig.getParameter<std::vector<uint>>("nTrackerHitsMin"))
  , nTrackerHitsMinEtaMax_(iConfig.getParameter<std::vector<double>>("nTrackerHitsMinEtaMax"))
  , usePFBlockElements_(iConfig.getParameter<bool>("usePFBlockElements"))
  , ttreeName_(iConfig.getParameter<std::string>("TTreeName"))
{
  nCh = std::vector<uint>(10, 0);
  nEv = std::vector<uint>(3, 0);

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fs->make<TTree>(ttreeName_.c_str(), ttreeName_.c_str());

  if (not ttree_) {
    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }

  ttree_->Branch("true_energy", &true_energy_);
  ttree_->Branch("true_eta", &true_eta_);
  ttree_->Branch("true_phi", &true_phi_);
  ttree_->Branch("true_dr", &true_dr_);
  ttree_->Branch("true_isCharged", &true_isCharged_);
  ttree_->Branch("pfc_ecal", &pfc_ecal_);
  ttree_->Branch("pfc_hcal", &pfc_hcal_);
  ttree_->Branch("pfc_eta", &pfc_eta_);
  ttree_->Branch("pfc_phi", &pfc_phi_);
  ttree_->Branch("pfc_charge", &pfc_charge_);
  ttree_->Branch("pfc_id", &pfc_id_);
  ttree_->Branch("trackRef_p", &trackRef_p_);
}

PFHadCalibNTuple::~PFHadCalibNTuple() {

  edm::LogPrint("") << "Total number of events: " << nEv[0];
  edm::LogPrint("") << "Number of isolated pions: " << nEv[1];
  edm::LogPrint("") << "Number of true particles within dR = 0.01 of an isolated pion: " << nEv[2];
  edm::LogPrint("") << "Number of true particles with track matching: " << nCh[7];
  edm::LogPrint("") << "Number of PF candidates: " << nCh[0];
  edm::LogPrint("") << "Number of PF Charged Hadrons: " << nCh[1];
  edm::LogPrint("") << " - With pt > " << ptMin_ << " GeV: " << nCh[2];
  edm::LogPrint("") << " - With E_HCAL > " << hcalMin_ << " GeV: " << nCh[3];
  edm::LogPrint("") << " - With only 1 track in the block: " << nCh[4];
  edm::LogPrint("") << " - With p > " << pMin_ << " GeV: " << nCh[5];
  edm::LogPrint("") << " - With at least " << nPixelHitsMin_ << " pixel hits: " << nCh[6];
  edm::LogPrint("") << " - With E_ECAL < " << ecalMax_ << " GeV: " << nCh[8];
}

void PFHadCalibNTuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& genParts = iEvent.get(genPartsToken_);
  auto const& pfSimParts = iEvent.get(pfSimPartsToken_);
  auto const& recoPFCands = iEvent.get(recoPFCandsToken_);

  reset_variables();

  nEv[0]++;

    for (uint genpIdx_i=0; genpIdx_i<genParts.size(); ++genpIdx_i) {
      auto const& genp_i = genParts.at(genpIdx_i);
      // Gen and true particle selection
      if (genp_i.status() == 1 and genp_i.pdgId() == -211) {
        auto mindR = 999999.f;
        for (uint genpIdx_j=0; genpIdx_j != genpIdx_i and genpIdx_j < genParts.size(); ++genpIdx_j) {
          auto const& genp_j = genParts.at(genpIdx_j);
          if (genp_j.status() == 1) {
            auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), genp_j.eta(), genp_j.phi());
            if (dR < mindR) mindR = dR;
          }
        }

        if (mindR > 1.) {  // Pion isolation
          nEv[1]++;

          for (auto const& ptc : pfSimParts) {
            // Only consider negatively charged particles
            if (ptc.charge() >= 0) continue;

            // There should be true particle within deltaR = 0.01 of the gen particle
            auto const& gen = ptc.trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach);
            auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), gen.momentum().Eta(), gen.momentum().Phi());
            if (dR > 0.01) continue;
            nEv[2]++;

            // Check if there is a reconstructed track *in the event*
            auto isCharged = false;
            for (auto const& pfc : recoPFCands) {
              if (pfc.particleId() < 4) {
                isCharged = true;
                break;
              }
            }

            reco::PFTrajectoryPoint::LayerType ecalEntrance = reco::PFTrajectoryPoint::ECALEntrance;
            const reco::PFTrajectoryPoint& tpatecal = ptc.extrapolatedPoint(ecalEntrance);
            if (not tpatecal.isValid()) continue;

            auto const eta = tpatecal.positionREP().Eta();
            auto const phi = tpatecal.positionREP().Phi();
            auto const trueE = std::sqrt(tpatecal.momentum().Vect().Mag2());
            auto const true_dr = reco::deltaR(gen.momentum().Eta(), gen.momentum().Phi(), eta, phi);

            // The extrapolated track should be within 0.1 of the true particle
            if (true_dr > 0.1) continue;
            nCh[7]++;

            true_energy_.emplace_back(trueE);
            true_eta_.emplace_back(eta);
            true_phi_.emplace_back(phi);
            true_dr_.emplace_back(true_dr);
            true_isCharged_.emplace_back(isCharged);
          }  // end of true particle loop
        } // isolation > 1
      } // stable gen particle pdgid = -211
    } // end of all gen particles loop

    // Reco pion(pi-) selection
    for (auto const& pfc : recoPFCands) {
      nCh[0]++;

      if (pfc.particleId() != 1) continue;
      nCh[1]++;

      if (pfc.pt() < ptMin_) continue;
      nCh[2]++;

      auto const ecalRaw = pfc.rawEcalEnergy();
      auto const hcalRaw = pfc.rawHcalEnergy();
      if ((ecalRaw + hcalRaw) < hcalMin_) continue;
      nCh[3]++;

      auto const& theElements = pfc.elementsInBlocks();

      //if( theElements.empty() ) continue;

      //const reco::PFBlockRef blockRef = theElements[0].first;
      //PFBlock::LinkData linkData =  blockRef->linkData();
      //const edm::OwnVector<reco::PFBlockElement>& elements = blockRef->elements();

      //uint nTracks = 0;
      //uint iTrack = 999999;

      //for(unsigned iEle=0; iEle<elements.size(); iEle++) {
      //	PFBlockElement::Type type = elements[iEle].type();
      //	switch( type )
      //	{
      //		case PFBlockElement::TRACK:
      //			iTrack = iEle;
      //			nTracks++;
      //			break;
      //		default:
      //			continue;
      //	}
      //}

      //if ( nTracks != 1 ) continue;
      nCh[4]++;

      //const reco::PFBlockElementTrack& et = dynamic_cast<const reco::PFBlockElementTrack &>( elements[iTrack] );
      auto const p = pfc.trackRef()->p();
      auto const pt = pfc.trackRef()->pt();
      auto const eta = pfc.trackRef()->eta();

      if (p < pMin_ || pt < ptMin_) continue;
      nCh[5]++;

      uint tobN = 0;
      uint tecN = 0;
      uint tibN = 0;
      uint tidN = 0;
      uint pxbN = 0;
      uint pxdN = 0;
      auto const& hp = pfc.trackRef()->hitPattern();
      switch (pfc.trackRef()->algo()) {
        case reco::TrackBase::hltIter0:
        case reco::TrackBase::hltIter1:
        case reco::TrackBase::hltIter2:
        case reco::TrackBase::highPtTripletStep:
          tobN += hp.numberOfValidStripTOBHits();
          tecN += hp.numberOfValidStripTECHits();
          tibN += hp.numberOfValidStripTIBHits();
          tidN += hp.numberOfValidStripTIDHits();
          pxbN += hp.numberOfValidPixelBarrelHits();
          pxdN += hp.numberOfValidPixelEndcapHits();
          break;
        case reco::TrackBase::hltIter3:
        case reco::TrackBase::hltIter4:
        case reco::TrackBase::hltIterX:
        default:
          break;
      }
      auto const inner = pxbN + pxdN;
      auto const outer = tibN + tobN + tidN + tecN;

      if (inner < nPixelHitsMin_) continue;
      nCh[6]++;

//!!      auto hasMinHits = false;
//!!      for (uint ieta = 0; ieta < nTrackerHitsMinEtaMax_.size(); ++ieta) {
//!!        auto const etaMin = ieta ? nTrackerHitsMinEtaMax_[ieta-1] : 0.;
//!!        auto const etaMax = nTrackerHitsMinEtaMax_[ieta];
//!!
//!!        if (std::abs(eta) >= etaMin and std::abs(eta) < etaMax) {
//!!          hasMinHits = (inner + outer) > nTrackerHitsMin_[ieta]);
//!!          break;
//!!        }
//!!      }

      if (ecalRaw > ecalMax_) continue;
      nCh[8]++;

      pfc_ecal_.emplace_back(ecalRaw);
      pfc_hcal_.emplace_back(hcalRaw);
      pfc_eta_.emplace_back(pfc.eta());
      pfc_phi_.emplace_back(pfc.phi());
      pfc_charge_.emplace_back(pfc.charge());
      pfc_id_.emplace_back(pfc.particleId());
      trackRef_p_.emplace_back(p);
    }  // end of pion (pi-) loop

    ttree_->Fill();
}

void PFHadCalibNTuple::reset_variables() {
  true_energy_.clear();
  true_eta_.clear();
  true_phi_.clear();
  true_dr_.clear();
  true_isCharged_.clear();
  pfc_ecal_.clear();
  pfc_hcal_.clear();
  pfc_eta_.clear();
  pfc_phi_.clear();
  pfc_charge_.clear();
  pfc_id_.clear();
  trackRef_p_.clear();
}

void PFHadCalibNTuple::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(PFHadCalibNTuple);
