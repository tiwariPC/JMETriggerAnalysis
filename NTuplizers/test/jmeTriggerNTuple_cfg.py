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

opts.register('globalTag', None,
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
if opts.reco == 'HLT_TRKv00':
   from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv00_cfg import cms, process
elif opts.reco == 'HLT_TRKv02':
   from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv02_cfg import cms, process
elif opts.reco == 'HLT_TRKv06':
   from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv06_cfg import cms, process
else:
   raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

###
### add analysis sequence (JMETrigger NTuple)
###
process.analysisCollectionsSequence = cms.Sequence()

process.hltPuppiMETv0 = process.hltPuppiMET.clone(src = 'hltPuppi')
process.reconstruction += process.hltPuppiMETv0

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

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
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
#    hltCaloMETClean = cms.InputTag('hltMetClean'),
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
    hltPuppiMETv0 = cms.InputTag('hltPuppiMETv0'),
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
    # GEN
    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    # HLT AK4
    hltAK4CaloJets = cms.string('pt > 12'),
    hltAK4PFClusterJets = cms.string('pt > 12'),
    hltAK4PFJets = cms.string('pt > 12'),
    hltAK4PFJetsCorrected = cms.string('pt > 12'),
    hltAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    hltAK4PuppiJetsCorrected = cms.string('pt > 12'),

    # HLT AK8
    hltAK8CaloJets = cms.string('pt > 80'),
    hltAK8PFClusterJets = cms.string('pt > 80'),
    hltAK8PFJetsCorrected = cms.string('pt > 80'),
    hltAK8PFCHSJetsCorrected = cms.string('pt > 80'),
    hltAK8PuppiJetsCorrected = cms.string('pt > 80'),

    # Offline
    offlineAK4PFCHSJetsCorrected = cms.string('pt > 12'),
    offlineAK4PuppiJetsCorrected = cms.string('pt > 12'),
    offlineAK8PuppiJetsCorrected = cms.string('pt > 80'),
  ),

  outputBranchesToBeDropped = cms.vstring(

    'offlinePrimaryVertices_tracksSize',

#    'hltPFMET_ChargedEMEtFraction',
#    'hltPFMETTypeOne_ChargedEMEtFraction',

    'genMETCalo_MuonEtFraction',
    'genMETCalo_InvisibleEtFraction',
  ),
)

process.analysisCollectionsPath = cms.Path(process.analysisCollectionsSequence)
process.schedule.extend([process.analysisCollectionsPath])

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.extend([process.analysisNTupleEndPath])

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

   if reco == 'hltPhase2_TRKv02':
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
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate

   _candTags = [
     ('_simPFCands', 'simPFProducer', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPFCands', 'particleFlowTmp', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPuppiCands', 'hltPuppi', pfCandidateHistogrammerRecoPFCandidate),
     ('_offlinePFCands', 'packedPFCandidates', pfCandidateHistogrammerPatPackedCandidate),
   ]

   _regTags = [
     ['', ''],
     ['_HB', '(0.0<=abs(eta) && abs(eta)<1.5)'],
     ['_HGCal', '(1.5<=abs(eta) && abs(eta)<3.0)'],
     ['_HF', '(3.0<=abs(eta) && abs(eta)<5.0)'],
   ]

   _pidTags = [
     ['', ''],
     ['_chargedHadrons', '(abs(pdgId) == 211)'],
     ['_neutralHadrons', '(abs(pdgId) == 130)'],
     ['_photons', '(abs(pdgId) == 22)'],
   ]

   process.pfMonitoringSeq = cms.Sequence()
   for _candTag in _candTags:
     for _regTag in _regTags:
       for _pidTag in _pidTags:
         _modName = 'PFCandidateHistograms'+_candTag[0]+_regTag[0]+_pidTag[0]
         setattr(process, _modName, _candTag[2].clone(
           src = _candTag[1],
           cut = ' && '.join([_tmp for _tmp in [_regTag[1], _pidTag[1]] if _tmp]),
         ))
         process.pfMonitoringSeq += getattr(process, _modName)

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
if opts.secondaryInputFiles == ['None']:
   process.source.secondaryFileNames = []
elif opts.secondaryInputFiles != []:
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
print 'process.GlobalTag =', process.GlobalTag.dumpPython()
print 'process.source =', process.source.dumpPython()
print 'process.maxEvents =', process.maxEvents.dumpPython()
print 'process.options =', process.options.dumpPython()
print '-------------------------------'
