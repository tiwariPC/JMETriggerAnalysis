###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('reco', 'HLT_TRKv06_TICL',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

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

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
### (choice of reconstruction sequence)
###

# flag: skim original collection of generalTracks (only tracks associated to first N pixel vertices)
opt_skimTracks = False

opt_reco = opts.reco
if opt_reco.endswith('_skimmedTracks'):
   opt_reco = opt_reco[:-len('_skimmedTracks')]
   opt_skimTracks = True

if   opt_reco == 'HLT_TRKv00':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_cfg      import cms, process
elif opt_reco == 'HLT_TRKv00_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_TICL_cfg import cms, process
elif opt_reco == 'HLT_TRKv02':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_cfg      import cms, process
elif opt_reco == 'HLT_TRKv02_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_TICL_cfg import cms, process
elif opt_reco == 'HLT_TRKv06':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_cfg      import cms, process
elif opt_reco == 'HLT_TRKv06_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_TICL_cfg import cms, process
else:
   logmsg = '\n\n'+' '*2+'Valid arguments for option "reco" are'
   for recoArg in [
     'HLT_TRKv00',
     'HLT_TRKv00_skimmedTracks',
     'HLT_TRKv00_TICL',
     'HLT_TRKv00_TICL_skimmedTracks',
     'HLT_TRKv02',
     'HLT_TRKv02_skimmedTracks',
     'HLT_TRKv02_TICL',
     'HLT_TRKv02_TICL_skimmedTracks',
     'HLT_TRKv06',
     'HLT_TRKv06_skimmedTracks',
     'HLT_TRKv06_TICL',
     'HLT_TRKv06_TICL_skimmedTracks',
   ]:
     logmsg += '\n'+' '*4+recoArg
   raise RuntimeError('invalid argument for option "reco": "'+opt_reco+'"'+logmsg+'\n')

# skimming of tracks
if opt_skimTracks:
   from JMETriggerAnalysis.Common.hltPhase2_skimmedTracks import customize_hltPhase2_skimmedTracks
   process = customize_hltPhase2_skimmedTracks(process)

###
### trigger paths
###

## sequence: ParticleFlow
process.HLTParticleFlowSequence = cms.Sequence(
    process.localreco
  + process.globalreco
  + process.particleFlowReco
)

## sequence: AK4 Jets, PFCHS
process.HLTAK4PFCHSJetsReconstruction = cms.Sequence(
    process.particleFlowPtrs
  + process.goodOfflinePrimaryVertices
  + process.pfPileUpJME
  + process.pfNoPileUpJME
  + process.hltAK4PFCHSJets
  + process.hltAK4PFCHSJetCorrectorL1
  + process.hltAK4PFCHSJetCorrectorL2
  + process.hltAK4PFCHSJetCorrectorL3
  + process.hltAK4PFCHSJetCorrectorL2L3
  + process.hltAK4PFCHSJetCorrector
  + process.hltAK4PFCHSJetsCorrected
)

## sequence: AK8 Jets, PFCHS
process.HLTAK8PFCHSJetsReconstruction = cms.Sequence(
    process.particleFlowPtrs
  + process.goodOfflinePrimaryVertices
  + process.pfPileUpJME
  + process.pfNoPileUpJME
  + process.hltAK8PFCHSJets
  + process.hltAK8PFCHSJetCorrectorL1
  + process.hltAK8PFCHSJetCorrectorL2
  + process.hltAK8PFCHSJetCorrectorL3
  + process.hltAK8PFCHSJetCorrectorL2L3
  + process.hltAK8PFCHSJetCorrector
  + process.hltAK8PFCHSJetsCorrected
)

## sequence: AK4 Jets, Puppi
process.HLTAK4PuppiJetsReconstruction = cms.Sequence(
    process.hltPuppi
  + process.hltAK4PuppiJets
  + process.hltAK4PuppiJetCorrectorL1
  + process.hltAK4PuppiJetCorrectorL2
  + process.hltAK4PuppiJetCorrectorL3
  + process.hltAK4PuppiJetCorrectorL2L3
  + process.hltAK4PuppiJetCorrector
  + process.hltAK4PuppiJetsCorrected
)

## sequence: AK8 Jets, Puppi
process.HLTAK8PuppiJetsReconstruction = cms.Sequence(
    process.hltPuppi
  + process.hltAK8PuppiJets
  + process.hltAK8PuppiJetCorrectorL2
  + process.hltAK8PuppiJetCorrectorL3
  + process.hltAK8PuppiJetCorrectorL2L3
  + process.hltAK8PuppiJetCorrector
  + process.hltAK8PuppiJetsCorrected
)

## sequence: Puppi MET (Raw)
process.HLTPuppiMETReconstruction = cms.Sequence(
    process.hltPuppiNoLep
  + process.hltPuppiMET
)

## single-object filters
_singlePFJet100 = cms.EDFilter('HLT1PFJet',
  MaxEta = cms.double(5.0),
  MaxMass = cms.double(-1.0),
  MinE = cms.double(-1.0),
  MinEta = cms.double(-1.0),
  MinMass = cms.double(-1.0),
  MinN = cms.int32(1),
  MinPt = cms.double(100.0),
  inputTag = cms.InputTag(''),
  saveTags = cms.bool(True),
  triggerType = cms.int32(85),
)

process.hltSingleAK4PFJet100    = _singlePFJet100.clone(inputTag = 'hltAK4PFJetsCorrected'   , MinPt = 100.)
process.hltSingleAK4PFCHSJet100 = _singlePFJet100.clone(inputTag = 'hltAK4PFCHSJetsCorrected', MinPt = 100.)
process.hltSingleAK4PuppiJet100 = _singlePFJet100.clone(inputTag = 'hltAK4PuppiJetsCorrected', MinPt = 100.)

process.hltSingleAK8PFJet300    = _singlePFJet100.clone(inputTag = 'hltAK8PFJetsCorrected'   , MinPt = 300.)
process.hltSingleAK8PFCHSJet300 = _singlePFJet100.clone(inputTag = 'hltAK8PFCHSJetsCorrected', MinPt = 300.)
process.hltSingleAK8PuppiJet300 = _singlePFJet100.clone(inputTag = 'hltAK8PuppiJetsCorrected', MinPt = 300.)

_hltPFMET200 = cms.EDFilter('HLT1PFMET',
  MaxEta = cms.double(-1.0),
  MaxMass = cms.double(-1.0),
  MinE = cms.double(-1.0),
  MinEta = cms.double(-1.0),
  MinMass = cms.double(-1.0),
  MinN = cms.int32(1),
  MinPt = cms.double(200.0),
  inputTag = cms.InputTag('hltPFMET'),
  saveTags = cms.bool(True),
  triggerType = cms.int32(87),
)

process.hltPFMET200    = _hltPFMET200.clone(inputTag = 'hltPFMET'   , MinPt = 200.)
process.hltPFCHSMET200 = _hltPFMET200.clone(inputTag = 'hltPFCHSMET', MinPt = 200.)
process.hltPuppiMET200 = _hltPFMET200.clone(inputTag = 'hltPuppiMET', MinPt = 200.)

## paths
process.HLT_AK4PFJet100_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK4PFJetsReconstruction + process.hltSingleAK4PFJet100)
process.HLT_AK8PFJet300_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK8PFJetsReconstruction + process.hltSingleAK8PFJet300)

process.HLT_AK4PFCHSJet100_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK4PFCHSJetsReconstruction + process.hltSingleAK4PFCHSJet100)
process.HLT_AK8PFCHSJet300_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK8PFCHSJetsReconstruction + process.hltSingleAK8PFCHSJet300)

process.HLT_AK4PuppiJet100_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK4PuppiJetsReconstruction + process.hltSingleAK4PuppiJet100)
process.HLT_AK8PuppiJet300_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTAK8PuppiJetsReconstruction + process.hltSingleAK8PuppiJet300)

process.HLT_PFMET200_v1 = cms.Path(process.HLTParticleFlowSequence + process.hltPFMET + process.hltPFMET200)
process.HLT_PFCHSMET200_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTPFCHSMETReconstruction + process.hltPFCHSMET200)
process.HLT_PuppiMET200_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTPuppiMETReconstruction + process.hltPuppiMET200)

## schedule
process.schedule = cms.Schedule(*[
  process.raw2digi_step,

  process.HLT_AK4PFJet100_v1,
  process.HLT_AK4PFCHSJet100_v1,
  process.HLT_AK4PuppiJet100_v1,

  process.HLT_AK8PFJet300_v1,
  process.HLT_AK8PFCHSJet300_v1,
  process.HLT_AK8PuppiJet300_v1,

  process.HLT_PFMET200_v1,
  process.HLT_PFCHSMET200_v1,
  process.HLT_PuppiMET200_v1,
])

###
### job configuration (input, output, GT, etc)
###

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# fix for AK4PF Phase-2 JECs
process.GlobalTag.toGet.append(cms.PSet(
  record = cms.string('JetCorrectionsRecord'),
  tag = cms.string('JetCorrectorParametersCollection_PhaseIIFall17_V5b_MC_AK4PF'),
  label = cms.untracked.string('AK4PF'),
))

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# EDM input
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/02C1FCCC-315F-404C-ABF7-A65154C46C28.root',
   ]

# EDM output
process.RECOoutput = cms.OutputModule('PoolOutputModule',
  dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RECO'),
    filterName = cms.untracked.string('')
  ),
  fileName = cms.untracked.string(opts.output),
  outputCommands = cms.untracked.vstring((
    'drop *',
    'keep edmTriggerResults_*_*_*',
  )),
  splitLevel = cms.untracked.int32(0)
)

process.RECOoutput_step = cms.EndPath(process.RECOoutput)
process.schedule.append(process.RECOoutput_step)

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())
