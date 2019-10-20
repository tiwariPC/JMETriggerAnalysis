#include <JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h>

PATMETCollectionContainer::PATMETCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : VCollectionContainer(name, inputTagLabel, token) {

  this->clear();
}

void PATMETCollectionContainer::clear(){

  Raw_pt_.clear();
  Raw_phi_.clear();
  Raw_sumEt_.clear();
  Type1_pt_.clear();
  Type1_phi_.clear();
  Type1_sumEt_.clear();
  Type1XY_pt_.clear();
  Type1XY_phi_.clear();
  Type1XY_sumEt_.clear();
  NeutralEMFraction_.clear();
  NeutralHadEtFraction_.clear();
  ChargedEMEtFraction_.clear();
  ChargedHadEtFraction_.clear();
  MuonEtFraction_.clear();
  Type6EtFraction_.clear();
  Type7EtFraction_.clear();
}

void PATMETCollectionContainer::fill(const pat::METCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  Raw_pt_.reserve(coll.size());
  Raw_phi_.reserve(coll.size());
  Raw_sumEt_.reserve(coll.size());
  Type1_pt_.reserve(coll.size());
  Type1_phi_.reserve(coll.size());
  Type1_sumEt_.reserve(coll.size());
  Type1XY_pt_.reserve(coll.size());
  Type1XY_phi_.reserve(coll.size());
  Type1XY_sumEt_.reserve(coll.size());
  NeutralEMFraction_.reserve(coll.size());
  NeutralHadEtFraction_.reserve(coll.size());
  ChargedEMEtFraction_.reserve(coll.size());
  ChargedHadEtFraction_.reserve(coll.size());
  MuonEtFraction_.reserve(coll.size());
  Type6EtFraction_.reserve(coll.size());
  Type7EtFraction_.reserve(coll.size());

  for(const auto& i_obj : coll){

    Raw_pt_.emplace_back(i_obj.shiftedPt(pat::MET::NoShift, pat::MET::Raw));
    Raw_phi_.emplace_back(i_obj.shiftedPhi(pat::MET::NoShift, pat::MET::Raw));
    Raw_sumEt_.emplace_back(i_obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Raw));
    Type1_pt_.emplace_back(i_obj.shiftedPt(pat::MET::NoShift, pat::MET::Type1));
    Type1_phi_.emplace_back(i_obj.shiftedPhi(pat::MET::NoShift, pat::MET::Type1));
    Type1_sumEt_.emplace_back(i_obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Type1));
    Type1XY_pt_.emplace_back(i_obj.shiftedPt(pat::MET::NoShift, pat::MET::Type1XY));
    Type1XY_phi_.emplace_back(i_obj.shiftedPhi(pat::MET::NoShift, pat::MET::Type1XY));
    Type1XY_sumEt_.emplace_back(i_obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Type1XY));
    NeutralEMFraction_.emplace_back(i_obj.NeutralEMFraction());
    NeutralHadEtFraction_.emplace_back(i_obj.NeutralHadEtFraction());
    ChargedEMEtFraction_.emplace_back(i_obj.ChargedEMEtFraction());
    ChargedHadEtFraction_.emplace_back(i_obj.ChargedHadEtFraction());
    MuonEtFraction_.emplace_back(i_obj.MuonEtFraction());
    Type6EtFraction_.emplace_back(i_obj.Type6EtFraction());
    Type7EtFraction_.emplace_back(i_obj.Type7EtFraction());
  }
}
