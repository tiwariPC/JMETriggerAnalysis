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

  chargedHadronEnergyFraction_.clear();
  chargedEmEnergyFraction_.clear();
  neutralHadronEnergyFraction_.clear();
  neutralEmEnergyFraction_.clear();
  muonEnergyFraction_.clear();

  chargedMultiplicity_.clear();
  neutralMultiplicity_.clear();
  muonMultiplicity_.clear();
  electronMultiplicity_.clear();
  photonMultiplicity_.clear();
}

void RecoPFJetCollectionContainer::reserve(const size_t vec_size){

  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  chargedHadronEnergyFraction_.reserve(vec_size);
  chargedEmEnergyFraction_.reserve(vec_size);
  neutralHadronEnergyFraction_.reserve(vec_size);
  neutralEmEnergyFraction_.reserve(vec_size);
  muonEnergyFraction_.reserve(vec_size);

  chargedMultiplicity_.reserve(vec_size);
  neutralMultiplicity_.reserve(vec_size);
  muonMultiplicity_.reserve(vec_size);
  electronMultiplicity_.reserve(vec_size);
  photonMultiplicity_.reserve(vec_size);
}

void RecoPFJetCollectionContainer::emplace_back(const reco::PFJet& obj){

  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  chargedHadronEnergyFraction_.emplace_back(obj.chargedHadronEnergyFraction());
  chargedEmEnergyFraction_.emplace_back(obj.chargedEmEnergyFraction());
  neutralHadronEnergyFraction_.emplace_back(obj.neutralHadronEnergyFraction());
  neutralEmEnergyFraction_.emplace_back(obj.neutralEmEnergyFraction());
  muonEnergyFraction_.emplace_back(obj.muonEnergyFraction());

  chargedMultiplicity_.emplace_back(obj.chargedMultiplicity());
  neutralMultiplicity_.emplace_back(obj.neutralMultiplicity());
  muonMultiplicity_.emplace_back(obj.muonMultiplicity());
  electronMultiplicity_.emplace_back(obj.electronMultiplicity());
  photonMultiplicity_.emplace_back(obj.photonMultiplicity());
}
