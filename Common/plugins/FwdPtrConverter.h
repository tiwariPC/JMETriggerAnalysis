#ifndef JMETriggerAnalysis_FwdPtrConverter_h
#define JMETriggerAnalysis_FwdPtrConverter_h

#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/stream/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/Common/interface/FwdPtr.h>

#include <memory>
#include <utility>

template<class T>
class FwdPtrConverter : public edm::stream::EDProducer<> {

 public:
  explicit FwdPtrConverter(const edm::ParameterSet&);

 private:
  void produce(edm::Event&, const edm::EventSetup&);

  edm::EDGetToken src_;
};

template<class T>
FwdPtrConverter<T>::FwdPtrConverter(const edm::ParameterSet& iConfig){

  src_ = consumes<std::vector<edm::FwdPtr<T> > >(iConfig.getParameter<edm::InputTag>("src"));

  produces<std::vector<T> >();
}

template<class T>
void FwdPtrConverter<T>::produce(edm::Event& iEvent,const edm::EventSetup& iSetup){

  edm::Handle<std::vector<edm::FwdPtr<T> > > handle;
  iEvent.getByToken(src_, handle);

  std::unique_ptr<std::vector<T> > output(new std::vector<T>());

  for(uint idx=0; idx<handle->size(); ++idx){

    output->emplace_back(*(handle->at(idx)));
  }

  iEvent.put(std::move(output));
}

#endif
