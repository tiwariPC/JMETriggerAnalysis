from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from JMETriggerAnalysis.Common.utils import *

#from offline_cfg_dump import *
#sequence = 'particleFlowReco'

from JMETriggerAnalysis.Common.hltPhase2_TRK_dump import *

process.otLocalReco = cms.Sequence(
   process.MeasurementTrackerEvent
)

process.initialStepPVSequence = cms.Sequence(
   process.firstStepPrimaryVerticesUnsorted + #uses beamspot
   process.initialStepTrackRefsForJets +
   process.caloTowerForTrk +
   process.ak4CaloJetsForTrk +
   process.firstStepPrimaryVertices
)

process.initialStepSequence = cms.Sequence(
   process.initialStepSeedLayers +
   process.initialStepTrackingRegions +
   process.initialStepHitDoublets +
   process.initialStepHitQuadruplets +
   process.initialStepSeeds +
   process.initialStepTrackCandidates +
   process.initialStepTracks +
   process.initialStepPVSequence + #uses beamspot
   process.initialStepSelector
)

process.highPtTripletStepSequence = cms.Sequence(
   process.highPtTripletStepClusters +
   process.highPtTripletStepSeedLayers +
   process.highPtTripletStepTrackingRegions +
   process.highPtTripletStepHitDoublets +
   process.highPtTripletStepHitTriplets +
   process.highPtTripletStepSeedLayers +
   process.highPtTripletStepSeeds +
   process.highPtTripletStepTrackCandidates +
   process.highPtTripletStepTracks +
   process.highPtTripletStepSelector +
   process.initialStepSeedClusterMask + # needed by electron, but also by highPtTripletStepSeedClusterMask
   process.highPtTripletStepSeedClusterMask
)

process.vertexReco = cms.Sequence(
   process.caloTowerForTrk +
   process.ak4CaloJetsForTrk +
   process.firstStepPrimaryVertices
)

process.itLocalReco = cms.Sequence(
   process.siPhase2Clusters +
   process.siPixelClusters +
   process.siPixelClusterShapeCache +
   process.siPixelClustersPreSplitting +
   process.siPixelRecHits +
   process.siPixelRecHitsPreSplitting
)

process.initialStepSequence = cms.Sequence(
   process.initialStepSeedLayers +
   process.initialStepTrackingRegions +
   process.initialStepHitDoublets +
   process.initialStepHitQuadruplets +
   process.initialStepSeeds +
   process.initialStepTrackCandidates +
   process.initialStepTracks +
   process.initialStepPVSequence + #uses beamspot
   process.initialStepSelector
)

process.highPtTripletStepSequence = cms.Sequence(
   process.highPtTripletStepClusters +
   process.highPtTripletStepSeedLayers +
   process.highPtTripletStepTrackingRegions +
   process.highPtTripletStepHitDoublets +
   process.highPtTripletStepHitTriplets +
   process.highPtTripletStepSeedLayers +
   process.highPtTripletStepSeeds +
   process.highPtTripletStepTrackCandidates +
   process.highPtTripletStepTracks +
   process.highPtTripletStepSelector +
   process.initialStepSeedClusterMask + 
   process.highPtTripletStepSeedClusterMask
)

process.vertexReco = cms.Sequence(
   process.ak4CaloJetsForTrk +
   process.unsortedOfflinePrimaryVertices +
   process.trackWithVertexRefSelectorBeforeSorting +
   process.trackRefsForJetsBeforeSorting +
   process.offlinePrimaryVertices +
   process.offlinePrimaryVerticesWithBS +
   process.inclusiveVertexFinder +
   process.vertexMerger +
   process.trackVertexArbitrator +
   process.inclusiveSecondaryVertices
)

process.MC_Tracking_v2_seq = cms.Sequence(
   process.itLocalReco +
   process.offlineBeamSpot + #cmssw_10_6
   process.otLocalReco +
   process.trackerClusterCheck +
   process.initialStepSequence +
   process.highPtTripletStepSequence +
   process.generalTracks +
   process.vertexReco 
)

sequence = 'MC_Tracking_v2_seq'

orderedListOfModuleNames = orderedListOfModuleNamesFromSequence(process, sequence)

#print('process.'+sequence+' = cms.Sequence(')
#for _idx in range(len(orderedListOfModuleNames)):
#    print('  '+(' ' if (_idx == 0) else '+')+' '+orderedListOfModuleNames[_idx])
#print(')')

print('import FWCore.ParameterSet.Config as cms\n')
for _idx in range(len(orderedListOfModuleNames)):
    print(orderedListOfModuleNames[_idx], '=', getattr(process, orderedListOfModuleNames[_idx]).dumpPython())
