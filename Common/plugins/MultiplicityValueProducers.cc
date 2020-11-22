#include "JMETriggerAnalysis/Common/plugins/MultiplicityValueProducers.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef MultiplicityValueProducerFromNestedCollection<SiPixelClusterCollectionNew, double>
    SiPixelClusterMultiplicityValueProducer;
DEFINE_FWK_MODULE(SiPixelClusterMultiplicityValueProducer);

typedef MultiplicityValueProducer<reco::Track, double> TrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(TrackMultiplicityValueProducer);

typedef MultiplicityValueProducer<reco::Vertex, double> VertexMultiplicityValueProducer;
DEFINE_FWK_MODULE(VertexMultiplicityValueProducer);
