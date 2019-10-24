### configuration file to re-run customized HLT Menu on RAW
from step3_CHSPFJets_11_0_0_pre7 import cms, process

### remove cms.EndPath for EDM output
del process.HLTOutput

process.DQMStore.enableMultiThread = False
process.options.numberOfStreams = 1
process.options.numberOfThreads = 1

### Sequence for HLT(-like) MET Collections
from JMETriggerAnalysis.NTuplizers.hltMETs_cff import hltMETSeq
hltMETSeq(process,
  particleFlow = 'particleFlowTmp'+'::'+process.name_(),
  ak4PFJetsForMETTypeOne = 'ak4PFJets'+'::'+process.name_(),
  primaryVertices = 'goodOfflinePrimaryVertices'+'::'+process.name_(),
  pfNoPileUpJME = None, #'pfNoPileUpJME'+'::'+process.name_(),
)
process.reconstruction *= process.hltMETSeq

### add analysis sequence (JMETrigger NTuple)
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

  TriggerResultsFilterOR = cms.vstring(

#    'HLT_IsoMu24',
#    'HLT_Ele32_WPTight_Gsf',
  ),

  TriggerResultsFilterAND = cms.vstring(

#    'HLT_IsoMu24',
#    'HLT_Ele32_WPTight_Gsf',
  ),

  TriggerResultsCollections = cms.vstring(

#    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
#    'HLT_Ele32_WPTight_Gsf',
#    'HLT_IsoMu24',
#    'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',
#    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
#    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
#    'HLT_PFJet80NoCaloJetCut',
#    'HLT_PFMET200NoCaloMETCut_NotCleaned',
#    'HLT_PFMETTypeOne200NoCaloMETCut_HBHE_BeamHaloCleaned',
  ),

  recoVertexCollections = cms.PSet(

    hltGoodPrimaryVertices = cms.InputTag('goodOfflinePrimaryVertices'+'::'+process.name_()),
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
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFCHSJetsCorrected = cms.InputTag('ak4PFJetsCHSCorrected'+'::'+process.name_()),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'+'::'+'PAT'),
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
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'+'::'+process.name_()),
    hltPuppiMET = cms.InputTag('hltPuppiMET'+'::'+process.name_()),
    hltPuppiMETWithPuppiForJets = cms.InputTag('hltPuppiMETWithPuppiForJets'+'::'+process.name_()),
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

    ak4GenJets = cms.string('pt>7'),
    hltAK4PFCHSJetsCorrected = cms.string('pt>7'),
    offlineAK4PFCHSJetsCorrected = cms.string('pt>7'),
  ),

  outputBranchesToBeDropped = cms.vstring(

#    'hltPixelVertices_isFake',
#    'hltPixelVertices_chi2',
#    'hltPixelVertices_ndof',
#
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

### command-line arguments
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('n', 10,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'max number of events to process')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'Path to output ROOT file')

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

opts.parseArguments()

# max number of events to be processed
process.maxEvents.input = opts.n

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     debugModules = cms.untracked.vstring(
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

process.source.fileNames = [
  '/store/mc/PhaseIITDRSpring19MiniAOD/VBF_HToInvisible_M125_14TeV_powheg_pythia8/MINIAODSIM/PU140_106X_upgrade2023_realistic_v3-v1/270000/3027DB5D-CD81-6A4A-978D-5C64CA8B68A3.root',
]

process.source.secondaryFileNames = [
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/5A26E7F9-B569-1D44-B57A-7BCD262B6A78.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/DB85BD49-E542-914C-8E9D-401D286818C9.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/F6986F4C-3A38-A342-829D-A8FB114DE6C6.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/5A2F16BB-A6FD-CB43-AF8F-EE93600BB6F2.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/7D6CE493-D575-604B-9E55-E71273641587.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/2051711D-7521-DF40-806B-3826D7146AE2.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/8B753C4A-D17F-0445-AF84-2B7BF692A5AE.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/AEC8D441-6162-E04D-92A7-7B29EF63C6A9.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/F9C99741-34AF-1741-A479-209581FC0735.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/5E64EA7A-9B56-0E46-9252-07A2A8DF5CD2.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/724E2624-4007-FF4A-9174-3FE54C2311B7.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/B2B241B8-8B19-A747-B050-2031AEB49751.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/C8DC4237-DD36-334E-A2F7-55EE98C05EEF.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/E84B8FFE-963D-5A48-AB23-13A454827B33.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/216933AF-FBDE-BD45-A24B-72D061EF76A6.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/2B552349-6FF7-BA44-A338-F4C2C260519A.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/2E2ED201-AA6C-5C42-A641-28FC28A172E4.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/690F417C-C5B5-224A-83BD-F92CACF15445.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/9F5F8751-0C0D-AB49-9C66-B742013E74CA.root',
  '/store/mc/PhaseIITDRSpring19DR/VBF_HToInvisible_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/PU140_106X_upgrade2023_realistic_v3-v1/270000/A9937051-2ED4-0E46-87CC-276FB3C7C112.root',
]
