#ifndef JMETriggerAnalysis_PATPackedCandidateCollectionContainer_h
#define JMETriggerAnalysis_PATPackedCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizer/interface/VCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/PackedCandidate.h>

#include <vector>

class PATPackedCandidateCollectionContainer : public VCollectionContainer<pat::PackedCandidateCollection> {

 public:
  explicit PATPackedCandidateCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~PATPackedCandidateCollectionContainer() {}

  void clear();
  void fill(const pat::PackedCandidateCollection&, const bool clear_before_filling=true);

  void orderByHighestPt(const bool foo){ orderByHighestPt_ = foo; }

  std::vector<int>& vec_pdgId(){ return pdgId_; }
  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }
  std::vector<float>& vec_vx(){ return vx_; }
  std::vector<float>& vec_vy(){ return vy_; }
  std::vector<float>& vec_vz(){ return vz_; }
  std::vector<int>& vec_fromPV(){ return fromPV_; }

 protected:
  bool orderByHighestPt_;

  // vector of indeces (used for ordering)
  std::vector<size_t> idxs_;

  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<int> fromPV_;
};

#endif
