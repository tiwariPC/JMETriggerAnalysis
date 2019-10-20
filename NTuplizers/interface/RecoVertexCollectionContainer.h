#ifndef JMETriggerAnalysis_RecoVertexCollectionContainer_h
#define JMETriggerAnalysis_RecoVertexCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>
#include <DataFormats/VertexReco/interface/VertexFwd.h>

#include <vector>

class RecoVertexCollectionContainer : public VCollectionContainer<reco::VertexCollection> {

 public:
  explicit RecoVertexCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&);
  virtual ~RecoVertexCollectionContainer() {}

  void clear();
  void fill(const reco::VertexCollection&, const bool clear_before_filling=true);

  std::vector<uint>& vec_tracksSize(){ return tracksSize_; }
  std::vector<bool>& vec_isFake(){ return isFake_; }
  std::vector<float>& vec_chi2(){ return chi2_; }
  std::vector<float>& vec_ndof(){ return ndof_; }
  std::vector<float>& vec_x(){ return x_; }
  std::vector<float>& vec_y(){ return y_; }
  std::vector<float>& vec_z(){ return z_; }

 protected:
  std::vector<uint> tracksSize_;
  std::vector<bool> isFake_;
  std::vector<float> chi2_;
  std::vector<float> ndof_;
  std::vector<float> x_;
  std::vector<float> y_;
  std::vector<float> z_;
};

#endif
