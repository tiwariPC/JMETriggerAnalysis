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
  std::vector<float>& vec_NeutralEMFraction(){ return NeutralEMFraction_; }
  std::vector<float>& vec_NeutralHadEtFraction(){ return NeutralHadEtFraction_; }
  std::vector<float>& vec_ChargedEMEtFraction(){ return ChargedEMEtFraction_; }
  std::vector<float>& vec_ChargedHadEtFraction(){ return ChargedHadEtFraction_; }
  std::vector<float>& vec_MuonEtFraction(){ return MuonEtFraction_; }
  std::vector<float>& vec_Type6EtFraction(){ return Type6EtFraction_; }
  std::vector<float>& vec_Type7EtFraction(){ return Type7EtFraction_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
  std::vector<float> NeutralEMFraction_;
  std::vector<float> NeutralHadEtFraction_;
  std::vector<float> ChargedEMEtFraction_;
  std::vector<float> ChargedHadEtFraction_;
  std::vector<float> MuonEtFraction_;
  std::vector<float> Type6EtFraction_;
  std::vector<float> Type7EtFraction_;
};

#endif
