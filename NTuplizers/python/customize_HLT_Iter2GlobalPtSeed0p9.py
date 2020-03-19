import FWCore.ParameterSet.Config as cms

def customize_HLT_iter2GlobalPtSeed0p9(process):

    process.hltIter2PFlowPixelTrackingRegionsGlobalPtSeed0p9 = cms.EDProducer( 'GlobalTrackingRegionWithVerticesEDProducer',
      RegionPSet = cms.PSet( 
        useFixedError = cms.bool( True ),
        nSigmaZ = cms.double( 4.0 ),
        VertexCollection = cms.InputTag( 'hltTrimmedPixelVertices' ),
        beamSpot = cms.InputTag( 'hltOnlineBeamSpot' ),
        useFoundVertices = cms.bool( True ),
        fixedError = cms.double( 0.2 ),
        sigmaZVertex = cms.double( 3.0 ),
        useFakeVertices = cms.bool( False ),
        ptMin = cms.double( 0.9 ),
        originRadius = cms.double( 0.05 ),
        precise = cms.bool( True ),
        useMultipleScattering = cms.bool( False )
      )
    )

    process.hltIter2PFlowPixelHitDoublets.trackingRegions = 'hltIter2PFlowPixelTrackingRegionsGlobalPtSeed0p9'

    process.HLTIterativeTrackingIteration2.replace(
      process.hltIter2PFlowPixelTrackingRegions,
      process.hltIter2PFlowPixelTrackingRegionsGlobalPtSeed0p9
    )

    return process
