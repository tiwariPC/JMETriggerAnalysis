#include <string>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"

template <class INP_TYPE, class OUT_TYPE>
class MultiplicityValueProducer : public edm::stream::EDProducer<> {
public:
  explicit MultiplicityValueProducer(const edm::ParameterSet&);
  ~MultiplicityValueProducer() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions&);

protected:
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<edm::View<INP_TYPE>> src_token_;
  StringCutObjectSelector<INP_TYPE, true> const strObjSelector_;
};

template <class INP_TYPE, class OUT_TYPE>
MultiplicityValueProducer<INP_TYPE, OUT_TYPE>::MultiplicityValueProducer(const edm::ParameterSet& iConfig)
  : src_token_(consumes<edm::View<INP_TYPE>>(iConfig.getParameter<edm::InputTag>("src")))
  , strObjSelector_(StringCutObjectSelector<INP_TYPE, true>(iConfig.getParameter<std::string>("cut"))) {

  produces<OUT_TYPE>();
}

template <class INP_TYPE, class OUT_TYPE>
void MultiplicityValueProducer<INP_TYPE, OUT_TYPE>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& objs(iEvent.get(src_token_));

  LogDebug("Input") << "size of input collection: " << objs.size();

  OUT_TYPE objMult(0);
  for (auto const& obj : objs) {
    if (strObjSelector_(obj)) {
      ++objMult;
    }
  }

  LogDebug("Output") << "size of selected input objects: " << objMult;

  iEvent.put(std::make_unique<double>(objMult));
}

template <class INP_TYPE, class OUT_TYPE>
void MultiplicityValueProducer<INP_TYPE, OUT_TYPE>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("input collection");
  desc.add<std::string>("cut", "")->setComment("string for StringCutObjectSelector");
  descriptions.add(defaultModuleLabel<MultiplicityValueProducer<INP_TYPE, OUT_TYPE>>(), desc);
}
