#include <JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h>

PATJetCollectionContainer::PATJetCollectionContainer(
  const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token, const std::string& strCut, const bool orderByHighestPt
) : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {
}

void PATJetCollectionContainer::clear(){

  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  jesc_.clear();

  chargedHadronEnergyFraction_.clear();
  chargedEmEnergyFraction_.clear();
  neutralHadronEnergyFraction_.clear();
  neutralEmEnergyFraction_.clear();
  muonEnergyFraction_.clear();

  chargedHadronMultiplicity_.clear();
  neutralHadronMultiplicity_.clear();
  muonMultiplicity_.clear();
  electronMultiplicity_.clear();
  photonMultiplicity_.clear();
}

void PATJetCollectionContainer::reserve(const size_t vec_size){

  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  jesc_.reserve(vec_size);

  chargedHadronEnergyFraction_.reserve(vec_size);
  chargedEmEnergyFraction_.reserve(vec_size);
  neutralHadronEnergyFraction_.reserve(vec_size);
  neutralEmEnergyFraction_.reserve(vec_size);
  muonEnergyFraction_.reserve(vec_size);

  chargedHadronMultiplicity_.reserve(vec_size);
  neutralHadronMultiplicity_.reserve(vec_size);
  muonMultiplicity_.reserve(vec_size);
  electronMultiplicity_.reserve(vec_size);
  photonMultiplicity_.reserve(vec_size);
}

void PATJetCollectionContainer::emplace_back(const pat::Jet& obj){

  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  jesc_.emplace_back(obj.jecFactor("Uncorrected") ? (1./obj.jecFactor("Uncorrected")) : 1.);

  chargedHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.chargedHadronEnergyFraction() : -99.);
  chargedEmEnergyFraction_.emplace_back(obj.isPFJet() ? obj.chargedEmEnergyFraction() : -99.);
  neutralHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.neutralHadronEnergyFraction() : -99.);
  neutralEmEnergyFraction_.emplace_back(obj.isPFJet() ? obj.neutralEmEnergyFraction() : -99.);
  muonEnergyFraction_.emplace_back(obj.isPFJet() ? obj.muonEnergyFraction() : -99.);

  chargedHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.chargedHadronMultiplicity() : -1);
  neutralHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.neutralHadronMultiplicity() : -1);
  muonMultiplicity_.emplace_back(obj.isPFJet() ? obj.muonMultiplicity() : -1);
  electronMultiplicity_.emplace_back(obj.isPFJet() ? obj.electronMultiplicity() : -1);
  photonMultiplicity_.emplace_back(obj.isPFJet() ? obj.photonMultiplicity() : -1);
}
