#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h>

RecoPFJetCollectionContainer::RecoPFJetCollectionContainer(
  const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token, const std::string& strCut, const bool orderByHighestPt
) : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {
}

void RecoPFJetCollectionContainer::clear(){

  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  jesc_.clear();

  chargedHadronEnergyFraction_.clear();
  neutralHadronEnergyFraction_.clear();
  electronEnergyFraction_.clear();
  photonEnergyFraction_.clear();
  muonEnergyFraction_.clear();

  chargedHadronMultiplicity_.clear();
  neutralHadronMultiplicity_.clear();
  electronMultiplicity_.clear();
  photonMultiplicity_.clear();
  muonMultiplicity_.clear();
}

void RecoPFJetCollectionContainer::reserve(const size_t vec_size){

  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  jesc_.reserve(vec_size);

  chargedHadronEnergyFraction_.reserve(vec_size);
  neutralHadronEnergyFraction_.reserve(vec_size);
  electronEnergyFraction_.reserve(vec_size);
  photonEnergyFraction_.reserve(vec_size);
  muonEnergyFraction_.reserve(vec_size);

  chargedHadronMultiplicity_.reserve(vec_size);
  neutralHadronMultiplicity_.reserve(vec_size);
  electronMultiplicity_.reserve(vec_size);
  photonMultiplicity_.reserve(vec_size);
  muonMultiplicity_.reserve(vec_size);
}

void RecoPFJetCollectionContainer::emplace_back(const reco::PFJet& obj){

  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  const auto totFrac = obj.chargedHadronEnergyFraction() + obj.neutralHadronEnergyFraction()
   + obj.photonEnergyFraction() + obj.electronEnergyFraction() + obj.muonEnergyFraction() +
   + obj.HFEMEnergyFraction();

  jesc_.emplace_back(totFrac ? (1./totFrac) : -1.);

  chargedHadronEnergyFraction_.emplace_back(obj.chargedHadronEnergyFraction());
  neutralHadronEnergyFraction_.emplace_back(obj.neutralHadronEnergyFraction());
  electronEnergyFraction_.emplace_back(obj.electronEnergyFraction());
  photonEnergyFraction_.emplace_back(obj.photonEnergyFraction());
  muonEnergyFraction_.emplace_back(obj.muonEnergyFraction());

  chargedHadronMultiplicity_.emplace_back(obj.chargedHadronMultiplicity());
  neutralHadronMultiplicity_.emplace_back(obj.neutralHadronMultiplicity());
  electronMultiplicity_.emplace_back(obj.electronMultiplicity());
  photonMultiplicity_.emplace_back(obj.photonMultiplicity());
  muonMultiplicity_.emplace_back(obj.muonMultiplicity());
}
