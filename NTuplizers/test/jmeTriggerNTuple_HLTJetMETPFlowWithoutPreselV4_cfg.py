### configuration file to re-run customized HLT Menu on RAW
from HLT_JetMETPFlowWithoutPreselV4_cfg import cms, process

### remove RECO step (EDM output file will not be produced)
process.schedule.remove(process.RECOSIMoutput_step)

### add analysis sequence (JMETrigger NTuple)
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'+'::'+process.name_()),

  HLTPathsWithoutVersion = cms.vstring(

    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    'HLT_Ele32_WPTight_Gsf',
    'HLT_IsoMu24',
    'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',
    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    'HLT_PFJet80NoCaloJetCut',
    'HLT_PFMET200NoCaloMETCut_NotCleaned',
    'HLT_PFMETTypeOne200NoCaloMETCut_HBHE_BeamHaloCleaned',
  ),

  HLTPathsFilterOR = cms.vstring(

    'HLT_IsoMu24',
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'+'::'+process.name_()),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'+'::'+process.name_()),
    offlineSlimmedPrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(

    hltParticleFlow = cms.InputTag('hltParticleFlow'+'::'+process.name_()),
  ),

  patPackedCandidateCollections = cms.PSet(

    packedPFCandidates = cms.InputTag('packedPFCandidates'),
  ),

#  recoPFJetCollections = cms.PSet(
#
#    hltAK4PFJets = cms.InputTag('hltAK4PFJets'+'::'+process.name_()),
#  ),

  recoCaloMETCollections = cms.PSet(

    hltMet = cms.InputTag('hltMet'+'::'+process.name_()),
    hltMetClean = cms.InputTag('hltMetClean'+'::'+process.name_()),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMet = cms.InputTag('hltPFMETProducer'+'::'+process.name_()),
    hltPFMetTypeOne = cms.InputTag('hltPFMETTypeOne'+'::'+process.name_()),
  ),

  patMETCollections = cms.PSet(

    slimmedMETs = cms.InputTag('slimmedMETs'),
    slimmedMETsPuppi = cms.InputTag('slimmedMETsPuppi'),
  ),

  outputBranchesToBeDropped = cms.vstring(

    'hltPixelVertices_isFake',
    'hltPixelVertices_chi2',
    'hltPixelVertices_ndof',

    'hltTrimmedPixelVertices_isFake',
    'hltTrimmedPixelVertices_chi2',
    'hltTrimmedPixelVertices_ndof',

    'offlineSlimmedPrimaryVertices_tracksSize',

    'hltPFMet_ChargedEMEtFraction',
    'hltPFMetTypeOne_ChargedEMEtFraction',
  ),
)

process.analysisSequence = cms.Sequence(
  process.JMETriggerNTuple
)

process.analysis_step = cms.EndPath(process.analysisSequence)

process.schedule.extend([process.analysis_step])

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
