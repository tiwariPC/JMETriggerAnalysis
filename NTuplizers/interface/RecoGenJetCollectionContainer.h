#ifndef JMETriggerAnalysis_RecoGenJetCollectionContainer_h
#define JMETriggerAnalysis_RecoGenJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/JetReco/interface/GenJet.h>

class RecoGenJetCollectionContainer : public VRecoCandidateCollectionContainer<reco::GenJet> {

 public:
  explicit RecoGenJetCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&, const std::string& strCut="", const bool orderByHighestPt=false);
  virtual ~RecoGenJetCollectionContainer() {}

  void clear();
  void reserve(const size_t);
  void emplace_back(const reco::GenJet&);

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }

  std::vector<uint>& vec_numberOfDaughters(){ return numberOfDaughters_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

  std::vector<uint> numberOfDaughters_;
};

#endif
