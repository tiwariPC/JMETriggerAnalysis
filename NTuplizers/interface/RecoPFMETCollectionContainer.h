#ifndef JMETriggerAnalysis_RecoPFMETCollectionContainer_h
#define JMETriggerAnalysis_RecoPFMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>
#include <DataFormats/METReco/interface/PFMETFwd.h>

#include <vector>

class RecoPFMETCollectionContainer : public VCollectionContainer<reco::PFMETCollection> {

 public:
  explicit RecoPFMETCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~RecoPFMETCollectionContainer() {}

  void clear();
  void fill(const reco::PFMETCollection&, const bool clear_before_filling=true);

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_sumEt(){ return sumEt_; }
  std::vector<float>& vec_photonEtFraction(){ return photonEtFraction_; }
  std::vector<float>& vec_neutralHadronEtFraction(){ return neutralHadronEtFraction_; }
  std::vector<float>& vec_electronEtFraction(){ return electronEtFraction_; }
  std::vector<float>& vec_chargedHadronEtFraction(){ return chargedHadronEtFraction_; }
  std::vector<float>& vec_muonEtFraction(){ return muonEtFraction_; }
  std::vector<float>& vec_HFHadronEtFraction(){ return HFHadronEtFraction_; }
  std::vector<float>& vec_HFEMEtFraction(){ return HFEMEtFraction_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
  std::vector<float> photonEtFraction_;
  std::vector<float> neutralHadronEtFraction_;
  std::vector<float> electronEtFraction_;
  std::vector<float> chargedHadronEtFraction_;
  std::vector<float> muonEtFraction_;
  std::vector<float> HFHadronEtFraction_;
  std::vector<float> HFEMEtFraction_;
};

#endif
