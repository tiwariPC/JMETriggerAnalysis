#include <JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h>

#include <numeric>
#include <algorithm>

PATElectronCollectionContainer::PATElectronCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
  : VCollectionContainer(name, inputTagLabel, token), orderByHighestPt_(false) {

  idxs_.clear();
  this->clear();
}

void PATElectronCollectionContainer::clear(){

  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  dxyPV_.clear();
  dzPV_.clear();
  id_.clear();
  pfIso_.clear();
  etaSC_.clear();
}

void PATElectronCollectionContainer::fill(const pat::ElectronCollection& coll, const bool clear_before_filling){

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
  dxyPV_.reserve(coll.size());
  dzPV_.reserve(coll.size());
  id_.reserve(coll.size());
  pfIso_.reserve(coll.size());
  etaSC_.reserve(coll.size());

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

    dxyPV_.emplace_back(i_obj.hasUserFloat("dxyPV") ? i_obj.userFloat("dxyPV") : -9999.);
    dzPV_.emplace_back(i_obj.hasUserFloat("dzPV") ? i_obj.userFloat("dzPV") : -9999.);

    uint i_obj_id(0);
    if(i_obj.hasUserInt("IDCutBasedVeto") && (i_obj.userInt("IDCutBasedVeto") > 0)){ i_obj_id |= (1u << 0); }
    if(i_obj.hasUserInt("IDCutBasedLoose") && (i_obj.userInt("IDCutBasedLoose") > 0)){ i_obj_id |= (1u << 1); }
    if(i_obj.hasUserInt("IDCutBasedMedium") && (i_obj.userInt("IDCutBasedMedium") > 0)){ i_obj_id |= (1u << 2); }
    if(i_obj.hasUserInt("IDCutBasedTight") && (i_obj.userInt("IDCutBasedTight") > 0)){ i_obj_id |= (1u << 3); }
    if(i_obj.hasUserInt("IDMVAIsoWP80") && (i_obj.userInt("IDMVAIsoWP80") > 0)){ i_obj_id |= (1u << 4); }
    if(i_obj.hasUserInt("IDMVAIsoWP90") && (i_obj.userInt("IDMVAIsoWP90") > 0)){ i_obj_id |= (1u << 5); }
    id_.emplace_back(i_obj_id);

    pfIso_.emplace_back(i_obj.hasUserFloat("pfIso") ? i_obj.userFloat("pfIso") : -9999.);
  }
}
