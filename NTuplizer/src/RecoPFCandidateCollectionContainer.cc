#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFCandidateCollectionContainer.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

RecoPFCandidateCollectionContainer::RecoPFCandidateCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : VCollectionContainer(name, inputTagLabel, token) {

  this->clear();
}

void RecoPFCandidateCollectionContainer::clear(){

  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
}

void RecoPFCandidateCollectionContainer::fill(const reco::PFCandidateCollection& coll){

  pdgId_.reserve(coll.size());
  pt_.reserve(coll.size());
  eta_.reserve(coll.size());
  phi_.reserve(coll.size());
  mass_.reserve(coll.size());
  vx_.reserve(coll.size());
  vy_.reserve(coll.size());
  vz_.reserve(coll.size());

  for(const auto& i_obj : coll){

    pdgId_.emplace_back(i_obj.pdgId());
    pt_.emplace_back(i_obj.pt());
    eta_.emplace_back(i_obj.eta());
    phi_.emplace_back(i_obj.phi());
    mass_.emplace_back(i_obj.mass());
    vx_.emplace_back(i_obj.vx());
    vy_.emplace_back(i_obj.vy());
    vz_.emplace_back(i_obj.vz());
  }
}
