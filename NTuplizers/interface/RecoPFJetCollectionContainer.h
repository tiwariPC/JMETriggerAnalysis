#ifndef JMETriggerAnalysis_RecoPFJetCollectionContainer_h
#define JMETriggerAnalysis_RecoPFJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>
#include <DataFormats/JetReco/interface/PFJetCollection.h>

#include <vector>

class RecoPFJetCollectionContainer : public VCollectionContainer<reco::PFJetCollection> {

 public:
  explicit RecoPFJetCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~RecoPFJetCollectionContainer() {}

  void clear();
  void fill(const reco::PFJetCollection&, const bool clear_before_filling=true);

  void orderByHighestPt(const bool foo){ orderByHighestPt_ = foo; }

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }

 protected:
  bool orderByHighestPt_;

  // vector of indeces (used for ordering)
  std::vector<size_t> idxs_;

  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
};

#endif
