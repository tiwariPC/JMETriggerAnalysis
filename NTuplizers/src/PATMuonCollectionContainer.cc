#include <JMETriggerAnalysis/NTuplizers/interface/PATMuonCollectionContainer.h>

#include <numeric>
#include <algorithm>

PATMuonCollectionContainer::PATMuonCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
  : VCollectionContainer(name, inputTagLabel, token), orderByHighestPt_(false) {

  idxs_.clear();
  this->clear();
}

void PATMuonCollectionContainer::clear(){

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
}

void PATMuonCollectionContainer::fill(const pat::MuonCollection& coll, const bool clear_before_filling){

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
    if(i_obj.hasUserInt("IDLoose") && (i_obj.userInt("IDLoose") > 0)){ i_obj_id |= (1u << 0); }
    if(i_obj.hasUserInt("IDMedium") && (i_obj.userInt("IDMedium") > 0)){ i_obj_id |= (1u << 1); }
    if(i_obj.hasUserInt("IDTight") && (i_obj.userInt("IDTight") > 0)){ i_obj_id |= (1u << 2); }
    if(i_obj.hasUserInt("IDSoft") && (i_obj.userInt("IDSoft") > 0)){ i_obj_id |= (1u << 3); }
    if(i_obj.hasUserInt("IDHighPt") && (i_obj.userInt("IDHighPt") > 0)){ i_obj_id |= (1u << 4); }
    if(i_obj.hasUserInt("IDHighPtTRK") && (i_obj.userInt("IDHighPtTRK") > 0)){ i_obj_id |= (1u << 5); }
    if(i_obj.hasUserInt("IDLooseHZZ") && (i_obj.userInt("IDLooseHZZ") > 0)){ i_obj_id |= (1u << 6); }
    if(i_obj.hasUserInt("IDTightHZZ") && (i_obj.userInt("IDTightHZZ") > 0)){ i_obj_id |= (1u << 7); }
    id_.emplace_back(i_obj_id);

    pfIso_.emplace_back(i_obj.hasUserFloat("pfIsoR04") ? i_obj.userFloat("pfIsoR04") : -9999.);
  }
}
