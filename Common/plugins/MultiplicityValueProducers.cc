#include "JMETriggerAnalysis/Common/plugins/MultiplicityValueProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"

typedef MultiplicityValueProducer<reco::Track, double> TrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(TrackMultiplicityValueProducer);
