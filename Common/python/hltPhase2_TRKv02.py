import FWCore.ParameterSet.Config as cms
import importlib

def customize_hltPhase2_TRKv02(process, cff='JMETriggerAnalysis.Common.hltPhase2_TRKv02_modules1110pre3_cff'):

    ### redefine process.globalreco_tracking
    process.otLocalReco = cms.Sequence(
        process.MeasurementTrackerEvent
    )

    process.initialStepPVSequence = cms.Sequence(
        process.firstStepPrimaryVerticesUnsorted #uses beamspot
      + process.initialStepTrackRefsForJets
      + process.hcalGlobalRecoSequence
      + process.caloTowerForTrk
      + process.ak4CaloJetsForTrk
      + process.firstStepPrimaryVertices
    )

    process.initialStepSequence = cms.Sequence(
        process.initialStepSeedLayers
      + process.initialStepTrackingRegions
      + process.initialStepHitDoublets
      + process.initialStepHitQuadruplets
      + process.initialStepSeeds
      + process.initialStepTrackCandidates
      + process.initialStepTracks
      + process.initialStepPVSequence #uses beamspot
      + process.initialStepSelector
    )

    process.highPtTripletStepSequence = cms.Sequence(
        process.highPtTripletStepClusters
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepTrackingRegions
      + process.highPtTripletStepHitDoublets
      + process.highPtTripletStepHitTriplets
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepSeeds
      + process.highPtTripletStepTrackCandidates
      + process.highPtTripletStepTracks
      + process.highPtTripletStepSelector
      + process.initialStepSeedClusterMask # needed by electron, but also by highPtTripletStepSeedClusterMask
      + process.highPtTripletStepSeedClusterMask
    )

    process.itLocalReco = cms.Sequence(
        process.siPhase2Clusters
      + process.siPixelClusters
      + process.siPixelClusterShapeCache
      + process.siPixelClustersPreSplitting
      + process.siPixelRecHits
      + process.siPixelRecHitsPreSplitting
    )

    process.initialStepSequence = cms.Sequence(
        process.initialStepSeedLayers
      + process.initialStepTrackingRegions
      + process.initialStepHitDoublets
      + process.initialStepHitQuadruplets
      + process.initialStepSeeds
      + process.initialStepTrackCandidates
      + process.initialStepTracks
      + process.initialStepPVSequence #uses beamspot
      + process.initialStepSelector
    )

    process.highPtTripletStepSequence = cms.Sequence(
        process.highPtTripletStepClusters
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepTrackingRegions
      + process.highPtTripletStepHitDoublets
      + process.highPtTripletStepHitTriplets
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepSeeds
      + process.highPtTripletStepTrackCandidates
      + process.highPtTripletStepTracks
      + process.highPtTripletStepSelector
      + process.initialStepSeedClusterMask 
      + process.highPtTripletStepSeedClusterMask
    )

    process.vertexReco = cms.Sequence(
        process.ak4CaloJetsForTrk
      + process.unsortedOfflinePrimaryVertices
      + process.trackWithVertexRefSelectorBeforeSorting
      + process.trackRefsForJetsBeforeSorting
      + process.offlinePrimaryVertices
      + process.offlinePrimaryVerticesWithBS
      + process.inclusiveVertexFinder
      + process.vertexMerger
      + process.trackVertexArbitrator
      + process.inclusiveSecondaryVertices
    )

    process.globalreco_tracking = cms.Sequence(
        process.itLocalReco
      + process.offlineBeamSpot #cmssw_10_6
      + process.otLocalReco
      + process.trackerClusterCheck
      + process.initialStepSequence
      + process.highPtTripletStepSequence
      + process.generalTracks
      + process.vertexReco 
    )

    # delete all modules in process.globalreco_tracking
    _globalreco_tracking_moduleNames = getattr(process, 'globalreco_tracking').moduleNames()

    # configuration file with plain list of modules modified by TRK POG
    _procTmp = importlib.import_module(cff)
    for _modName in _globalreco_tracking_moduleNames:
        if hasattr(process, _modName) and hasattr(_procTmp, _modName):
           setattr(process, _modName, getattr(_procTmp, _modName).clone())
#    for _modName in process.es_prefers_():
#        if hasattr(_procTmp, _modName) and (getattr(_procTmp, _modName) != getattr(process, _modName)):
#           setattr(process, _modName, getattr(_procTmp, _modName).clone())
#    for _modName in process.es_sources_():
#        if hasattr(_procTmp, _modName) and (getattr(_procTmp, _modName) != getattr(process, _modName)):
#           setattr(process, _modName, getattr(_procTmp, _modName).clone())
#    for _modName in process.es_producers_():
#        if hasattr(_procTmp, _modName) and (getattr(_procTmp, _modName) != getattr(process, _modName)):
#           setattr(process, _modName, getattr(_procTmp, _modName).clone())
    del _procTmp

    process.trackAlgoPriorityOrder.algoOrder = [
      'initialStep',
      'highPtTripletStep',
    ]

    ## PixelCPE issue
    process.TrackProducer.TTRHBuilder = 'WithTrackAngle'
    process.PixelCPEGenericESProducer.UseErrorsFromTemplates = False
    process.PixelCPEGenericESProducer.LoadTemplatesFromDB = False
    process.PixelCPEGenericESProducer.TruncatePixelCharge = False
    process.PixelCPEGenericESProducer.IrradiationBiasCorrection = False
    process.PixelCPEGenericESProducer.DoCosmics = False
    process.PixelCPEGenericESProducer.Upgrade = True

    return process
