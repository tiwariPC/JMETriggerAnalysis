###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

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

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('gt', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'trkV2_110X_D49',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('trkdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected Tracks and Vertices')

opts.register('pfdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected PF-Candidates')

opts.register('skimTracks', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'skim original collection of generalTracks (only tracks associated to first N pixel vertices)')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### configuration file to re-run customized HLT Menu on RAW
###
if opts.reco == 'trkV0_110X_D41':
   from JMETriggerAnalysis.NTuplizers.step3_TrackingV0_110X_GeometryD41 import cms, process

elif opts.reco == 'trkV0_110X_D49':
   from JMETriggerAnalysis.NTuplizers.step3_TrackingV0_110X_GeometryD49 import cms, process

elif opts.reco == 'trkV2_110X_D41':
   from JMETriggerAnalysis.NTuplizers.step3_TrackingV2_110X_GeometryD41 import cms, process

elif opts.reco == 'trkV2_110X_D49':
   from JMETriggerAnalysis.NTuplizers.step3_TrackingV2_110X_GeometryD49 import cms, process

else:
   raise RuntimeError('invalid argument for option "reco": '+opts.reco)

# remove cms.EndPath for EDM output
del process.HLTOutput

# remove cms.EndPath for DQM output
del process.DQMFileSaverOutput

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

process.ak4CaloJets.doPVCorrection = False

# Calo AK4
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

# Calo AK8
process.ak8CaloJets = process.ak4CaloJets.clone(rParam = 0.8)

#process.ak8CaloL1FastjetCorrector = cms.EDProducer('L1FastjetCorrectorProducer',
#  algorithm = cms.string('AK8Calo'),
#  level = cms.string('L1FastJet'),
#  srcRho = cms.InputTag('fixedGridRhoFastjetAll'),
#)
#process.ak8CaloL2RelativeCorrector = cms.EDProducer('LXXXCorrectorProducer',
#  algorithm = cms.string('AK8Calo'),
#  level = cms.string('L2Relative'),
#)
#process.ak8CaloL3AbsoluteCorrector = cms.EDProducer('LXXXCorrectorProducer',
#  algorithm = cms.string('AK8Calo'),
#  level = cms.string('L3Absolute'),
#)
#process.ak8CaloL1FastL2L3Corrector = cms.EDProducer('ChainedJetCorrectorProducer',
#  correctors = cms.VInputTag('ak8CaloL1FastjetCorrector', 'ak8CaloL2RelativeCorrector', 'ak8CaloL3AbsoluteCorrector'),
#)
#process.ak8CaloJetsCorrected = cms.EDProducer('CorrectedCaloJetProducer',
#  correctors = cms.VInputTag('ak8CaloL1FastL2L3Corrector'),
#  src = cms.InputTag('ak8CaloJets'),
#)

# CaloJets Sequence
process.caloJetsSeq = cms.Sequence(
   (process.ak4CaloL1FastjetCorrector
  * process.ak4CaloL2RelativeCorrector
  * process.ak4CaloL3AbsoluteCorrector
  * process.ak4CaloL1FastL2L3Corrector
  * process.ak4CaloJetsCorrected)
  +(process.ak8CaloJets)
#  * process.ak8CaloL1FastjetCorrector
#  * process.ak8CaloL2RelativeCorrector
#  * process.ak8CaloL3AbsoluteCorrector
#  * process.ak8CaloL1FastL2L3Corrector
#  * process.ak8CaloJetsCorrected)
)
process.reconstruction *= process.caloJetsSeq

# PFClusterJets
process.load('RecoJets.JetProducers.PFClustersForJets_cff')

# PFClusterJets AK4
process.load('RecoJets.JetProducers.ak4PFClusterJets_cfi')
process.ak4PFClusterJets.doPVCorrection = False

# PFClusterJets AK8
process.ak8PFClusterJets = process.ak4PFClusterJets.clone(rParam = 0.8)

# PFClusterJets Sequence
process.pfClusterJetsSeq = cms.Sequence(
    process.pfClusterRefsForJets_step
  *(process.ak4PFClusterJets
  + process.ak8PFClusterJets)
)
process.reconstruction *= process.pfClusterJetsSeq

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
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
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

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJetsUncorrected = cms.InputTag('ak4CaloJets'),
    hltAK8CaloJetsUncorrected = cms.InputTag('ak8CaloJets'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    hltAK4PFClusterJetsUncorrected = cms.InputTag('ak4PFClusterJets'),
    hltAK8PFClusterJetsUncorrected = cms.InputTag('ak8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJetsUncorrected = cms.InputTag('ak4PFJets'+'::'+process.name_()),
    hltAK4PFJetsCorrected = cms.InputTag('ak4PFJetsCorrected'+'::'+process.name_()),
    hltAK4PFCHSJetsCorrected = cms.InputTag('ak4PFJetsCHSCorrected'+'::'+process.name_()),
    hltAK4PuppiJetsCorrected = cms.InputTag('hltAK4PuppiJetsCorrected'+'::'+process.name_()),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
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

    offlineMETs = cms.InputTag('slimmedMETs'),
    offlineMETsPuppi = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(

    offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'+'::'+process.name_()),
  ),

  patElectronCollections = cms.PSet(

    offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'+'::'+process.name_()),
  ),

  stringCutObjectSelectors = cms.PSet(

    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),
    hltAK4CaloJetsUncorrected = cms.string('pt > 12'),
    hltAK8CaloJetsUncorrected = cms.string('pt > 100'),
    hltAK4PFClusterJetsUncorrected = cms.string('pt > 12'),
    hltAK8PFClusterJetsUncorrected = cms.string('pt > 100'),
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

# update process.GlobalTag.globaltag
if opts.gt is not None:
   process.GlobalTag.globaltag = opts.gt

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)
if hasattr(process, 'DQMStore'):
   process.DQMStore.enableMultiThread = (process.options.numberOfThreads > 1)

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
   )

   if opts.skimTracks:
      process.TrackHistograms_generalTracksOriginal = TrackHistogrammer.clone(src = cms.InputTag('generalTracksOriginal'))
      process.trkMonitoringSeq += process.TrackHistograms_generalTracksOriginal

   process.trkMonitoringSeq += cms.Sequence(
       process.VertexHistograms_pixelVertices
     + process.VertexHistograms_offlinePrimaryVertices
   )

   from Validation.RecoVertex.PrimaryVertexAnalyzer4PUSlimmed_cfi import vertexAnalysis, pixelVertexAnalysisPixelTrackingOnly
   process.vertexAnalysis = vertexAnalysis.clone(vertexRecoCollections = ['offlinePrimaryVertices'])
   process.pixelVertexAnalysis = pixelVertexAnalysisPixelTrackingOnly.clone(vertexRecoCollections = ['pixelVertices'])

   process.trkMonitoringSeq += cms.Sequence(
       process.vertexAnalysis
     + process.pixelVertexAnalysis
   )

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)

# ParticleFlow Monitoring
if opts.pfdqm:

   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate
   process.PFCandidateHistograms_hltPFCands = pfCandidateHistogrammerRecoPFCandidate.clone(src='particleFlowTmp')
   process.PFCandidateHistograms_hltPFCands_HB = process.PFCandidateHistograms_hltPFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_hltPFCands_HB_chargedHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPFCands_HB_neutralHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPFCands_HB_photons = process.PFCandidateHistograms_hltPFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_hltPFCands_HGCal = process.PFCandidateHistograms_hltPFCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_chargedHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut='abs(pdgId)==211 && (1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_neutralHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut='abs(pdgId)==130 && (1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_photons = process.PFCandidateHistograms_hltPFCands.clone(cut='abs(pdgId)==22  && (1.5<=abs(eta) && abs(eta)<3.0)')

   process.PFCandidateHistograms_hltPuppiCands = pfCandidateHistogrammerRecoPFCandidate.clone(src='hltPuppi')
   process.PFCandidateHistograms_hltPuppiCands_HB = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_hltPuppiCands_HB_chargedHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPuppiCands_HB_neutralHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPuppiCands_HB_photons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_hltPuppiCands_HGCal = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_chargedHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_neutralHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_photons = process.PFCandidateHistograms_hltPuppiCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==22')

   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate
   process.PFCandidateHistograms_offlinePFCands = pfCandidateHistogrammerPatPackedCandidate.clone(src='packedPFCandidates')
   process.PFCandidateHistograms_offlinePFCands_HB = process.PFCandidateHistograms_offlinePFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_offlinePFCands_HB_chargedHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_offlinePFCands_HB_neutralHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_offlinePFCands_HB_photons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_offlinePFCands_HGCal = process.PFCandidateHistograms_offlinePFCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_offlinePFCands_HGCal_chargedHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==211')
   process.PFCandidateHistograms_offlinePFCands_HGCal_neutralHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==130')
   process.PFCandidateHistograms_offlinePFCands_HGCal_photons = process.PFCandidateHistograms_offlinePFCands.clone(cut='(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==22')

   process.pfMonitoringSeq = cms.Sequence(
       process.PFCandidateHistograms_hltPFCands
     + process.PFCandidateHistograms_hltPFCands_HB
     + process.PFCandidateHistograms_hltPFCands_HB_chargedHadrons
     + process.PFCandidateHistograms_hltPFCands_HB_neutralHadrons
     + process.PFCandidateHistograms_hltPFCands_HB_photons
     + process.PFCandidateHistograms_hltPFCands_HGCal
     + process.PFCandidateHistograms_hltPFCands_HGCal_chargedHadrons
     + process.PFCandidateHistograms_hltPFCands_HGCal_neutralHadrons
     + process.PFCandidateHistograms_hltPFCands_HGCal_photons
     + process.PFCandidateHistograms_hltPuppiCands
     + process.PFCandidateHistograms_hltPuppiCands_HB
     + process.PFCandidateHistograms_hltPuppiCands_HB_chargedHadrons
     + process.PFCandidateHistograms_hltPuppiCands_HB_neutralHadrons
     + process.PFCandidateHistograms_hltPuppiCands_HB_photons
     + process.PFCandidateHistograms_hltPuppiCands_HGCal
     + process.PFCandidateHistograms_hltPuppiCands_HGCal_chargedHadrons
     + process.PFCandidateHistograms_hltPuppiCands_HGCal_neutralHadrons
     + process.PFCandidateHistograms_hltPuppiCands_HGCal_photons
     + process.PFCandidateHistograms_offlinePFCands
     + process.PFCandidateHistograms_offlinePFCands_HB
     + process.PFCandidateHistograms_offlinePFCands_HB_chargedHadrons
     + process.PFCandidateHistograms_offlinePFCands_HB_neutralHadrons
     + process.PFCandidateHistograms_offlinePFCands_HB_photons
     + process.PFCandidateHistograms_offlinePFCands_HGCal
     + process.PFCandidateHistograms_offlinePFCands_HGCal_chargedHadrons
     + process.PFCandidateHistograms_offlinePFCands_HGCal_neutralHadrons
     + process.PFCandidateHistograms_offlinePFCands_HGCal_photons
   )

   process.pfMonitoringEndPath = cms.EndPath(process.pfMonitoringSeq)

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

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/MINIAODSIM/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/7589BB2C-3179-6345-86A5-D7F65C4F1D1D.root',
   ]

# input EDM files [secondary]
if opts.secondaryInputFiles:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = [
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/020785D6-2611-D64A-A1D8-6ADDEF8D5B15.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/137AD489-9669-7148-93B8-EB743460A028.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/1599C1F0-BC15-7F4F-A9D5-E3438A46C8CC.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/25D09A8F-8755-2D4B-882D-8082C9473523.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/27C7CA8C-A923-4A4D-ABAB-345E74B3F6DC.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/37623260-89AF-2346-8D02-9382F14EC018.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/3F0BF703-1344-C546-AFB1-78824B21A022.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/6EBEF926-DD6D-9449-9D42-F8BAA3AAF462.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/70869742-728C-2946-B84D-76446E63715F.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/76022194-556D-6F4C-934C-EEA17BF845A5.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/7A9A5194-B02F-9B45-A39F-138FFCB2B4B4.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/91710CF1-D996-A049-82AB-587BF73D66BC.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/9FD78B49-8535-4B44-AAD1-CB067B0F1D06.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/A33FBE94-FE94-8B4C-AD1F-B6667277BF48.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/A63C0692-51BC-7C4B-8616-4B1662974193.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/ACB652A4-27AA-2544-BC62-28CC1C306D0C.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/BBBF1CD9-BCA8-8E42-AEFF-4F31CBBA5FE2.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/C3733900-B5E4-CB40-88BB-9D5DE956BBEF.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/C6A51DBE-8A25-E449-8B31-827C3B13EAFE.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/C6D607BE-7C36-7040-AC34-95DDA535C401.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/DF714427-4FDF-A543-9B60-2900AFD09503.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/E45E11CE-168D-9747-A0B7-33BD0AA8ECC8.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/EAB22C54-165E-5847-8431-DFBAC441B238.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/EC195DA2-5129-3549-BEC4-03F5ADB857C1.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/EE316A70-3F31-7448-95DB-8C5468A46E2B.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/F7124A73-16AA-4847-BE9E-C649BFCC7ECB.root',
     '/store/relval/CMSSW_11_0_0/RelValQCD_Pt15To7000_Flat_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/20000/FC222052-E9BD-E94E-BC38-867DA59C3326.root',
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

#   # modify PV inputs of Puppi collections
#   process.puppiNoLep.vertexName = process.generalTracks.vertices
#   process.hltPuppi.vertexName = process.generalTracks.vertices

   # add PV collections to JMETriggerNTuple
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet(
     hltPixelVertices = cms.InputTag('pixelVertices'+'::'+process.name_()),
     hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'+'::'+process.name_()),
     hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'+'::'+process.name_()),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
   )

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: reco =', opts.reco
print 'option: skimTracks =', opts.skimTracks
print 'option: trkdqm =', opts.trkdqm
print 'option: pfdqm =', opts.pfdqm
print 'option: dumpPython =', opts.dumpPython
print ''
print 'process.GlobalTag.globaltag =', process.GlobalTag.globaltag
print 'process.maxEvents =', process.maxEvents
print 'process.source =', process.source
print '-------------------------------'
