#include <JMETriggerAnalysis/NTuplizer/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizer/interface/RecoPFMETCollectionContainer.h>

#include <vector>

namespace {

  struct dictionary {

    RecoVertexCollectionContainer rvcc1;
    RecoPFCandidateCollectionContainer rpfcc1;
    RecoCaloMETCollectionContainer rcmc1;
    RecoPFMETCollectionContainer rpfmc1;
  };
}
