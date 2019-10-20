#include <JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATPackedCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h>

namespace {

  struct dictionary {

    TriggerResultsContainer trc1;
    RecoVertexCollectionContainer rvcc1;
    RecoPFCandidateCollectionContainer rpfcc1;
    PATPackedCandidateCollectionContainer ppcc1;
    RecoCaloMETCollectionContainer rcmc1;
    RecoPFMETCollectionContainer rpfmc1;
  };
}
