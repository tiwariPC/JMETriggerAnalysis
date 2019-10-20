#include <JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATPackedCandidateCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoCaloMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATMuonCollectionContainer.h>
#include <JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h>

namespace {

  struct dictionary {

    TriggerResultsContainer TriggerResultsContainer1;
    RecoVertexCollectionContainer RecoVertexCollectionContainer1;
    RecoPFCandidateCollectionContainer RecoPFCandidateCollectionContainer1;
    PATPackedCandidateCollectionContainer PATPackedCandidateCollectionContainer1;
    RecoCaloMETCollectionContainer RecoCaloMETCollectionContainer1;
    RecoPFMETCollectionContainer RecoPFMETCollectionContainer1;
    PATMETCollectionContainer PATMETCollectionContainer1;
    PATMuonCollectionContainer PATMuonCollectionContainer1;
    PATElectronCollectionContainer PATElectronCollectionContainer1;
  };
}
