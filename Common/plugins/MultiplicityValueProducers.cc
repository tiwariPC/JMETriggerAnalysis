#include "JMETriggerAnalysis/Common/plugins/MultiplicityValueProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef MultiplicityValueProducer<reco::Track, double> TrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(TrackMultiplicityValueProducer);

typedef MultiplicityValueProducer<reco::Vertex, double> VertexMultiplicityValueProducer;
DEFINE_FWK_MODULE(VertexMultiplicityValueProducer);
