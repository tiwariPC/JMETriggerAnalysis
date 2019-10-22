#ifndef JMETriggerAnalysis_RecoCaloMETCollectionContainer_h
#define JMETriggerAnalysis_RecoCaloMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/METReco/interface/CaloMET.h>

class RecoCaloMETCollectionContainer : public VRecoCandidateCollectionContainer<reco::CaloMET> {

 public:
  explicit RecoCaloMETCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&, const std::string& strCut="", const bool orderByHighestPt=false);
  virtual ~RecoCaloMETCollectionContainer() {}

  void clear();
  void reserve(const size_t);
  void emplace_back(const reco::CaloMET&);

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_sumEt(){ return sumEt_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
};

#endif
