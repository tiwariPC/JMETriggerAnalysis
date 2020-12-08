#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMETriggerAnalysis/Common/plugins/CorrectedJetAnalyzer.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"

typedef CorrectedJetAnalyzer<reco::CaloJet> CorrectedCaloJetAnalyzer;
DEFINE_FWK_MODULE(CorrectedCaloJetAnalyzer);

typedef CorrectedJetAnalyzer<reco::PFJet> CorrectedPFJetAnalyzer;
DEFINE_FWK_MODULE(CorrectedPFJetAnalyzer);
