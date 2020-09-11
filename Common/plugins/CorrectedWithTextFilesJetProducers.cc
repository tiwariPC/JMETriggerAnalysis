#include "JMETriggerAnalysis/Common/plugins/CorrectedWithTextFilesJetProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/JPTJet.h"
#include "DataFormats/JetReco/interface/PFClusterJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/TrackJet.h"

typedef CorrectedWithTextFilesJetProducer<reco::CaloJet> CorrectedWithTextFilesCaloJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesCaloJetProducer);

typedef CorrectedWithTextFilesJetProducer<reco::GenJet> CorrectedWithTextFilesGenJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesGenJetProducer);

typedef CorrectedWithTextFilesJetProducer<reco::JPTJet> CorrectedWithTextFilesJPTJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesJPTJetProducer);

typedef CorrectedWithTextFilesJetProducer<reco::PFClusterJet> CorrectedWithTextFilesPFClusterJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesPFClusterJetProducer);

typedef CorrectedWithTextFilesJetProducer<reco::PFJet> CorrectedWithTextFilesPFJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesPFJetProducer);

typedef CorrectedWithTextFilesJetProducer<reco::TrackJet> CorrectedWithTextFilesTrackJetProducer;
DEFINE_FWK_MODULE(CorrectedWithTextFilesTrackJetProducer);
