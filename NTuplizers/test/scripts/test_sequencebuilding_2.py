from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from JMETriggerAnalysis.Common.utils import *

#from offline_cfg_dump import *
#sequence = 'particleFlowReco'

from trkPOG_dump import *

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

#for _modname in process.switchProducerNames():
#    print(_modname)
#processHasModule(process, 'a')
#for _tmp in []:
#    print(_tmp, processHasModule(process, _tmp))

orderedListOfModuleNames = orderedListOfModuleNamesFromSequence(process, sequence)

newList = orderedListOfModuleNames[:]
for _tmp in orderedListOfModuleNames:
    newList += getModuleDependencies(getattr(process, _tmp))
newList = sorted(list(set(newList)))

#print('process.'+sequence+' = cms.Sequence(')
#for _idx in range(len(orderedListOfModuleNames)):
#    print('  '+(' ' if (_idx == 0) else '+')+' '+orderedListOfModuleNames[_idx])
#print(')')



#for _tmp in newList:
#    if hasattr(process, _tmp): print(_tmp)

print('import FWCore.ParameterSet.Config as cms\n')
#for _idx in range(len(newList)):
#    if newList[_idx] in orderedListOfModuleNames: continue
#    if not hasattr(process, newList[_idx]): continue
#    print(newList[_idx], '=', getattr(process, newList[_idx]).dumpPython())
for _tmp in process.es_prefers_():
    if _tmp in orderedListOfModuleNames: continue
    print(_tmp, '=', getattr(process, _tmp).dumpPython())
for _tmp in process.es_sources_():
    if _tmp in orderedListOfModuleNames: continue
    print(_tmp, '=', getattr(process, _tmp).dumpPython())
for _tmp in process.es_producers_():
    if _tmp in orderedListOfModuleNames: continue
    print(_tmp, '=', getattr(process, _tmp).dumpPython())
for _idx in range(len(orderedListOfModuleNames)):
    print(orderedListOfModuleNames[_idx], '=', getattr(process, orderedListOfModuleNames[_idx]).dumpPython())
