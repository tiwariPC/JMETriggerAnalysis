import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import os

def customize_hltPhase2_L1(process):

    GEOMETRY = "D49"
    # Specify L1 tracking algo ('HYBRID', 'HYBRID_DISPLACED', 'TMTT','HYBRID_FLOAT', 'TRACKLET_FLOAT')
    L1TRKALGO = 'HYBRID'

    # Write output dataset?
    WRITE_DATA = False

    if (L1TRKALGO == 'HYBRID_FLOAT'):
        if ( not os.path.exists( os.environ['CMSSW_BASE']+'/src/L1Trigger/HybridFloat' ) ):
            print "=== ERROR: Please checkout HybridFloat code from git before using this option ==="; exit

    if GEOMETRY == "D49":
        # print "using geometry " + GEOMETRY + " (tilted)"
        # process = cms.Process('REPR',eras.Phase2C9)
        # process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
        process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
    else:
        print "this is not a valid geometry!!!"

    # process.load('Configuration.StandardSequences.Services_cff')
    # process.load('FWCore.MessageService.MessageLogger_cfi')
    # process.load('Configuration.EventContent.EventContent_cff')
    # process.load('Configuration.StandardSequences.MagneticField_cff')
    # process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    #
    process.load('Configuration.StandardSequences.SimL1Emulator_cff')
    # process.load('Configuration.StandardSequences.EndOfProcess_cff')
    # process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


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
        from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import TTClusterAssociatorFromPixelDigis,premix_stage2
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
        print "ERROR: Unknown L1TRKALGO option"
        exit(1)


    # process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi") #conflict with customisation function of TRKv00
    process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")
    process.TTTrackAssociatorFromPixelDigis.TTTracks = cms.VInputTag( cms.InputTag(L1TRK_NAME, L1TRK_LABEL) )

    ## emulation
    process.TTTracksEmulation = cms.Path(process.offlineBeamSpot*L1TRK_PROC)
    process.TTTracksEmulationWithTruth = cms.Path(process.offlineBeamSpot*L1TRK_PROC*process.TrackTriggerAssociatorTracks)

    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
    process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

    process.L1simulation_step = cms.Path(process.SimL1Emulator)
    process.schedule.extend([process.TTTracksEmulationWithTruth, process.L1simulation_step])


    return process
