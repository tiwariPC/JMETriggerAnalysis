import FWCore.ParameterSet.Config as cms
import os

def customize_hltPhase2_L1T(process):

    # L1T recipe for D49 geometry
    GEOMETRY = 'D49'

    if GEOMETRY != 'D49':
       raise RuntimeError('customize_hltPhase2_L1T -- ERROR: invalid value for GEOMETRY: "'+GEOMETRY+'"')

    # Specify L1 tracking algo ('HYBRID', 'HYBRID_DISPLACED', 'TMTT','HYBRID_FLOAT', 'TRACKLET_FLOAT')
    L1TRKALGO = 'HYBRID'
    if L1TRKALGO == 'HYBRID_FLOAT':
       if not os.path.exists(os.environ['CMSSW_BASE']+'/src/L1Trigger/HybridFloat'):
          raise RuntimeError('customize_hltPhase2_L1T -- ERROR: Please checkout HybridFloat code before using "L1TRKALGO == \'HYBRID_FLOAT\'"')

    process.load('Configuration.StandardSequences.SimL1Emulator_cff')

    ############################################################
    # L1 tracking
    ############################################################

    # remake stubs ?
    process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
    # from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import *
    from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import TTStubAlgorithm_cbc3_Phase2TrackerDigi_,TTStubAlgorithm_Phase2TrackerDigi_,TTStubAlgorithm_official_Phase2TrackerDigi_
    process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")

    if GEOMETRY != "TkOnly":
       # from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import *
       from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import TTClusterAssociatorFromPixelDigis
       TTClusterAssociatorFromPixelDigis.digiSimLinks = cms.InputTag("simSiPixelDigis","Tracker")

    process.TTClusterStub = cms.Path(process.TrackTriggerClustersStubs)
    process.TTClusterStubTruth = cms.Path(process.TrackTriggerAssociatorClustersStubs)

    NHELIXPAR = 4
    if   (L1TRKALGO == 'HYBRID'):
        process.load("L1Trigger.TrackFindingTracklet.Tracklet_cfi")
        L1TRK_PROC  =  process.TTTracksFromTrackletEmulation
        L1TRK_NAME  = "TTTracksFromTrackletEmulation"
        L1TRK_LABEL = "Level1TTTracks"
    elif (L1TRKALGO == 'HYBRID_DISPLACED'):
        process.load("L1Trigger.TrackFindingTracklet.Tracklet_cfi")
        L1TRK_PROC  =  process.TTTracksFromExtendedTrackletEmulation
        L1TRK_NAME  = "TTTracksFromExtendedTrackletEmulation"
        L1TRK_LABEL = "Level1TTTracks"
        NHELIXPAR = 5
    elif (L1TRKALGO == 'TMTT'):
        process.load("L1Trigger.TrackFindingTMTT.TMTrackProducer_Ultimate_cff")
        L1TRK_PROC  =  process.TMTrackProducer
        L1TRK_NAME  = "TMTrackProducer"
        L1TRK_LABEL = "TML1TracksKF4ParamsComb"
        L1TRK_PROC.EnableMCtruth = cms.bool(False) # Reduce CPU use by disabling internal histos.
        L1TRK_PROC.EnableHistos  = cms.bool(False)
    elif (L1TRKALGO == 'HYBRID_FLOAT'):
        process.load("L1Trigger.HybridFloat.HybridTrackProducer_cff")
        L1TRK_PROC  =  process.HybridTrackProducer
        L1TRK_NAME  = "HybridTrackProducer"
        L1TRK_LABEL = "HybridL1TracksKF4ParamsComb"
        L1TRK_PROC.EnableMCtruth = cms.bool(False) # Reduce CPU use by disabling internal histos.
        L1TRK_PROC.EnableHistos  = cms.bool(False)
    elif (L1TRKALGO == 'TRACKLET_FLOAT'):
        process.load("L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff")
        L1TRK_PROC  =  process.TTTracksFromTracklet
        L1TRK_NAME  = "TTTracksFromTracklet"
        L1TRK_LABEL = "Level1TTTracks"
    else:
        raise RuntimeError('customize_hltPhase2_L1T -- ERROR: unknown value for L1TRKALGO: "'+L1TRKALGO+'"')

    process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")
    process.TTTrackAssociatorFromPixelDigis.TTTracks = cms.VInputTag( cms.InputTag(L1TRK_NAME, L1TRK_LABEL) )

    ## emulation
    if not hasattr(process, 'offlineBeamSpot'):
       process.load('RecoVertex.BeamSpotProducer.BeamSpot_cfi')

    process.TTTracksEmulation = cms.Path(process.offlineBeamSpot * L1TRK_PROC)
    process.TTTracksEmulationWithTruth = cms.Path(process.offlineBeamSpot * L1TRK_PROC * process.TrackTriggerAssociatorTracks)

    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
    process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

    process.L1simulation_step = cms.Path(process.SimL1Emulator)
    process.schedule.extend([process.TTTracksEmulationWithTruth, process.L1simulation_step])

    return process
