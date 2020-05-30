###
### command-line arguments
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

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', '110X_mcRun3_2021_realistic_Candidate_2020_05_26_16_08_15',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('trkdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected Tracks and Vertices')

opts.register('pfdqm', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'added monitoring histograms for selected PF-Candidates')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### HLT configuration
###
from JMETriggerAnalysis.NTuplizers.customisedHLTProcess import *
cms, process = customisedHLTProcess(opts.reco)

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       print '> removed cms.OutputModule:', _modname

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       print '> removed cms.EndPath:', _modname
       
# remove selected cms.Path objects from HLT config-dump
for _modname in process.paths_():
    if _modname.startswith('MC_') and (('Jets' in _modname) or ('MET' in _modname)):
       continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
       process.__delattr__(_modname)
       print '> removed cms.Path:', _modname

# delete process.MessaggeLogger from HLT config
if hasattr(process, 'MessageLogger'):
   del process.MessageLogger

###
### add analysis sequence (JMETrigger NTuple)
###
process.analysisCollectionsSequence = cms.Sequence()

## Muons
from JMETriggerAnalysis.NTuplizers.userMuons_cff import userMuons
process, userMuonsCollection = userMuons(process)
process.analysisCollectionsSequence += process.userMuonsSequence

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
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
#    'MC_PFMETNoMu',
#    'MC_PuppiMET',
#    'MC_PuppiMETNoMu',
  ),

  fillCollectionConditions = cms.PSet(),

  bools = cms.PSet(),

  ints = cms.PSet(),

  floats = cms.PSet(),

  doubles = cms.PSet(
#    hltPuppiV1_PuppiNAlgos = cms.InputTag('hltPuppiV1:PuppiNAlgos'),
#    hltPuppiV3_PuppiNAlgos = cms.InputTag('hltPuppiV3:PuppiNAlgos'),
  ),

  vbools = cms.PSet(),

  vints = cms.PSet(),

  vfloats = cms.PSet(),

  vdoubles = cms.PSet(
#    hltPuppiV1_PuppiAlphas = cms.InputTag('hltPuppiV1:PuppiAlphas'),
#    hltPuppiV1_PuppiAlphasMed = cms.InputTag('hltPuppiV1:PuppiAlphasMed'),
#    hltPuppiV1_PuppiAlphasRms = cms.InputTag('hltPuppiV1:PuppiAlphasRms'),
#    hltPuppiV1_PuppiRawAlphas = cms.InputTag('hltPuppiV1:PuppiRawAlphas'),

#    hltPuppiV3_PuppiAlphas = cms.InputTag('hltPuppiV3:PuppiAlphas'),
#    hltPuppiV3_PuppiAlphasMed = cms.InputTag('hltPuppiV3:PuppiAlphasMed'),
#    hltPuppiV3_PuppiAlphasRms = cms.InputTag('hltPuppiV3:PuppiAlphasRms'),
#    hltPuppiV3_PuppiRawAlphas = cms.InputTag('hltPuppiV3:PuppiRawAlphas'),
  ),

  recoVertexCollections = cms.PSet(
    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
#    hltParticleFlow = cms.InputTag('hltParticleFlow'),
#    hltParticleFlowCHSv1 = cms.InputTag('hltParticleFlowCHSv1'),
#    hltParticleFlowCHSv2 = cms.InputTag('hltParticleFlowCHSv2'),

#    hltPuppiV1 = cms.InputTag('hltPuppiV1'),
#    hltPuppiV3 = cms.InputTag('hltPuppiV3'),
  ),

  patPackedCandidateCollections = cms.PSet(
#    offlineParticleFlow = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(
    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(
    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(
    hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(
    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    hltAK4PFCHSv1Jets = cms.InputTag('hltAK4PFCHSv1Jets'),
    hltAK4PFCHSv1JetsCorrected = cms.InputTag('hltAK4PFCHSv1JetsCorrected'),
    hltAK4PFCHSv2Jets = cms.InputTag('hltAK4PFCHSv2Jets'),
    hltAK4PFCHSv2JetsCorrected = cms.InputTag('hltAK4PFCHSv2JetsCorrected'),
    hltAK4PuppiV1Jets = cms.InputTag('hltAK4PuppiV1Jets'),
    hltAK4PuppiV1JetsCorrected = cms.InputTag('hltAK4PuppiV1JetsCorrected'),
    hltAK4PuppiV3Jets = cms.InputTag('hltAK4PuppiV3Jets'),
    hltAK4PuppiV3JetsCorrected = cms.InputTag('hltAK4PuppiV3JetsCorrected'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
    hltAK8PFCHSv1Jets = cms.InputTag('hltAK8PFCHSv1Jets'),
    hltAK8PFCHSv1JetsCorrected = cms.InputTag('hltAK8PFCHSv1JetsCorrected'),
    hltAK8PFCHSv2Jets = cms.InputTag('hltAK8PFCHSv2Jets'),
    hltAK8PFCHSv2JetsCorrected = cms.InputTag('hltAK8PFCHSv2JetsCorrected'),
    hltAK8PuppiV1Jets = cms.InputTag('hltAK8PuppiV1Jets'),
    hltAK8PuppiV1JetsCorrected = cms.InputTag('hltAK8PuppiV1JetsCorrected'),
    hltAK8PuppiV3Jets = cms.InputTag('hltAK8PuppiV3Jets'),
    hltAK8PuppiV3JetsCorrected = cms.InputTag('hltAK8PuppiV3JetsCorrected'),
  ),

  patJetCollections = cms.PSet(
    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    offlineAK8PuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(
    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(
    hltCaloMET = cms.InputTag('hltMet'),
  ),

  recoPFClusterMETCollections = cms.PSet(
  ),

  recoPFMETCollections = cms.PSet(
    hltPFMET = cms.InputTag('hltPFMETProducer'),
    hltPFMETNoMu = cms.InputTag('hltPFMETNoMuProducer'),

    hltPFCHSv2MET = cms.InputTag('hltPFCHSv2MET'),
    hltPFCHSv1MET = cms.InputTag('hltPFCHSv1MET'),

    hltPuppiV1MET     = cms.InputTag('hltPuppiV1MET'),
    hltPuppiV1METNoMu = cms.InputTag('hltPuppiV1METNoMu'),
    hltPuppiV2MET     = cms.InputTag('hltPuppiV2MET'),
    hltPuppiV2METNoMu = cms.InputTag('hltPuppiV2METNoMu'),

    hltPuppiV3MET     = cms.InputTag('hltPuppiV3MET'),
    hltPuppiV3METNoMu = cms.InputTag('hltPuppiV3METNoMu'),
    hltPuppiV4MET     = cms.InputTag('hltPuppiV4MET'),
    hltPuppiV4METNoMu = cms.InputTag('hltPuppiV4METNoMu'),

    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(
    offlineMuons = cms.InputTag(userMuonsCollection)
  ),

  patElectronCollections = cms.PSet(
  ),

  stringCutObjectSelectors = cms.PSet(
    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    hltAK4CaloJets             = cms.string('pt > 20'),
    hltAK4CaloJetsCorrected    = cms.string('pt > 20'),
    hltAK4PFClusterJets        = cms.string('pt > 20'),
    hltAK4PFJets               = cms.string('pt > 20'),
    hltAK4PFJetsCorrected      = cms.string('pt > 20'),
    hltAK4PFCHSv1Jets          = cms.string('pt > 20'),
    hltAK4PFCHSv1JetsCorrected = cms.string('pt > 20'),
    hltAK4PFCHSv2Jets          = cms.string('pt > 20'),
    hltAK4PFCHSv2JetsCorrected = cms.string('pt > 20'),
    hltAK4PuppiV1Jets          = cms.string('pt > 20'),
    hltAK4PuppiV1JetsCorrected = cms.string('pt > 20'),
    hltAK4PuppiV3Jets          = cms.string('pt > 20'),
    hltAK4PuppiV3JetsCorrected = cms.string('pt > 20'),

    hltAK8CaloJets             = cms.string('pt > 80'),
    hltAK8CaloJetsCorrected    = cms.string('pt > 80'),
    hltAK8PFClusterJets        = cms.string('pt > 80'),
    hltAK8PFJets               = cms.string('pt > 80'),
    hltAK8PFJetsCorrected      = cms.string('pt > 80'),
    hltAK8PFCHSv1Jets          = cms.string('pt > 80'),
    hltAK8PFCHSv1JetsCorrected = cms.string('pt > 80'),
    hltAK8PFCHSv2Jets          = cms.string('pt > 80'),
    hltAK8PFCHSv2JetsCorrected = cms.string('pt > 80'),
    hltAK8PuppiV1Jets          = cms.string('pt > 80'),
    hltAK8PuppiV1JetsCorrected = cms.string('pt > 80'),
    hltAK8PuppiV3Jets          = cms.string('pt > 80'),
    hltAK8PuppiV3JetsCorrected = cms.string('pt > 80'),

    offlineAK4PFCHSJetsCorrected = cms.string('pt > 20'),
    offlineAK4PuppiJetsCorrected = cms.string('pt > 20'),
    offlineAK8PuppiJetsCorrected = cms.string('pt > 80'),
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

process.analysisCollectionsPath = cms.Path(process.analysisCollectionsSequence)
#process.HLTSchedule.extend([process.analysisCollectionsPath])

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
#process.HLTSchedule.extend([process.analysisNTupleEndPath])

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)
#if hasattr(process, 'DQMStore'):
#   process.DQMStore.enableMultiThread = (process.options.numberOfThreads > 1)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# Tracking Monitoring
if opts.trkdqm:
   process.trkMonitoringSeq = cms.Sequence()

   # tracks
   from JMETriggerAnalysis.Common.TrackHistogrammer_cfi import TrackHistogrammer
   for _trkColl in [
     'hltPixelTracks',
     'hltPixelTracksClean',
     'hltMergedTracks',
     'hltIter0PFlowTrackSelectionHighPurity',
   ]:
     setattr(process, 'TrackHistograms_'+_trkColl, TrackHistogrammer.clone(src = _trkColl))
     process.trkMonitoringSeq += getattr(process, 'TrackHistograms_'+_trkColl)

   # vertices
   from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
   for _vtxColl in [
     'hltPixelVertices',
     'hltTrimmedPixelVertices',
     'hltVerticesPF',
     'offlineSlimmedPrimaryVertices',
   ]:
     setattr(process, 'VertexHistograms_'+_vtxColl, VertexHistogrammer.clone(src = _vtxColl))
     process.trkMonitoringSeq += getattr(process, 'VertexHistograms_'+_vtxColl)

#   from Validation.RecoVertex.PrimaryVertexAnalyzer4PUSlimmed_cfi import vertexAnalysis, pixelVertexAnalysisPixelTrackingOnly
#   process.vertexAnalysis = vertexAnalysis.clone(vertexRecoCollections = ['offlinePrimaryVertices'])
#   process.pixelVertexAnalysis = pixelVertexAnalysisPixelTrackingOnly.clone(vertexRecoCollections = ['pixelVertices'])
#
#   process.trkMonitoringSeq += cms.Sequence(
#       process.vertexAnalysis
#     + process.pixelVertexAnalysis
#   )

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
#   process.HLTSchedule.extend([process.trkMonitoringEndPath])

# ParticleFlow Monitoring
if opts.pfdqm > 0:
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate

   _candTags = [
     ('_offlineParticleFlow', 'packedPFCandidates', '', pfCandidateHistogrammerPatPackedCandidate),
     ('_hltParticleFlow', 'hltParticleFlow', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltParticleFlowCHSv1', 'hltParticleFlowCHSv1', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltParticleFlowCHSv2', 'hltParticleFlowCHSv2', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPuppiV1', 'hltPuppiV1', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
#    ('_hltPuppiV2', 'hltPuppiV2', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPuppiV3', 'hltPuppiV3', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
#    ('_hltPuppiV4', 'hltPuppiV4', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
   ]

   if opts.pfdqm > 1:
      _tmpCandTags = []
      for _tmp in _candTags:
          _tmpCandTags += [(_tmp[0]+'_2GeV', _tmp[1], '(pt > 2.)', _tmp[3])]
      _candTags += _tmpCandTags
      del _tmpCandTags

   _regTags = [
     ['', ''],
     ['_HB', '(0.0<=abs(eta) && abs(eta)<1.3)'],
     ['_HE', '(1.3<=abs(eta) && abs(eta)<3.0)'],
     ['_HF', '(3.0<=abs(eta) && abs(eta)<5.0)'],
   ]

   _pidTags = [
     ['', ''],
     ['_h', '(abs(pdgId) == 211)'],
     ['_e', '(abs(pdgId) == 11)'],
     ['_mu', '(abs(pdgId) == 13)'],
     ['_gamma', '(abs(pdgId) == 22)'],
     ['_h0', '(abs(pdgId) == 130)'],
   ]

   process.pfMonitoringSeq = cms.Sequence()
   for _candTag in _candTags:
     for _regTag in _regTags:
       for _pidTag in _pidTags:
         _modName = 'PFCandidateHistograms'+_candTag[0]+_regTag[0]+_pidTag[0]
         setattr(process, _modName, _candTag[3].clone(
           src = _candTag[1],
           cut = ' && '.join([_tmp for _tmp in [_candTag[2], _regTag[1], _pidTag[1]] if _tmp]),
         ))
         process.pfMonitoringSeq += getattr(process, _modName)

   process.pfMonitoringEndPath = cms.EndPath(process.pfMonitoringSeq)
#   process.HLTSchedule.extend([process.pfMonitoringEndPath])

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

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/MINIAODSIM/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/06046A61-F68D-364A-B48B-9B8B71D99980.root',
   ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
   process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles == ['None']:
   process.source.secondaryFileNames = []
elif opts.secondaryInputFiles != []:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = [
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/1E007C6B-0236-774C-AE76-16FF40129ED8.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/28B01ED8-0D18-7546-BA43-0237889F3BA7.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/2A97FB7E-1CAF-C14F-B35D-73109005BFD0.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/2CBC0309-9AA0-A047-8AA0-E099EA6B4745.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/460E3EEF-6F6E-D94A-AD05-7F20945D96C6.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/6CC199A5-0BBA-CD4D-AC64-86BA65281EBB.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/75CD4F71-FC10-4F40-9A59-540A2367FDF8.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/79961B00-117B-994F-8425-E9DC19AF6823.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/9275A076-96E6-2347-A859-ED4F3835FDFB.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/AEF78A17-5BF6-714C-BA73-8916E7684185.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/C1A22F6E-FE7C-4A45-9D0D-B6A568011166.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/CC44A2B7-BB6B-914F-9AC2-571448730AFF.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/D3198660-A789-5C43-A589-0994A675CD75.root',
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/E7C3A195-4EBA-5B41-B611-8431BE3DB069.root',
   ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: reco =', opts.reco
print 'option: trkdqm =', opts.trkdqm
print 'option: pfdqm =', opts.pfdqm
print 'option: dumpPython =', opts.dumpPython
print ''
print 'process.GlobalTag =', process.GlobalTag.dumpPython()
print 'process.source =', process.source.dumpPython()
print 'process.maxEvents =', process.maxEvents.dumpPython()
print 'process.options =', process.options.dumpPython()
print '-------------------------------'
