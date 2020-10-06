#include <vector>
#include <memory>
#include <utility>
#include <algorithm>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/Utils/interface/PtComparator.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"

template <class JET_TYPE>
class CorrectedWithTextFilesJetProducer : public edm::stream::EDProducer<> {
public:
  explicit CorrectedWithTextFilesJetProducer(const edm::ParameterSet&);
  ~CorrectedWithTextFilesJetProducer() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions&);

protected:
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<edm::View<JET_TYPE>> token_jets_;
  const edm::FileInPath textFile_;
  const bool useRho_;
  const edm::EDGetTokenT<double> token_rho_;

  std::unique_ptr<FactorizedJetCorrector> factorizedJetCorrector_;
};

template <class JET_TYPE>
CorrectedWithTextFilesJetProducer<JET_TYPE>::CorrectedWithTextFilesJetProducer(const edm::ParameterSet& iConfig)
    : token_jets_(consumes<edm::View<JET_TYPE>>(iConfig.getParameter<edm::InputTag>("src"))),
      textFile_(iConfig.getParameter<edm::FileInPath>("textFile")),
      useRho_(iConfig.getParameter<bool>("useRho")),
      token_rho_(useRho_ ? consumes<double>(iConfig.getParameter<edm::InputTag>("rho")) : edm::EDGetTokenT<double>()) {
  std::vector<JetCorrectorParameters> jetCorrectorParameters({JetCorrectorParameters(textFile_.fullPath())});
  factorizedJetCorrector_.reset(new FactorizedJetCorrector(jetCorrectorParameters));

  produces<std::vector<JET_TYPE>>();
}

template <class JET_TYPE>
void CorrectedWithTextFilesJetProducer<JET_TYPE>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& jets(iEvent.get(token_jets_));

  LogDebug("Input") << "size of input jet collection: " << jets.size();

  auto out_jets = std::make_unique<std::vector<JET_TYPE>>();
  out_jets->reserve(jets.size());

  double const rho(useRho_ ? iEvent.get(token_rho_) : 0.);

  for (auto const& jet : jets) {
    out_jets->emplace_back(jet);
    auto& outJet(out_jets->back());

    factorizedJetCorrector_->setJetEta(jet.eta());
    factorizedJetCorrector_->setJetPt(jet.pt());
    factorizedJetCorrector_->setJetA(jet.jetArea());
    if (useRho_) {
      factorizedJetCorrector_->setRho(rho);
    }

    outJet.scaleEnergy(factorizedJetCorrector_->getCorrection());

    LogDebug("Output") << "output jet: pt=" << outJet.pt() << ", eta=" << outJet.eta() << ", phi=" << outJet.phi()
                       << ", mass=" << outJet.mass() << ", jesc=" << factorizedJetCorrector_->getCorrection();
  }

  NumericSafeGreaterByPt<JET_TYPE> jetComp;
  std::sort(out_jets->begin(), out_jets->end(), jetComp);

  LogDebug("Output") << "size of output jet collection: " << out_jets->size();

  iEvent.put(std::move(out_jets));
}

template <class JET_TYPE>
void CorrectedWithTextFilesJetProducer<JET_TYPE>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("input collection of jets");
  desc.add<edm::FileInPath>("textFile")->setComment("text file (edm::FileInPath) for JES corrections");
  desc.add<bool>("useRho", false)->setComment("use event rho for JESC computation");
  desc.addOptional<edm::InputTag>("rho")->setComment("event rho for JESC computation");
  descriptions.add(defaultModuleLabel<CorrectedWithTextFilesJetProducer<JET_TYPE>>(), desc);
}
