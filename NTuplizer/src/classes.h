#include <JMETriggerAnalysis/NTuplizer/interface/TriggerResultsContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/PATPackedCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFMETCollectionContainer.h>

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
