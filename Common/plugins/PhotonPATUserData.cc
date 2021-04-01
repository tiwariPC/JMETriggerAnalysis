#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <CommonTools/Utils/interface/StringCutObjectSelector.h>
#include <CommonTools/Utils/interface/StringObjectFunction.h>
#include <DataFormats/Common/interface/ValueMap.h>
#include <DataFormats/PatCandidates/interface/Photon.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include <DataFormats/VertexReco/interface/VertexFwd.h>
#include <CommonTools/Egamma/interface/EffectiveAreas.h>

#include <string>
#include <vector>
#include <memory>
#include <utility>

class PhotonPATUserData : public edm::EDProducer {

 public:
  explicit PhotonPATUserData(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions&);

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  edm::EDGetToken src_;

  std::vector<std::string>     vmaps_bool_;
  std::vector<edm::EDGetToken> vmaps_bool_token_;

  std::vector<std::string>     vmaps_float_;
  std::vector<edm::EDGetToken> vmaps_float_token_;

  std::vector<std::pair<std::string, std::string> > v_float_copycats_;

  std::vector<std::pair<std::string, StringCutObjectSelector<pat::Photon, true> > > userInt_stringSelects_;
  std::vector<std::pair<std::string, StringObjectFunction   <pat::Photon, true> > > userFloat_stringFuncs_;

  edm::EDGetTokenT<edm::View<reco::Vertex> > primaryVertices_;

  EffectiveAreas effAreas_;
  edm::EDGetToken rho_;
};

PhotonPATUserData::PhotonPATUserData(const edm::ParameterSet& iConfig)
  : effAreas_(iConfig.getParameter<edm::FileInPath>("effAreas_file").fullPath()) {

  src_ = consumes<edm::View<pat::Photon> >(iConfig.getParameter<edm::InputTag>("src"));

  // ValueMaps [bool]
  vmaps_bool_ = iConfig.exists("valueMaps_bool") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_bool") : std::vector<std::string>();

  for(const auto& vm_str : vmaps_bool_)
  {
    vmaps_bool_token_.emplace_back(consumes<edm::ValueMap<bool> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // ValueMaps [float]
  vmaps_float_ = iConfig.exists("valueMaps_float") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_float") : std::vector<std::string>();

  for(const auto& vm_str : vmaps_float_)
  {
    vmaps_float_token_.emplace_back(consumes<edm::ValueMap<float> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // PSet for userFloat copycat(s)
  const edm::ParameterSet pset_userFloat_copycat = iConfig.exists("userFloat_copycat") ? iConfig.getParameter<edm::ParameterSet>("userFloat_copycat") : edm::ParameterSet();
  for(unsigned int i=0; i<pset_userFloat_copycat.getParameterNames().size(); ++i)
  {
    const std::string pset_arg = pset_userFloat_copycat.getParameterNames().at(i);
    const std::string pset_val = pset_userFloat_copycat.getParameter<std::string>(pset_arg);

    v_float_copycats_.emplace_back(std::make_pair(pset_arg, pset_val));
  }
  // -----------------

  // PSet for userInts from StringCutObjectSelector(s)
  const edm::ParameterSet& pset_userInt_stringSelects = iConfig.exists("userInt_stringSelectors") ? iConfig.getParameter<edm::ParameterSet>("userInt_stringSelectors") : edm::ParameterSet();
  for(const std::string& vname : pset_userInt_stringSelects.getParameterNamesForType<std::string>())
  {
    userInt_stringSelects_.emplace_back(std::pair<std::string, StringCutObjectSelector<pat::Photon, true> >(vname, pset_userInt_stringSelects.getParameter<std::string>(vname)));
  }
  // -----------------

  // PSet for userFloats from StringObjectFunction(s)
  const edm::ParameterSet& pset_userFloat_stringFuncs = iConfig.exists("userFloat_stringFunctions") ? iConfig.getParameter<edm::ParameterSet>("userFloat_stringFunctions") : edm::ParameterSet();
  for(const std::string& vname : pset_userFloat_stringFuncs.getParameterNamesForType<std::string>())
  {
    userFloat_stringFuncs_.emplace_back(std::pair<std::string, StringObjectFunction<pat::Photon, true> >(vname, pset_userFloat_stringFuncs.getParameter<std::string>(vname)));
  }
  // -----------------

  primaryVertices_ = consumes<edm::View<reco::Vertex> >(iConfig.getParameter<edm::InputTag>("primaryVertices"));

  rho_ = consumes<double>(iConfig.getParameter<edm::InputTag>("rho"));

  produces<pat::PhotonCollection>();
}

void PhotonPATUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<edm::View<pat::Photon> > patElecs;
  iEvent.getByToken(src_, patElecs);

  // ValueMaps [bool]
  std::vector<edm::Handle<edm::ValueMap<bool> > > v_vmap_bool;
  for(unsigned int i=0; i<vmaps_bool_token_.size(); ++i)
  {
    edm::Handle<edm::ValueMap<bool> > vmap;
    iEvent.getByToken(vmaps_bool_token_.at(i), vmap);
    v_vmap_bool.emplace_back(vmap);
  }
  // -----------------

  // ValueMaps [float]
  std::vector<edm::Handle<edm::ValueMap<float> > > v_vmap_float;
  for(unsigned int i=0; i<vmaps_float_token_.size(); ++i)
  {
    edm::Handle<edm::ValueMap<float> > vmap;
    iEvent.getByToken(vmaps_float_token_.at(i), vmap);
    v_vmap_float.emplace_back(vmap);
  }
  // -----------------

  // PV
  edm::Handle<edm::View<reco::Vertex> > recoVtxs;
  iEvent.getByToken(primaryVertices_, recoVtxs);

  const auto* PV = (recoVtxs->size() > 0) ? &(recoVtxs->at(0)) : nullptr;

  if(not PV){

    edm::LogWarning("Input") << "@@@ PhotonPATUserData::produce -- empty collection of primary vertices";
  }
  // -----------------

  // Rho
  edm::Handle<double> rho_h;
  iEvent.getByToken(rho_, rho_h);
  const float rho = float(*rho_h);
  // -----------------

  std::unique_ptr<pat::PhotonCollection> newElecs(new pat::PhotonCollection);
  newElecs->reserve(patElecs->size());

  for(unsigned int i_ele=0; i_ele<patElecs->size(); ++i_ele){

    newElecs->emplace_back(patElecs->at(i_ele));
    pat::Photon& pho = newElecs->back();

    // ValueMaps [bool]
    for(unsigned int i=0; i<v_vmap_bool.size(); ++i)
    {
      if(pho.hasUserInt(vmaps_bool_.at(i)))
      {
        throw cms::Exception("InputError")
	  << "@@@ PhotonPATUserData::produce -- PAT user-int label already exists: " << vmaps_bool_.at(i);
      }

      if(v_vmap_bool.at(i)->contains(patElecs->refAt(i_ele).id()))
      {
        const bool val = (*(v_vmap_bool.at(i)))[patElecs->refAt(i_ele)];
        pho.addUserInt(vmaps_bool_.at(i), int(val));
      }
      else
      {
        throw cms::Exception("InputError")
          << "@@@ PhotonPATUserData::produce -- object reference not found in ValueMap<bool> \"" << vmaps_bool_.at(i) << "\"";
      }
    }
    // -----------------

    // ValueMaps [float]
    for(unsigned int i=0; i<v_vmap_float.size(); ++i)
    {
      if(pho.hasUserFloat(vmaps_float_.at(i)))
      {
        throw cms::Exception("InputError")
	  << "@@@ PhotonPATUserData::produce -- PAT user-float label already exists: " << vmaps_float_.at(i);
      }

      if(v_vmap_float.at(i)->contains(patElecs->refAt(i_ele).id()))
      {
        const float val = (*(v_vmap_float.at(i)))[patElecs->refAt(i_ele)];
        pho.addUserFloat(vmaps_float_.at(i), val);
      }
      else
      {
        throw cms::Exception("InputError")
          << "@@@ PhotonPATUserData::produce -- object reference not found in ValueMap<float> \"" << vmaps_float_.at(i) << "\"";
      }
    }
    // -----------------

    // userFloat copycat(s)
    for(const auto& userfloat_copycat : v_float_copycats_)
    {
      const std::string& ref = userfloat_copycat.second;
      const std::string& out = userfloat_copycat.first;

      if(pho.hasUserFloat(ref) == false)
      {
        throw cms::Exception("InputError") << "@@@ PhotonPATUserData::produce -- PAT user-float key \""+ref+"\" not found";
      }

      if(pho.hasUserFloat(out) == true)
      {
        throw cms::Exception("InputError") << "@@@ PhotonPATUserData::produce -- target PAT user-float key \""+out+"\" already exists";
      }

      pho.addUserFloat(out, pho.userFloat(ref));
    }
    // -----------------

    // Impact Parameter(s)
    const float dxyPV((PV && pho.gsfTrack().isNonnull()) ? pho.gsfTrack()->dxy(PV->position()) : -9999.);
    const float dzPV ((PV && pho.gsfTrack().isNonnull()) ? pho.gsfTrack()->dz (PV->position()) : -9999.);

    pho.addUserFloat("dxyPV", dxyPV);
    pho.addUserFloat("dzPV", dzPV);

    const float SIP3D = ((pho.edB(pat::Photon::PV3D) != 0.) ? (pho.dB(pat::Photon::PV3D) / pho.edB(pat::Photon::PV3D)) : +9999.);
    pho.addUserFloat("SIP3D", SIP3D);
    // -----------------

    // PF-Isolation used for EGamma Cut-Based ID
    //  * "${CMSSW_BASE}"/src/RecoEgamma/PhotonIdentification/python/Identification/cutBasedPhotonID_tools.py
    //  * "${CMSSW_BASE}"/src/RecoEgamma/PhotonIdentification/plugins/cuts/GsfEleEffAreaPFIsoCut.cc
    const float pfIso_CH(pho.pfIsolationVariables().sumChargedHadronPt);
    const float pfIso_NH(pho.pfIsolationVariables().sumNeutralHadronEt);
    const float pfIso_Ph(pho.pfIsolationVariables().sumPhotonEt);
    const float pfIso_rA(rho * effAreas_.getEffectiveArea(fabs(pho.superCluster()->eta())));

    const float pfIso = (pho.pt() != 0.) ? ((pfIso_CH + std::max(0.0f, pfIso_NH + pfIso_Ph - pfIso_rA)) / pho.pt()) : -1.;

    pho.addUserFloat("pfIso_CH", pfIso_CH);
    pho.addUserFloat("pfIso_NH", pfIso_NH);
    pho.addUserFloat("pfIso_Ph", pfIso_Ph);
    pho.addUserFloat("pfIso_rA", pfIso_rA);
    pho.addUserFloat("pfIso", pfIso);
    // -----------------

    // Selectors [int]
    for(const auto& i_strNfunc : userInt_stringSelects_)
    {
      const auto& i_str  = i_strNfunc.first;
      const auto& i_func = i_strNfunc.second;

      if(pho.hasUserInt(i_str))
      {
        throw cms::Exception("InputError") << "@@@ PhotonPATUserData::produce -- PAT user-int label already exists: " << i_str;
      }

      pho.addUserInt(i_str, int(i_func(pho)));
    }
    // -----------------

    // Functions [float]
    for(const auto& i_strNfunc : userFloat_stringFuncs_)
    {
      const auto& i_str  = i_strNfunc.first;
      const auto& i_func = i_strNfunc.second;

      if(pho.hasUserFloat(i_str))
      {
        throw cms::Exception("InputError") << "@@@ PhotonPATUserData::produce -- PAT user-float label already exists: " << i_str;
      }

      pho.addUserFloat(i_str, float(i_func(pho)));
    }
    // -----------------
  }

  iEvent.put(std::move(newElecs));

  return;
}

void PhotonPATUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions){

  edm::ParameterSetDescription desc;
  desc.setUnknown();

  descriptions.add("PhotonPATUserData", desc);
}

DEFINE_FWK_MODULE(PhotonPATUserData);
