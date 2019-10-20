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
  photonEtFraction_.clear();
  neutralHadronEtFraction_.clear();
  electronEtFraction_.clear();
  chargedHadronEtFraction_.clear();
  muonEtFraction_.clear();
  HFHadronEtFraction_.clear();
  HFEMEtFraction_.clear();
}

void RecoPFMETCollectionContainer::fill(const reco::PFMETCollection& coll, const bool clear_before_filling){

  if(clear_before_filling){

    this->clear();
  }

  pt_.reserve(coll.size());
  phi_.reserve(coll.size());
  sumEt_.reserve(coll.size());
  photonEtFraction_.reserve(coll.size());
  neutralHadronEtFraction_.reserve(coll.size());
  electronEtFraction_.reserve(coll.size());
  chargedHadronEtFraction_.reserve(coll.size());
  muonEtFraction_.reserve(coll.size());
  HFHadronEtFraction_.reserve(coll.size());
  HFEMEtFraction_.reserve(coll.size());

  for(const auto& i_obj : coll){

    pt_.emplace_back(i_obj.pt());
    phi_.emplace_back(i_obj.phi());
    sumEt_.emplace_back(i_obj.sumEt());
    photonEtFraction_.emplace_back(i_obj.photonEtFraction());
    neutralHadronEtFraction_.emplace_back(i_obj.neutralHadronEtFraction());
    electronEtFraction_.emplace_back(i_obj.electronEtFraction());
    chargedHadronEtFraction_.emplace_back(i_obj.chargedHadronEtFraction());
    muonEtFraction_.emplace_back(i_obj.muonEtFraction());
    HFHadronEtFraction_.emplace_back(i_obj.HFHadronEtFraction());
    HFEMEtFraction_.emplace_back(i_obj.HFEMEtFraction());
  }
}
