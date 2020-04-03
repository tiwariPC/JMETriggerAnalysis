###
### VarParsing (command-line arguments)
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('reportEvery', 100,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'report Run/Lumi/Event information every N events')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('isData', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'apply customizations for real collisions Data')

opts.register('era', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword for data-taking period')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### Process
###
import FWCore.ParameterSet.Config as cms

process = cms.Process("ANALYSIS")

process.load('Configuration.StandardSequences.Services_cff')
process.load("Configuration.Geometry.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

###
### PoolSource (EDM input)
###
process.source = cms.Source('PoolSource',
  fileNames = cms.untracked.vstring(opts.inputFiles),
  secondaryFileNames = cms.untracked.vstring(opts.secondaryInputFiles),
  # number of events to be skipped
  skipEvents = cms.untracked.uint32(opts.skipEvents)
)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

###
### EDM Options
###
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opts.maxEvents))

process.options = cms.untracked.PSet(
  # show cmsRun summary at job completion
  wantSummary = cms.untracked.bool(opts.wantSummary),
  # multi-threading settings
  numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1),
  numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1),
)

###
### Global Tag
###
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
if opts.globalTag is not None:
   from Configuration.AlCa.GlobalTag import GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
else:
   raise RuntimeError('failed to specify name of the GlobalTag (use "globalTag=XYZ")"')

###
### TFileService
###
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

###
### MessageLogger
###
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
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(opts.reportEvery),
       ),
     ),
   )
else:
   process.load("FWCore.MessageLogger.MessageLogger_cfi")
   process.MessageLogger.cerr.threshold = 'INFO'
   process.MessageLogger.cerr.FwkReport.reportEvery = opts.reportEvery

###
### Analysis Modules
###

## METFilters
from JMETriggerAnalysis.NTuplizers.METFilters_cff import METFilters
process = METFilters(process, era=opts.era)

## Muons
from JMETriggerAnalysis.NTuplizers.userMuons_cff import userMuons
process, userMuonsCollection = userMuons(process)

## Electrons
from JMETriggerAnalysis.NTuplizers.userElectrons_cff import userElectrons
process, userElectronsCollection = userElectrons(process, era=opts.era)

## Electrons
from JMETriggerAnalysis.NTuplizers.userJets_AK04PFCHS_cff import userJets_AK04PFCHS
process, userJetsAK04PFCHSCollection = userJets_AK04PFCHS(process, era=opts.era, isData=opts.isData)

## Event Selection
process.userLeptons = cms.EDProducer('CandViewMerger',
  src = cms.VInputTag(userMuonsCollection, userElectronsCollection)
)

process.userLeptonsMultiplicityFilter = cms.EDFilter('CandViewCountFilter',
  src = cms.InputTag('userLeptons'),
  minNumber = cms.uint32(1),
)

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults::'+('HLT' if opts.isData else 'PAT')),

  TriggerResultsFilterOR = cms.vstring(
  ),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
    'Flag_goodVertices',
    'Flag_globalSuperTightHalo2016Filter',
    'Flag_HBHENoiseFilter',
    'Flag_HBHENoiseIsoFilter',
    'Flag_EcalDeadCellTriggerPrimitiveFilter',
    'Flag_BadPFMuonFilter',
    'Flag_BadChargedCandidateFilter',
    'Flag_eeBadScFilter',
#    'HLT_AK4PFJet100',
#    'HLT_AK4PFJet120',
#    'HLT_AK4PFJet30',
#    'HLT_AK4PFJet50',
#    'HLT_AK4PFJet80',
#    'HLT_AK8PFHT750_TrimMass50',
#    'HLT_AK8PFHT800_TrimMass50',
#    'HLT_AK8PFHT850_TrimMass50',
#    'HLT_AK8PFHT900_TrimMass50',
#    'HLT_AK8PFJet140',
#    'HLT_AK8PFJet15',
#    'HLT_AK8PFJet200',
#    'HLT_AK8PFJet25',
#    'HLT_AK8PFJet260',
#    'HLT_AK8PFJet320',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02',
#    'HLT_AK8PFJet360_TrimMass30',
#    'HLT_AK8PFJet380_TrimMass30',
#    'HLT_AK8PFJet40',
#    'HLT_AK8PFJet400',
#    'HLT_AK8PFJet400_TrimMass30',
#    'HLT_AK8PFJet420_TrimMass30',
#    'HLT_AK8PFJet450',
#    'HLT_AK8PFJet500',
#    'HLT_AK8PFJet550',
#    'HLT_AK8PFJet60',
#    'HLT_AK8PFJet80',
#    'HLT_AK8PFJetFwd140',
#    'HLT_AK8PFJetFwd15',
#    'HLT_AK8PFJetFwd200',
#    'HLT_AK8PFJetFwd25',
#    'HLT_AK8PFJetFwd260',
#    'HLT_AK8PFJetFwd320',
#    'HLT_AK8PFJetFwd40',
#    'HLT_AK8PFJetFwd400',
#    'HLT_AK8PFJetFwd450',
#    'HLT_AK8PFJetFwd500',
#    'HLT_AK8PFJetFwd60',
#    'HLT_AK8PFJetFwd80',
#    'HLT_DiJet110_35_Mjj650_PFMET110',
#    'HLT_DiJet110_35_Mjj650_PFMET120',
#    'HLT_DiJet110_35_Mjj650_PFMET130',
#    'HLT_DiPFJetAve140',
#    'HLT_DiPFJetAve200',
#    'HLT_DiPFJetAve260',
#    'HLT_DiPFJetAve320',
#    'HLT_DiPFJetAve40',
#    'HLT_DiPFJetAve400',
#    'HLT_DiPFJetAve500',
#    'HLT_DiPFJetAve60',
#    'HLT_DiPFJetAve80',
#    'HLT_DoublePFJets100_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets200_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets350_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets40_CaloBTagDeepCSV_p71',
#    'HLT_Ele15_IsoVVVL_PFHT450',
#    'HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5',
#    'HLT_Ele15_IsoVVVL_PFHT450_PFMET50',
#    'HLT_Ele15_IsoVVVL_PFHT600',
#    'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165',
#    'HLT_Ele50_IsoVVVL_PFHT450',
#    'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30',
#    'HLT_Ele8_CaloIdM_TrackIdM_PFJet30',
#    'HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu130_PFMHTNoMu130_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu140_PFMHTNoMu140_IDTight',
#    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350',
#    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ',
#    'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60',
#    'HLT_PFHT1050',
#    'HLT_PFHT180',
#    'HLT_PFHT250',
#    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',
#    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5',
#    'HLT_PFHT350',
#    'HLT_PFHT350MinPFJet15',
#    'HLT_PFHT370',
#    'HLT_PFHT400_FivePFJet_100_100_60_30_30',
#    'HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5',
#    'HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5',
#    'HLT_PFHT400_SixPFJet32',
#    'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
#    'HLT_PFHT430',
#    'HLT_PFHT450_SixPFJet36',
#    'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
#    'HLT_PFHT500_PFMET100_PFMHT100_IDTight',
#    'HLT_PFHT500_PFMET110_PFMHT110_IDTight',
#    'HLT_PFHT510',
#    'HLT_PFHT590',
#    'HLT_PFHT680',
#    'HLT_PFHT700_PFMET85_PFMHT85_IDTight',
#    'HLT_PFHT700_PFMET95_PFMHT95_IDTight',
#    'HLT_PFHT780',
#    'HLT_PFHT800_PFMET75_PFMHT75_IDTight',
#    'HLT_PFHT800_PFMET85_PFMHT85_IDTight',
#    'HLT_PFHT890',
#    'HLT_PFJet140',
#    'HLT_PFJet15',
#    'HLT_PFJet200',
#    'HLT_PFJet25',
#    'HLT_PFJet260',
#    'HLT_PFJet320',
#    'HLT_PFJet40',
#    'HLT_PFJet400',
#    'HLT_PFJet450',
#    'HLT_PFJet500',
#    'HLT_PFJet550',
#    'HLT_PFJet60',
#    'HLT_PFJet80',
#    'HLT_PFJetFwd140',
#    'HLT_PFJetFwd15',
#    'HLT_PFJetFwd200',
#    'HLT_PFJetFwd25',
#    'HLT_PFJetFwd260',
#    'HLT_PFJetFwd320',
#    'HLT_PFJetFwd40',
#    'HLT_PFJetFwd400',
#    'HLT_PFJetFwd450',
#    'HLT_PFJetFwd500',
#    'HLT_PFJetFwd60',
#    'HLT_PFJetFwd80',
#    'HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET100_PFMHT100_IDTight_PFHT60',
#    'HLT_PFMET110_PFMHT110_IDTight',
#    'HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET120_PFMHT120_IDTight',
#    'HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
#    'HLT_PFMET130_PFMHT130_IDTight',
#    'HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET140_PFMHT140_IDTight',
#    'HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET200_BeamHaloCleaned',
#    'HLT_PFMET200_NotCleaned',
#    'HLT_PFMET250_NotCleaned',
#    'HLT_PFMET300_NotCleaned',
#    'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60',
#    'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight',
#    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
#    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60',
#    'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight',
#    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
#    'HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60',
#    'HLT_PFMETTypeOne110_PFMHT110_IDTight',
#    'HLT_PFMETTypeOne120_PFMHT120_IDTight',
#    'HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60',
#    'HLT_PFMETTypeOne130_PFMHT130_IDTight',
#    'HLT_PFMETTypeOne140_PFMHT140_IDTight',
#    'HLT_PFMETTypeOne200_BeamHaloCleaned',
#    'HLT_Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50',
#    'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3',
#    'HLT_Photon90_CaloIdL_PFHT700',
#    'HLT_QuadPFJet103_88_75_15',
#    'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet105_88_76_15',
#    'HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet111_90_80_15',
#    'HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet98_83_71_15',
#    'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET110',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET120',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET130',
#    'MC_AK4PFJets',
#    'MC_AK8PFHT',
#    'MC_AK8PFJets',
#    'MC_AK8TrimPFJets',
#    'MC_PFHT',
#    'MC_PFMET',
  ),

  fillCollectionConditions = cms.PSet(),

  recoVertexCollections = cms.PSet(

#    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
#    hltVerticesPF = cms.InputTag('hltVerticesPF'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    hltParticleFlow = cms.InputTag('hltParticleFlow'),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

#    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
#    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

#    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
#    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

#    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
#    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(
  ),

  recoPFJetCollections = cms.PSet(
#    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
#    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

#    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
#    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
  ),

  patJetCollections = cms.PSet(
    offlineJetsAK04PFCHS = cms.InputTag(userJetsAK04PFCHSCollection),
  ),

  recoGenMETCollections = cms.PSet(
#    genMETCalo = cms.InputTag('genMetCalo::HLT'),
#    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(
#    hltCaloMET = cms.InputTag('hltMet'),
  ),

  recoPFClusterMETCollections = cms.PSet(
  ),

  recoPFMETCollections = cms.PSet(
#    hltPFMET = cms.InputTag('hltPFMETProducer'),
#    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
    offlineMETs = cms.InputTag('slimmedMETs'),
    offlineMETsPuppi = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(
    offlineMuons = cms.InputTag(userMuonsCollection),
  ),

  patElectronCollections = cms.PSet(
    offlineElectrons = cms.InputTag(userElectronsCollection),
  ),

  stringCutObjectSelectors = cms.PSet(
#    ak4GenJetsNoNu = cms.string('pt > 12'),
#    ak8GenJetsNoNu = cms.string('pt > 50'),

#    hltAK4CaloJets = cms.string('pt > 12'),
#    hltAK4CaloJetsCorrected = cms.string('pt > 12'),

#    hltAK8CaloJets = cms.string('pt > 80'),
#    hltAK8CaloJetsCorrected = cms.string('pt > 80'),

#    hltAK4PFJets = cms.string('pt > 12'),
#    hltAK4PFJetsCorrected = cms.string('pt > 12'),

#    hltAK8PFJets = cms.string('pt > 80'),
#    hltAK8PFJetsCorrected = cms.string('pt > 80'),
  ),

  outputBranchesToBeDropped = cms.vstring(

#    'offlinePrimaryVertices_tracksSize',
#
##    'hltPFMet_ChargedEMEtFraction',
##    'hltPFMetTypeOne_ChargedEMEtFraction',
#
#    'genMetCalo_MuonEtFraction',
#    'genMetCalo_InvisibleEtFraction',
  ),
)

process.analysisCollectionsPath = cms.Path(
    process.METFiltersSeq
  + process.userMuonsSeq
  + process.userElectronsSeq
  + process.userLeptons
  + process.userLeptonsMultiplicityFilter
  + process.userJetsAK04PFCHSSeq
  + process.JMETriggerNTuple
)

#process.JMETriggerNTupleEndPath = cms.EndPath(process.analysisCollectionsPath)

### dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

### print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: dumpPython =', opts.dumpPython
print ''
print 'process.GlobalTag =', process.GlobalTag.dumpPython()
print 'process.source =', process.source.dumpPython()
print 'process.maxEvents =', process.maxEvents.dumpPython()
print 'process.options =', process.options.dumpPython()
print 'process.MessageLogger.cerr.FwkReport.reportEvery =', process.MessageLogger.cerr.FwkReport.reportEvery
print '-------------------------------'
