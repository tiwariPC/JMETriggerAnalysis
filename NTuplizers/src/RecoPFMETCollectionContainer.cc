#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h>
#include <DataFormats/METReco/interface/PFMET.h>

RecoPFMETCollectionContainer::RecoPFMETCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : VCollectionContainer(name, inputTagLabel, token) {

  this->clear();
}

void RecoPFMETCollectionContainer::clear(){

  pt_.clear();
  phi_.clear();
  sumEt_.clear();
  NeutralEMFraction_.clear();
  NeutralHadEtFraction_.clear();
  ChargedEMEtFraction_.clear();
  ChargedHadEtFraction_.clear();
  MuonEtFraction_.clear();
  Type6EtFraction_.clear();
  Type7EtFraction_.clear();
}

void RecoPFMETCollectionContainer::fill(const reco::PFMETCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  pt_.reserve(coll.size());
  phi_.reserve(coll.size());
  sumEt_.reserve(coll.size());
  NeutralEMFraction_.reserve(coll.size());
  NeutralHadEtFraction_.reserve(coll.size());
  ChargedEMEtFraction_.reserve(coll.size());
  ChargedHadEtFraction_.reserve(coll.size());
  MuonEtFraction_.reserve(coll.size());
  Type6EtFraction_.reserve(coll.size());
  Type7EtFraction_.reserve(coll.size());

  for(const auto& i_obj : coll){

    pt_.emplace_back(i_obj.pt());
    phi_.emplace_back(i_obj.phi());
    sumEt_.emplace_back(i_obj.sumEt());
    NeutralEMFraction_.emplace_back(i_obj.NeutralEMFraction());
    NeutralHadEtFraction_.emplace_back(i_obj.NeutralHadEtFraction());
    ChargedEMEtFraction_.emplace_back(i_obj.ChargedEMEtFraction());
    ChargedHadEtFraction_.emplace_back(i_obj.ChargedHadEtFraction());
    MuonEtFraction_.emplace_back(i_obj.MuonEtFraction());
    Type6EtFraction_.emplace_back(i_obj.Type6EtFraction());
    Type7EtFraction_.emplace_back(i_obj.Type7EtFraction());
  }
}
