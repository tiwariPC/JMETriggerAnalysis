#ifndef JMETriggerAnalysis_PATPhotonCollectionContainer_h
#define JMETriggerAnalysis_PATPhotonCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/Photon.h>

class PATPhotonCollectionContainer : public VRecoCandidateCollectionContainer<pat::Photon> {
public:
  explicit PATPhotonCollectionContainer(const std::string&,
                                          const std::string&,
                                          const edm::EDGetToken&,
                                          const std::string& strCut = "",
                                          const bool orderByHighestPt = false);
  ~PATPhotonCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const pat::Photon&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }
  std::vector<float>& vec_dxyPV() { return dxyPV_; }
  std::vector<float>& vec_dzPV() { return dzPV_; }
  std::vector<uint>& vec_id() { return id_; }
  std::vector<float>& vec_pfIso() { return pfIso_; }
  std::vector<float>& vec_etaSC() { return etaSC_; }

protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<float> dxyPV_;
  std::vector<float> dzPV_;
  std::vector<uint> id_;
  std::vector<float> pfIso_;
  std::vector<float> etaSC_;
};

#endif
