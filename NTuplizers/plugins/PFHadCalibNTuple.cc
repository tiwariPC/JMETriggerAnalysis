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

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  // name of module
  std::string const moduleLabel_;

  // name of TTree
  std::string const ttreeName_;

  // input EDM collections
  edm::EDGetTokenT<reco::GenParticleCollection> const genPartsToken_;
  edm::EDGetTokenT<reco::PFSimParticleCollection> const pfSimPartsToken_;
  edm::EDGetTokenT<reco::PFCandidateCollection> const recoPFCandsToken_;

  // min pt for charged hadrons
  double const minPt_;

  // min track-p for charged hadrons
  double const minTrackP_;

  // min ecal+hcal raw energy for charged hadrons
  double const minCaloEnergy_;

  // max ecal raw energy to define a MIP
  double const maxECalEnergy_;

  // min number of pixel hits for charged hadrons
  uint const minPixelHits_;

  // min number of tracker hits for charged hadrons
  std::vector<uint> const minTrackerHits_;
  std::vector<double> const maxEtaForMinTrackerHitsCut_;

  // use PFBlockElements to count tracks associated to reco::PFCandidate
  bool const usePFBlockElements_;

  // Number of tracks after cuts
  std::vector<uint> globalCounter_;

  TTree* ttree_ = nullptr;

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
    : moduleLabel_(iConfig.getParameter<std::string>("@module_label")),
      ttreeName_(iConfig.getParameter<std::string>("TTreeName")),
      genPartsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
      pfSimPartsToken_(consumes<reco::PFSimParticleCollection>(iConfig.getParameter<edm::InputTag>("pfSimParticles"))),
      recoPFCandsToken_(consumes<reco::PFCandidateCollection>(iConfig.getParameter<edm::InputTag>("recoPFCandidates"))),
      minPt_(iConfig.getParameter<double>("minPt")),
      minTrackP_(iConfig.getParameter<double>("minTrackP")),
      minCaloEnergy_(iConfig.getParameter<double>("minCaloEnergy")),
      maxECalEnergy_(iConfig.getParameter<double>("maxECalEnergy")),
      minPixelHits_(iConfig.getParameter<uint>("minPixelHits")),
      minTrackerHits_(iConfig.getParameter<std::vector<uint>>("minTrackerHits")),
      maxEtaForMinTrackerHitsCut_(iConfig.getParameter<std::vector<double>>("maxEtaForMinTrackerHitsCut")),
      usePFBlockElements_(iConfig.getParameter<bool>("usePFBlockElements")) {
  globalCounter_ = std::vector<uint>(13, 0);

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
  edm::LogPrint("") << "----------------------------------------------------------";
  edm::LogPrint("") << moduleLabel_;
  edm::LogPrint("") << "----------------------------------------------------------";
  edm::LogPrint("") << "Total number of events: " << globalCounter_[0];
  edm::LogPrint("") << "Number of isolated pions: " << globalCounter_[1];
  edm::LogPrint("") << "Number of true particles within dR = 0.01 of an isolated pion: " << globalCounter_[2];
  edm::LogPrint("") << "Number of true particles with track matching: " << globalCounter_[3];
  edm::LogPrint("") << "Number of PF candidates: " << globalCounter_[4];
  edm::LogPrint("") << "Number of PF Charged Hadrons: " << globalCounter_[5];
  edm::LogPrint("") << " - With pt > " << minPt_ << " GeV: " << globalCounter_[6];
  edm::LogPrint("") << " - With E_ECAL+E_HCAL > " << minCaloEnergy_ << " GeV: " << globalCounter_[7];
  edm::LogPrint("") << " - With only 1 track in the block: " << globalCounter_[8];
  edm::LogPrint("") << " - With p > " << minTrackP_ << " GeV: " << globalCounter_[9];
  edm::LogPrint("") << " - With at least " << minPixelHits_ << " pixel hits: " << globalCounter_[10];
//  edm::LogPrint("") << " - With at least [N] tracker hits " << globalCounter_[11];
  edm::LogPrint("") << " - With E_ECAL < " << maxECalEnergy_ << " GeV: " << globalCounter_[12];
}

void PFHadCalibNTuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& genParts = iEvent.get(genPartsToken_);
  auto const& pfSimParts = iEvent.get(pfSimPartsToken_);
  auto const& recoPFCands = iEvent.get(recoPFCandsToken_);

  reset_variables();

  globalCounter_[0]++;

  for (uint genpIdx_i = 0; genpIdx_i < genParts.size(); ++genpIdx_i) {
    auto const& genp_i = genParts.at(genpIdx_i);
    // Gen and true particle selection
    if (genp_i.status() == 1 and genp_i.pdgId() == -211) {
      auto mindR = 999999.f;
      for (uint genpIdx_j = 0; genpIdx_j != genpIdx_i and genpIdx_j < genParts.size(); ++genpIdx_j) {
        auto const& genp_j = genParts.at(genpIdx_j);
        if (genp_j.status() == 1) {
          auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), genp_j.eta(), genp_j.phi());
          if (dR < mindR)
            mindR = dR;
        }
      }

      if (mindR > 1.) {  // Pion isolation
        globalCounter_[1]++;

        for (auto const& ptc : pfSimParts) {
          // Only consider negatively charged particles
          if (ptc.charge() >= 0)
            continue;

          // There should be true particle within deltaR = 0.01 of the gen particle
          auto const& gen = ptc.trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach);
          auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), gen.momentum().Eta(), gen.momentum().Phi());
          if (dR > 0.01) continue;
          globalCounter_[2]++;

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
          if (not tpatecal.isValid())
            continue;

          auto const eta = tpatecal.positionREP().Eta();
          auto const phi = tpatecal.positionREP().Phi();
          auto const trueE = std::sqrt(tpatecal.momentum().Vect().Mag2());
          auto const true_dr = reco::deltaR(gen.momentum().Eta(), gen.momentum().Phi(), eta, phi);

          // extrapolated track within 0.1 of the true particle
          if (true_dr > 0.1) continue;
          globalCounter_[3]++;

          true_energy_.emplace_back(trueE);
          true_eta_.emplace_back(eta);
          true_phi_.emplace_back(phi);
          true_dr_.emplace_back(true_dr);
          true_isCharged_.emplace_back(isCharged);
        }  // end of true particle loop
      }    // isolation > 1
    }      // stable gen particle pdgid = -211
  }        // end of all gen particles loop

  // Reco pion(pi-) selection
  for (auto const& pfc : recoPFCands) {
    globalCounter_[4]++;

    if (pfc.particleId() != 1) continue;
    globalCounter_[5]++;

    if (pfc.pt() < minPt_) continue;
    globalCounter_[6]++;

    auto const ecalRaw = pfc.rawEcalEnergy();
    auto const hcalRaw = pfc.rawHcalEnergy();
    if ((ecalRaw + hcalRaw) < minCaloEnergy_) continue;
    globalCounter_[7]++;

    auto nTracks = 0u;
    auto const& theElements = pfc.elementsInBlocks();
    if (theElements.empty()) {
      if (not usePFBlockElements_)
        nTracks = 1;  //!! hack for pfTICL (ref: https://github.com/cms-sw/cmssw/pull/32202)
    } else {
      auto const& elements = theElements[0].first->elements();
      for (unsigned iEle = 0; iEle < elements.size(); ++iEle) {
        if (elements[iEle].type() == reco::PFBlockElement::TRACK) {
          ++nTracks;
        }
      }
    }

    if (nTracks != 1) continue;
    globalCounter_[8]++;

    auto trackRef = pfc.trackRef();

    auto const track_p = trackRef->p();
    auto const track_pt = trackRef->pt();
    auto const track_eta = trackRef->eta();

    if (track_p < minTrackP_ || track_pt < minPt_) continue;
    globalCounter_[9]++;

    uint tobN = 0;
    uint tecN = 0;
    uint tibN = 0;
    uint tidN = 0;
    uint pxbN = 0;
    uint pxdN = 0;
    auto const& hp = trackRef->hitPattern();
    switch (trackRef->algo()) {
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

    if (inner < minPixelHits_) continue;
    globalCounter_[10]++;

//!!    auto hasMinHits = false;
//!!    for (uint ieta = 0; ieta < maxEtaForMinTrackerHitsCut_.size(); ++ieta) {
//!!      auto const etaMin = ieta ? maxEtaForMinTrackerHitsCut_[ieta-1] : 0.;
//!!      auto const etaMax = maxEtaForMinTrackerHitsCut_[ieta];
//!!
//!!      if (std::abs(eta) >= etaMin and std::abs(eta) < etaMax) {
//!!        hasMinHits = (inner + outer) > minTrackerHits_[ieta]);
//!!        break;
//!!      }
//!!    }
//!!    if (not hasMinHits) continue;
    globalCounter_[11]++;

    if (ecalRaw > maxECalEnergy_) continue;
    globalCounter_[12]++;

    pfc_ecal_.emplace_back(ecalRaw);
    pfc_hcal_.emplace_back(hcalRaw);
    pfc_eta_.emplace_back(pfc.eta());
    pfc_phi_.emplace_back(pfc.phi());
    pfc_charge_.emplace_back(pfc.charge());
    pfc_id_.emplace_back(pfc.particleId());
    trackRef_p_.emplace_back(track_p);
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
