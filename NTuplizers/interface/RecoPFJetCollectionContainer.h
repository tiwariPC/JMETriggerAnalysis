#ifndef JMETriggerAnalysis_RecoPFJetCollectionContainer_h
#define JMETriggerAnalysis_RecoPFJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/JetReco/interface/PFJet.h>

class RecoPFJetCollectionContainer : public VRecoCandidateCollectionContainer<reco::PFJet> {

 public:
  explicit RecoPFJetCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&, const std::string& strCut="", const bool orderByHighestPt=false);
  virtual ~RecoPFJetCollectionContainer() {}

  void clear();
  void reserve(const size_t);
  void emplace_back(const reco::PFJet&);

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }

  std::vector<float>& vec_chargedHadronEnergyFraction(){ return chargedHadronEnergyFraction_; }
  std::vector<float>& vec_chargedEmEnergyFraction(){ return chargedEmEnergyFraction_; }
  std::vector<float>& vec_neutralHadronEnergyFraction(){ return neutralHadronEnergyFraction_; }
  std::vector<float>& vec_neutralEmEnergyFraction(){ return neutralEmEnergyFraction_; }
  std::vector<float>& vec_muonEnergyFraction(){ return muonEnergyFraction_; }

  std::vector<int>& vec_chargedMultiplicity(){ return chargedMultiplicity_; }
  std::vector<int>& vec_neutralMultiplicity(){ return neutralMultiplicity_; }
  std::vector<int>& vec_muonMultiplicity(){ return muonMultiplicity_; }
  std::vector<int>& vec_electronMultiplicity(){ return electronMultiplicity_; }
  std::vector<int>& vec_photonMultiplicity(){ return photonMultiplicity_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

  std::vector<float> chargedHadronEnergyFraction_;
  std::vector<float> chargedEmEnergyFraction_;
  std::vector<float> neutralHadronEnergyFraction_;
  std::vector<float> neutralEmEnergyFraction_;
  std::vector<float> muonEnergyFraction_;

  std::vector<int> chargedMultiplicity_;
  std::vector<int> neutralMultiplicity_;
  std::vector<int> muonMultiplicity_;
  std::vector<int> electronMultiplicity_;
  std::vector<int> photonMultiplicity_;
};

#endif
