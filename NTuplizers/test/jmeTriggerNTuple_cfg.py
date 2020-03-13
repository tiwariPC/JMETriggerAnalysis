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
### base configuration file
###
if opts.reco != '':
   from hltPhase2_cfg import cms, process
else:
   raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

###
### add analysis sequence (JMETrigger NTuple)
###
process.analysisCollectionsSequence = cms.Sequence()

### Muons
#process.load('JMETriggerAnalysis.NTuplizers.userMuons_cff')
#process.analysisCollectionsSequence *= process.userMuonsSequence
#
### Electrons
#process.load('JMETriggerAnalysis.NTuplizers.userElectrons_cff')
#process.analysisCollectionsSequence *= process.userElectronsSequence

## Event Selection (none yet)

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(),

  fillCollectionConditions = cms.PSet(),

  recoVertexCollections = cms.PSet(

    hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    particleFlowTmp = cms.InputTag('particleFlowTmp'),
#    hltPuppi = cms.InputTag('hltPuppi'),
#    hltPuppiForMET = cms.InputTag('hltPuppiForMET'),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJetsUncorrected = cms.InputTag('hltAK4CaloJets'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    hltAK4PFClusterJetsUncorrected = cms.InputTag('hltAK4PFClusterJets'),
    hltAK8PFClusterJetsUncorrected = cms.InputTag('hltAK8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJetsUncorrected = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),
    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),
    hltAK4PuppiJetsCorrected = cms.InputTag('hltAK4PuppiJetsCorrected'),
    hltAK8PuppiJetsCorrected = cms.InputTag('hltAK8PuppiJetsCorrected'),
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

    hltCaloMET = cms.InputTag('hltCaloMET'),
#    hltMetClean = cms.InputTag('hltMetClean'),
  ),

  recoPFClusterMETCollections = cms.PSet(

    hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMET'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
    hltPFMETCHS = cms.InputTag('hltPFMETCHS'),
    hltPFMETSoftKiller = cms.InputTag('hltPFMETSoftKiller'),
    hltPuppiMET = cms.InputTag('hltPuppiMET'),
    hltPuppiMETTypeOne = cms.InputTag('hltPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    offlineMETs = cms.InputTag('slimmedMETs'),
    offlineMETsPuppi = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(

#    offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'),
  ),

  patElectronCollections = cms.PSet(

#    offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'),
  ),

  stringCutObjectSelectors = cms.PSet(

    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    hltAK4CaloJetsUncorrected = cms.string('pt > 12'),

    hltAK4PFClusterJetsUncorrected = cms.string('pt > 12'),
    hltAK8PFClusterJetsUncorrected = cms.string('pt > 100'),

    hltAK4PFJetsUncorrected = cms.string('pt > 12'),
    hltAK4PFJetsCorrected = cms.string('pt > 12'),
    hltAK8PFJetsCorrected = cms.string('pt > 100'),
    hltAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    hltAK8PFCHSJetsCorrected = cms.string('pt > 100'),
    hltAK4PuppiJetsCorrected = cms.string('pt > 12'),
    hltAK8PuppiJetsCorrected = cms.string('pt > 100'),

    offlineAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    offlineAK4PuppiJetsCorrected = cms.string('pt > 12'),
    offlineAK8PuppiJetsCorrected = cms.string('pt > 100'),
  ),

  outputBranchesToBeDropped = cms.vstring(

    'offlinePrimaryVertices_tracksSize',

#    'hltPFMet_ChargedEMEtFraction',
#    'hltPFMetTypeOne_ChargedEMEtFraction',

    'genMetCalo_MuonEtFraction',
    'genMetCalo_InvisibleEtFraction',
  ),
)

process.analysisCollectionsPath = cms.Path(process.analysisCollectionsSequence)
process.schedule.extend([process.analysisCollectionsPath])

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.extend([process.analysisNTupleEndPath])

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

#   from Validation.RecoVertex.PrimaryVertexAnalyzer4PUSlimmed_cfi import vertexAnalysis, pixelVertexAnalysisPixelTrackingOnly
#   process.vertexAnalysis = vertexAnalysis.clone(vertexRecoCollections = ['offlinePrimaryVertices'])
#   process.pixelVertexAnalysis = pixelVertexAnalysisPixelTrackingOnly.clone(vertexRecoCollections = ['pixelVertices'])
#
#   process.trkMonitoringSeq += cms.Sequence(
#       process.vertexAnalysis
#     + process.pixelVertexAnalysis
#   )

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
   process.schedule.extend([process.trkMonitoringEndPath])

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
   process.schedule.extend([process.pfMonitoringEndPath])

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

   if opts.skimTracks:
      process.MessageLogger.debugModules += [
        'hltTrimmedPixelVertices',
        'generalTracks',
      ]

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Phase2HLTTDRWinter20RECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/MINIAODSIM/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/71D52D95-2372-4F4C-93BA-AAC6E86E28B7.root',
   ]

# input EDM files [secondary]
if opts.secondaryInputFiles:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = [
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/02C1FCCC-315F-404C-ABF7-A65154C46C28.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/04FE5F37-363A-714A-A1A3-7580076CF50E.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/05BFAD3E-3F91-1843-ABA2-2040324C7567.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/0701D254-5CF2-5C4E-A33F-62E453486DD0.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/150DC662-2DBE-214B-99BE-013C18454483.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/3C49CF8E-3E58-9643-A295-8CB91B4D9E69.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/42472BB0-D800-244B-B1D7-958E9A627D7B.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/4261F78B-F488-F444-A198-2A1319D5B854.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/46873CB9-C1DA-2242-99CC-76357F8F8DDE.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/4C90A453-54AE-4C44-AB89-789E24CEF23E.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/4F0FBB7F-AE69-4547-8863-02CF56F3BDFF.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/528C37EC-6C9B-E64F-82E1-7AF5DAD2C61F.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/5C4AD815-3815-8942-8E90-F79AE1C5FA64.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/6209D079-A984-CF4A-B002-243CA4D2CDB8.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/64E0D4F9-562D-224B-A060-EADD6859BFF3.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/650D4853-9B90-E24F-8423-1A8CACBE641F.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/67FB8B08-7E69-C543-9BBD-2ADFF5BACEA2.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/814608B9-7032-974F-88C0-9D789A3577BD.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/8B447C17-3E03-2C48-A9B2-81754BF050B5.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/9CCA0D97-4E83-3844-92B1-81D7AEA03BC8.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/A5CC6630-1EA2-2B49-8C1B-509E51649AFB.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/A978D1D7-2DAC-2448-B432-E4F9FAF04EF0.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/B363490C-3F4D-0F4B-B0BD-ED40B47BE99A.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/C632593D-EDC7-B84C-AC56-9A8193A4A687.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/DA2A29BE-BDF3-B845-997C-54EE15270D3E.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/E958B1A4-0414-CC4C-97FC-2BECA46F217E.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/F23960D9-581A-C14B-835F-3F7273D71BEB.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/FCDEFBBF-4B75-EE4D-A09B-1D19C4344785.root',
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/FF3E1196-D650-CD49-BAAF-4616A818CD16.root',
   ]

# skimming of tracks
if opts.skimTracks:

   from JMETriggerAnalysis.Common.hltPhase2_skimmedTracks import customize_hltPhase2_skimmedTracks
   process = customize_hltPhase2_skimmedTracks(process)

#   # modify PV inputs of Puppi collections
#   process.puppiNoLep.vertexName = process.generalTracks.vertices
#   process.hltPuppi.vertexName = process.generalTracks.vertices

   # add PV collections to JMETriggerNTuple
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet(
     hltPixelVertices = cms.InputTag('pixelVertices'),
     hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
     hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
   )

   process.JMETriggerNTuple.outputBranchesToBeDropped += [
     'hltPixelVertices_isFake',
     'hltPixelVertices_chi2',
     'hltPixelVertices_ndof',

     'hltTrimmedPixelVertices_isFake',
     'hltTrimmedPixelVertices_chi2',
     'hltTrimmedPixelVertices_ndof',
   ]

# print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: reco =', opts.reco
print 'option: skimTracks =', opts.skimTracks
print 'option: trkdqm =', opts.trkdqm
print 'option: pfdqm =', opts.pfdqm
print ''
print 'process.GlobalTag.globaltag =', process.GlobalTag.globaltag
print 'process.maxEvents =', process.maxEvents
print 'process.source =', process.source
print '-------------------------------'
