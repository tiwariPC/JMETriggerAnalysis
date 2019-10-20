#include <JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h>
#include <DataFormats/VertexReco/interface/Vertex.h>

RecoVertexCollectionContainer::RecoVertexCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : VCollectionContainer(name, inputTagLabel, token) {

  this->clear();
}

void RecoVertexCollectionContainer::clear(){

  tracksSize_.clear();
  isFake_.clear();
  chi2_.clear();
  ndof_.clear();
  x_.clear();
  y_.clear();
  z_.clear();
}

void RecoVertexCollectionContainer::fill(const reco::VertexCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  tracksSize_.reserve(coll.size());
  isFake_.reserve(coll.size());
  chi2_.reserve(coll.size());
  ndof_.reserve(coll.size());
  x_.reserve(coll.size());
  y_.reserve(coll.size());
  z_.reserve(coll.size());

  for(const auto& i_obj : coll){

    tracksSize_.emplace_back(i_obj.tracksSize());
    isFake_.emplace_back(i_obj.isFake());
    chi2_.emplace_back(i_obj.chi2());
    ndof_.emplace_back(i_obj.ndof());
    x_.emplace_back(i_obj.x());
    y_.emplace_back(i_obj.y());
    z_.emplace_back(i_obj.z());
  }
}
