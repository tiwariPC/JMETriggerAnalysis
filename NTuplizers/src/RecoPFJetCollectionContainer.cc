#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h>
#include <DataFormats/JetReco/interface/PFJet.h>

#include <numeric>
#include <algorithm>

RecoPFJetCollectionContainer::RecoPFJetCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
  : VCollectionContainer(name, inputTagLabel, token), orderByHighestPt_(false) {

  idxs_.clear();
  this->clear();
}

void RecoPFJetCollectionContainer::clear(){

  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
}

void RecoPFJetCollectionContainer::fill(const reco::PFJetCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  pt_.reserve(coll.size());
  eta_.reserve(coll.size());
  phi_.reserve(coll.size());
  mass_.reserve(coll.size());

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

    pt_.emplace_back(i_obj.pt());
    eta_.emplace_back(i_obj.eta());
    phi_.emplace_back(i_obj.phi());
    mass_.emplace_back(i_obj.mass());
  }
}
