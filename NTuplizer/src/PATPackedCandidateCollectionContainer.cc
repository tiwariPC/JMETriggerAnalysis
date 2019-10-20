#include <JMETriggerAnalysis/NTuplizer/interface/PATPackedCandidateCollectionContainer.h>

#include <numeric>
#include <algorithm>

PATPackedCandidateCollectionContainer::PATPackedCandidateCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
  : VCollectionContainer(name, inputTagLabel, token), orderByHighestPt_(false) {

  idxs_.clear();
  this->clear();
}

void PATPackedCandidateCollectionContainer::clear(){

  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  fromPV_.clear();
}

void PATPackedCandidateCollectionContainer::fill(const pat::PackedCandidateCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  pdgId_.reserve(coll.size());
  pt_.reserve(coll.size());
  eta_.reserve(coll.size());
  phi_.reserve(coll.size());
  mass_.reserve(coll.size());
  vx_.reserve(coll.size());
  vy_.reserve(coll.size());
  vz_.reserve(coll.size());
  fromPV_.reserve(coll.size());

  if(orderByHighestPt_){

    idxs_.clear();
    idxs_.reserve(coll.size());

    // initialize indeces
    for(uint idx=0; idx<coll.size(); ++idx){

      idxs_.emplace_back(idx);
    }

    // sort indeces based on pt-ordering
    std::sort(idxs_.begin(), idxs_.end(), [&coll](const size_t& i1, const size_t& i2){ return coll.at(i1).pt() > coll.at(i2).pt(); });
  }

  for(uint idx=0; idx<coll.size(); ++idx){

    const auto& i_obj = coll.at(orderByHighestPt_ ? idxs_.at(idx) : idx);

    pdgId_.emplace_back(i_obj.pdgId());
    pt_.emplace_back(i_obj.pt());
    eta_.emplace_back(i_obj.eta());
    phi_.emplace_back(i_obj.phi());
    mass_.emplace_back(i_obj.mass());
    vx_.emplace_back(i_obj.vx());
    vy_.emplace_back(i_obj.vy());
    vz_.emplace_back(i_obj.vz());
    fromPV_.emplace_back(i_obj.fromPV());
  }
}
