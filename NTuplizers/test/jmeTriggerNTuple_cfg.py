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

opts.register('gt', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'hltPhase2',
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
if opts.reco == 'hltPhase2':
   from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv02_cfg import cms, process
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

    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    particleFlowTmp = cms.InputTag('particleFlowTmp'),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJetsUncorrected = cms.InputTag(''),
    hltAK4CaloJetsCorrected = cms.InputTag(''),

    hltAK8CaloJetsUncorrected = cms.InputTag(''),
    hltAK8CaloJetsCorrected = cms.InputTag(''),
  ),

  recoPFClusterJetCollections = cms.PSet(
  ),

  recoPFJetCollections = cms.PSet(
    hltAK4PFJetsUncorrected = cms.InputTag(''),
    hltAK4PFJetsCorrected = cms.InputTag(''),

    hltAK4PFJetsUncorrected = cms.InputTag(''),
    hltAK4PFJetsCorrected = cms.InputTag(''),
  ),

  patJetCollections = cms.PSet(
  ),

  recoGenMETCollections = cms.PSet(
    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(
    hltCaloMET = cms.InputTag('hltMET'),
  ),

  recoPFClusterMETCollections = cms.PSet(
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMET'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
  ),

  patMuonCollections = cms.PSet(
  ),

  patElectronCollections = cms.PSet(
  ),

  stringCutObjectSelectors = cms.PSet(

    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    hltAK4CaloJetsUncorrected = cms.string('pt > 12'),
    hltAK4CaloJetsCorrected = cms.string('pt > 12'),

    hltAK8CaloJetsUncorrected = cms.string('pt > 80'),
    hltAK8CaloJetsCorrected = cms.string('pt > 80'),

    hltAK4PFJetsUncorrected = cms.string('pt > 12'),
    hltAK4PFJetsCorrected = cms.string('pt > 12'),

    hltAK8PFJetsUncorrected = cms.string('pt > 80'),
    hltAK8PFJetsCorrected = cms.string('pt > 80'),
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
   process.schedule.extend([process.reconstruction_pixelTrackingOnly_step])

   from JMETriggerAnalysis.Common.TrackHistogrammer_cfi import TrackHistogrammer
   process.TrackHistograms_pixelTracks = TrackHistogrammer.clone(src = 'pixelTracks')
   process.TrackHistograms_generalTracks = TrackHistogrammer.clone(src = 'generalTracks')

   from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
   process.VertexHistograms_pixelVertices = VertexHistogrammer.clone(src = 'pixelVertices')
   process.VertexHistograms_offlinePrimaryVertices = VertexHistogrammer.clone(src = 'offlinePrimaryVertices')

   process.trkMonitoringSeq = cms.Sequence(
       process.TrackHistograms_pixelTracks
     + process.TrackHistograms_generalTracks
   )

   if opts.skimTracks:
      process.TrackHistograms_generalTracksOriginal = TrackHistogrammer.clone(src = 'generalTracksOriginal')
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
   process.PFCandidateHistograms_hltPFCands = pfCandidateHistogrammerRecoPFCandidate.clone(src = 'particleFlowTmp')
   process.PFCandidateHistograms_hltPFCands_HB = process.PFCandidateHistograms_hltPFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_hltPFCands_HB_chargedHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPFCands_HB_neutralHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPFCands_HB_photons = process.PFCandidateHistograms_hltPFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_hltPFCands_HGCal = process.PFCandidateHistograms_hltPFCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_chargedHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut = 'abs(pdgId)==211 && (1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_neutralHadrons = process.PFCandidateHistograms_hltPFCands.clone(cut = 'abs(pdgId)==130 && (1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPFCands_HGCal_photons = process.PFCandidateHistograms_hltPFCands.clone(cut = 'abs(pdgId)==22  && (1.5<=abs(eta) && abs(eta)<3.0)')

   process.PFCandidateHistograms_hltPuppiCands = pfCandidateHistogrammerRecoPFCandidate.clone(src = 'hltPuppi')
   process.PFCandidateHistograms_hltPuppiCands_HB = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_hltPuppiCands_HB_chargedHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPuppiCands_HB_neutralHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPuppiCands_HB_photons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_hltPuppiCands_HGCal = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_chargedHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==211')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_neutralHadrons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==130')
   process.PFCandidateHistograms_hltPuppiCands_HGCal_photons = process.PFCandidateHistograms_hltPuppiCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==22')

   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate
   process.PFCandidateHistograms_offlinePFCands = pfCandidateHistogrammerPatPackedCandidate.clone(src = 'packedPFCandidates')
   process.PFCandidateHistograms_offlinePFCands_HB = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5)')
   process.PFCandidateHistograms_offlinePFCands_HB_chargedHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==211')
   process.PFCandidateHistograms_offlinePFCands_HB_neutralHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==130')
   process.PFCandidateHistograms_offlinePFCands_HB_photons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(0.0<=abs(eta) && abs(eta)<1.5) && abs(pdgId)==22')
   process.PFCandidateHistograms_offlinePFCands_HGCal = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0)')
   process.PFCandidateHistograms_offlinePFCands_HGCal_chargedHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==211')
   process.PFCandidateHistograms_offlinePFCands_HGCal_neutralHadrons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==130')
   process.PFCandidateHistograms_offlinePFCands_HGCal_photons = process.PFCandidateHistograms_offlinePFCands.clone(cut = '(1.5<=abs(eta) && abs(eta)<3.0) && abs(pdgId)==22')

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
     '/store/mc/Run3Winter20DRPremixMiniAOD/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/40000/A623EE66-618D-FC43-B4FC-6C4029CD68FB.root',
   ]

# input EDM files [secondary]
if opts.secondaryInputFiles == ['None']:
   process.source.secondaryFileNames = []
elif opts.secondaryInputFiles != []:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = []

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
