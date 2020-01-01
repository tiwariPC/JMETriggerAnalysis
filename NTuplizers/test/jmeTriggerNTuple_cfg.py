###
### configuration file to re-run customized HLT Menu on RAW
###
#from JMETriggerAnalysis.NTuplizers.step3_TrackingV0_11_0_0 import cms, process
from JMETriggerAnalysis.NTuplizers.step3_TrackingV2_11_0_0 import cms, process

# remove cms.EndPath for EDM output
del process.HLTOutput

# reset path to EDM input files
process.source.fileNames = []
process.source.secondaryFileNames = []

###
### Sequence for HLT(-like) MET Collections
###
from JMETriggerAnalysis.NTuplizers.hltJMESequence_cff import hltJMESequence
hltJMESequence(process,
  particleFlow = 'particleFlowTmp'+'::'+process.name_(),
  ak4PFJetsForPFMETTypeOne = 'ak4PFJetsCHS'+'::'+process.name_(),
  jescLabelForPFMETTypeOne = 'AK4PFchs',
  primaryVertices = 'goodOfflinePrimaryVertices'+'::'+process.name_(),
  pfNoPileUpJME = 'pfNoPileUpJME'+'::'+process.name_(),
)
process.reconstruction *= process.hltJMESequence

###
### Sequence for HLT(-like) AK4-{PF,Calo} Jets
###
process.ak4PFJetsCorrected.correctors = ['ak4PFL1FastL2L3Corrector']

process.ak4CaloL1FastjetCorrector = cms.EDProducer('L1FastjetCorrectorProducer',
  algorithm = cms.string('AK4Calo'),
  level = cms.string('L1FastJet'),
  srcRho = cms.InputTag('fixedGridRhoFastjetAll'),
)
process.ak4CaloL2RelativeCorrector = cms.EDProducer('LXXXCorrectorProducer',
  algorithm = cms.string('AK4Calo'),
  level = cms.string('L2Relative'),
)
process.ak4CaloL3AbsoluteCorrector = cms.EDProducer('LXXXCorrectorProducer',
  algorithm = cms.string('AK4Calo'),
  level = cms.string('L3Absolute'),
)
process.ak4CaloL1FastL2L3Corrector = cms.EDProducer('ChainedJetCorrectorProducer',
  correctors = cms.VInputTag('ak4CaloL1FastjetCorrector', 'ak4CaloL2RelativeCorrector', 'ak4CaloL3AbsoluteCorrector'),
)
process.ak4CaloJetsCorrected = cms.EDProducer('CorrectedCaloJetProducer',
  correctors = cms.VInputTag('ak4CaloL1FastL2L3Corrector'),
  src = cms.InputTag('ak4CaloJets'),
)
process.ak4CaloJetsSeq = cms.Sequence(
    process.ak4CaloL1FastjetCorrector
  * process.ak4CaloL2RelativeCorrector
  * process.ak4CaloL3AbsoluteCorrector
  * process.ak4CaloL1FastL2L3Corrector
  * process.ak4CaloJetsCorrected
)
process.reconstruction *= process.ak4CaloJetsSeq

###
### add analysis sequence (JMETrigger NTuple)
###
process.analysisCollectionsSequence = cms.Sequence()

## Muons
process.load('JMETriggerAnalysis.NTuplizers.userMuons_cff')
process.analysisCollectionsSequence *= process.userMuonsSequence

## Electrons
process.load('JMETriggerAnalysis.NTuplizers.userElectrons_cff')
process.analysisCollectionsSequence *= process.userElectronsSequence

## Event Selection (none yet)

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'+'::'+process.name_()),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(),

  fillCollectionConditions = cms.PSet(),

  recoVertexCollections = cms.PSet(

    hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'+'::'+process.name_()),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'+'::'+'PAT'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    particleFlowTmp = cms.InputTag('particleFlowTmp'+'::'+process.name_()),
#    hltPuppi = cms.InputTag('hltPuppi'+'::'+process.name_()),
#    hltPuppiForMET = cms.InputTag('hltPuppiForMET'+'::'+process.name_()),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJets = cms.InputTag('ak4GenJets::HLT'),
    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJetsUncorrected = cms.InputTag('ak4CaloJets'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJetsUncorrected = cms.InputTag('ak4PFJets'+'::'+process.name_()),
    hltAK4PFJetsCorrected = cms.InputTag('ak4PFJetsCorrected'+'::'+process.name_()),
    hltAK4PFCHSJetsCorrected = cms.InputTag('ak4PFJetsCHSCorrected'+'::'+process.name_()),
    hltAK4PuppiJetsCorrected = cms.InputTag('hltAK4PuppiJetsCorrected'+'::'+process.name_()),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'+'::'+'PAT'),
    offlineAK4PuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'+'::'+'PAT'),
  ),

  recoGenMETCollections = cms.PSet(

    genMetCalo = cms.InputTag('genMetCalo::HLT'),
    genMetTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

#    hltMet = cms.InputTag('hltMet'+'::'+process.name_()),
#    hltMetClean = cms.InputTag('hltMetClean'+'::'+process.name_()),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMET'+'::'+process.name_()),
    hltPFMETNoPileUpJME = cms.InputTag('hltPFMETNoPileUpJME'+'::'+process.name_()),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'+'::'+process.name_()),

    hltPuppiMET = cms.InputTag('hltPuppiMET'+'::'+process.name_()),
    hltPuppiMETTypeOne = cms.InputTag('hltPuppiMETTypeOne'+'::'+process.name_()),
    hltPuppiMETWithPuppiForJets = cms.InputTag('hltPuppiMETWithPuppiForJets'+'::'+process.name_()),

    hltSoftKillerMET = cms.InputTag('hltSoftKillerMET'+'::'+process.name_()),
  ),

  patMETCollections = cms.PSet(

    offlineMETs = cms.InputTag('slimmedMETs::PAT'),
    offlineMETsPuppi = cms.InputTag('slimmedMETsPuppi::PAT'),
  ),

  patMuonCollections = cms.PSet(

    offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'+'::'+process.name_()),
  ),

  patElectronCollections = cms.PSet(

    offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'+'::'+process.name_()),
  ),

  stringCutObjectSelectors = cms.PSet(

    ak4GenJets = cms.string('pt > 12'),
    ak4GenJetsNoNu = cms.string('pt > 12'),
    hltAK4CaloJetsUncorrected = cms.string('pt > 12'),
    hltAK4PFJetsUncorrected = cms.string('pt > 12'),
    hltAK4PFJetsCorrected = cms.string('pt > 12'),
    hltAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    hltAK4PuppiJetsCorrected = cms.string('pt > 12'),
    offlineAK4CaloJetsCorrected = cms.string('pt > 12'),
    offlineAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    offlineAK4PuppiJetsCorrected = cms.string('pt > 12'),
  ),

  outputBranchesToBeDropped = cms.vstring(

#    'hltPixelVertices_isFake',
#    'hltPixelVertices_chi2',
#    'hltPixelVertices_ndof',

#    'hltTrimmedPixelVertices_isFake',
#    'hltTrimmedPixelVertices_chi2',
#    'hltTrimmedPixelVertices_ndof',

    'offlinePrimaryVertices_tracksSize',

#    'hltPFMet_ChargedEMEtFraction',
#    'hltPFMetTypeOne_ChargedEMEtFraction',

    'genMetCalo_MuonEtFraction',
    'genMetCalo_InvisibleEtFraction',
  ),
)

process.analysisCollectionsPath = cms.Path(process.analysisCollectionsSequence)
#process.analysisCollectionsSchedule = cms.Schedule(process.analysisCollectionsPath)
#process.schedule.extend(process.analysisCollectionsSchedule)

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
#process.schedule.extend([process.analysisNTupleEndPath])

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('threads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads/streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'Path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'Path to python file with content of cms.Process')

opts.register('htrk', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected Tracks and Vertices')

opts.register('skimTracks', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'skim original collection of generalTracks (only tracks associated to first N pixel vertices)')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'Path to output ROOT file')

opts.parseArguments()

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
if opts.threads > 1:
   process.DQMStore.enableMultiThread = True
   process.options.numberOfStreams = opts.threads
   process.options.numberOfThreads = opts.threads
else:
   process.DQMStore.enableMultiThread = False
   process.options.numberOfStreams = 1
   process.options.numberOfThreads = 1

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# Tracking Monitoring
if opts.htrk:
   process.reconstruction_pixelTrackingOnly_step = cms.Path(process.reconstruction_pixelTrackingOnly)

   from JMETriggerAnalysis.Common.TrackHistogrammer_cfi import TrackHistogrammer
   process.TrackHistograms_pixelTracks = TrackHistogrammer.clone(src = cms.InputTag('pixelTracks'))
   process.TrackHistograms_generalTracks = TrackHistogrammer.clone(src = cms.InputTag('generalTracks'))

   from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
   process.VertexHistograms_pixelVertices = VertexHistogrammer.clone(src = cms.InputTag('pixelVertices'))
   process.VertexHistograms_offlinePrimaryVertices = VertexHistogrammer.clone(src = cms.InputTag('offlinePrimaryVertices'))

   process.trkMonitoringSeq = cms.Sequence(
       process.TrackHistograms_pixelTracks
     + process.TrackHistograms_generalTracks
     + process.VertexHistograms_pixelVertices
     + process.VertexHistograms_offlinePrimaryVertices
   )
   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)

# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
       'PixelVerticesSelector',
       'TracksClosestToFirstVerticesSelector',
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
   )

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/PhaseIITDRSpring19MiniAOD/VBF_HToInvisible_M125_14TeV_powheg_pythia8/MINIAODSIM/PU200_106X_upgrade2023_realistic_v3-v1/270000/44F51AA8-922E-2642-83E4-BC53F2D88EF2.root',
   ]

# input EDM files [secondary]
if opts.secondaryInputFiles:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = [
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/1E1B806D-79E0-E64D-BF05-C3A27770E806.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/89AC30B0-09CC-0546-85F1-5A44E9862E23.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/49E12F95-9253-2648-8367-D4A365874C3A.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/B2FF45B9-F262-5B4F-B6C7-DFDD7F32548A.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/C121E739-5001-1740-BAE3-BED6B2B884C0.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/FA8E3C34-2C63-984E-A29C-006612623D1A.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/3A196B8F-0379-7D4C-B708-610966D0EF53.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/81749946-45BB-DF42-94A7-9ECBEE99BF63.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/287B3859-98B3-9B48-ADC0-A977EB28356C.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/91F4C91D-0074-3947-B8C7-599010B26910.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/7C5FCF1B-03E3-074A-AB4B-B3E1AC4E6A10.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/138081EF-72D4-3B4B-995B-E7B8B068BA00.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/C4737E02-79A8-EA48-904B-F4EFFA28475A.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/205038D2-3BE9-6646-A976-8887B2B5B1FE.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/A2301ED8-ADCF-D543-9A80-E29D700AA1B7.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/108EB88F-7978-7443-B62A-26A020677697.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/5CFC5A38-A05D-1048-A5F3-008D7996A9A5.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/8F717475-6ECC-2243-AEFF-3DEF0A278480.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/1C102355-F05E-2E42-9D00-512F27ACC410.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/B5E23869-1DA0-944B-8D85-BC1BCAD564E3.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/81A97D18-471D-C44F-8E43-EC750D709318.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/281740D4-55CE-BF4D-A973-8B4D6C94D668.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/EDA86465-936B-C44A-A927-4E474237807F.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/7F6A6846-BE2A-D74C-A267-26DB9F099F92.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/D78E16FA-9B5F-F84C-9528-2604FC455F89.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/D8A2DF13-8892-9D48-9276-DC058B48573E.root',
     '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v1/270000/1935F21C-E1E1-1345-A8A1-1A44315C1180.root',
   ]

# skimming of tracks
if opts.skimTracks:

   ###
   ### redefine GeneralTracks, selecting a subset of tracks associated to N pixel vertices
   ###  - each track is associated to the pixel vertex which is closest to it in Z
   ###  - the track is retained only if the associated pixel vertex is one of the first N of the vertex collection (ranking is based on sum-pT2)
   ###
   # clone original collection of generalTracks
   process.generalTracksOriginal = process.generalTracks.clone()

   # re-order (see ranker) and restrict the original list of pixel vertices similarly
   # to what was done at HLT in Run-2 (see hltTrimmedPrimaryVertices in 2018 HLT Menu)
   process.hltTrimmedPixelVertices = cms.EDProducer('PixelVerticesSelector',

     src = cms.InputTag('pixelVertices'),

     minSumPt2 = cms.double( 0.0 ),
     minSumPt2FractionWrtMax = cms.double( 0.3 ),

     # criterion to rank pixel vertices
     # (utilizes PVClusterComparer to compute
     # the vertex SumPtSquared f.o.m. using a sub-set of tracks)
     ranker = cms.PSet(
       track_chi2_max = cms.double( 20.0 ),
       track_pt_max = cms.double( 20.0 ),
       track_prob_min = cms.double( -1.0 ),
       track_pt_min = cms.double( 1.0 )
     ),

     # retain only first N vertices
     maxNVertices = cms.int32( -1 ),
   )

   # updated collection of generalTracks
   #  - redefine the module "generalTracks", so that downstream modules
   #    automatically use this updated collection
   #    (instead of the original "generalTracks" collection)
   #  - new set of generalTracks contains only the input tracks
   #    associated to one of the first N pixel vertices
   process.generalTracks = cms.EDProducer('TracksClosestToFirstVerticesSelector',

     tracks = cms.InputTag('generalTracksOriginal'),
     vertices = cms.InputTag('hltTrimmedPixelVertices'),

     # retain only tracks associated to one of the first N vertices
     maxNVertices = cms.int32( 10 ),

     # track-vertex association: max delta-Z between track and z-closest vertex
     maxDeltaZ = cms.double( 0.2 ),
   )

   # insert updated generalTracks into tracking sequence and related task
   process.globalreco_tracking.replace(process.generalTracks, cms.Sequence(
      (process.generalTracksOriginal
     +(process.reconstruction_pixelTrackingOnly * process.hltTrimmedPixelVertices))
     * process.generalTracks
   ))

   process.generalTracksTask.add(process.generalTracksOriginal, process.hltTrimmedPixelVertices)

   # modify PV inputs of Puppi collections
   process.puppiNoLep.vertexName = process.generalTracks.vertices
   process.hltPuppi.vertexName = process.generalTracks.vertices

   # add PV collections to JMETriggerNTuple
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet(
     hltPixelVertices = cms.InputTag('pixelVertices'+'::'+process.name_()),
     hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'+'::'+process.name_()),
     hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'+'::'+process.name_()),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'+'::'+'PAT'),
   )

# print-outs
print '--- jmeTriggerNTuple_cfg.py ---\n'
print 'process.maxEvents.input =', process.maxEvents.input
print 'process.source.skipEvents =', process.source.skipEvents
print 'process.source.fileNames =', process.source.fileNames
print 'process.source.secondaryFileNames =', process.source.secondaryFileNames
print '\n-------------------------------'
