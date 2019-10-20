#ifndef JMETriggerAnalysis_RecoPFCandidateCollectionContainer_h
#define JMETriggerAnalysis_RecoPFCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizer/interface/VCollectionContainer.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h>

#include <vector>

class RecoPFCandidateCollectionContainer : public VCollectionContainer<reco::PFCandidateCollection> {

 public:
  explicit RecoPFCandidateCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~RecoPFCandidateCollectionContainer() {}

  void clear();
  void fill(const reco::PFCandidateCollection&, const bool clear_before_filling=true);

  std::vector<int>& vec_pdgId(){ return pdgId_; }
  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }
  std::vector<float>& vec_vx(){ return vx_; }
  std::vector<float>& vec_vy(){ return vy_; }
  std::vector<float>& vec_vz(){ return vz_; }

 protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
};

#endif
