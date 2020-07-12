#ifndef JMETriggerAnalysis_RecoPFClusterMETCollectionContainer_h
#define JMETriggerAnalysis_RecoPFClusterMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/METReco/interface/PFClusterMET.h>

class RecoPFClusterMETCollectionContainer : public VRecoCandidateCollectionContainer<reco::PFClusterMET> {
public:
  explicit RecoPFClusterMETCollectionContainer(const std::string&,
                                               const std::string&,
                                               const edm::EDGetToken&,
                                               const std::string& strCut = "",
                                               const bool orderByHighestPt = false);
  virtual ~RecoPFClusterMETCollectionContainer() {}

  void clear();
  void reserve(const size_t);
  void emplace_back(const reco::PFClusterMET&);

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_sumEt() { return sumEt_; }

protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
};

#endif
