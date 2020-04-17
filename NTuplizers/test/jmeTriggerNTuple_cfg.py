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

opts.register('reco', 'HLT',
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

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
###
if opts.reco == 'HLT':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process

elif opts.reco == 'HLT_trkIter2GlobalPtSeed0p9':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   from JMETriggerAnalysis.NTuplizers.customise_HLT_trkIter2Global import *
   process = customise_HLT_trkIter2Global(process, ptMin = 0.9)

elif opts.reco == 'HLT_pfBlockAlgoRemovePS':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   from JMETriggerAnalysis.NTuplizers.customise_HLT_pfBlockAlgoRemovePS import *
   process = customise_HLT_pfBlockAlgoRemovePS(process)

elif opts.reco == 'HLT_trkIter2RegionalPtSeed0p9':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 0.9

elif opts.reco == 'HLT_trkIter2RegionalPtSeed2p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 2.0

elif opts.reco == 'HLT_trkIter2RegionalPtSeed5p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 5.0

elif opts.reco == 'HLT_trkIter2RegionalPtSeed10p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_V5_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 10.0

elif opts.reco == 'HLT_globalPixelTracks_v01':
   from JMETriggerAnalysis.NTuplizers.HLT_globalPixelTracks_v01 import cms, process

   ## enforce sorting of Pixel Vertices
   process.hltUnsortedPixelVertices = process.hltPixelVertices.clone()

   process.hltPixelVertices = cms.EDProducer('PixelVerticesSelector',

     src = cms.InputTag('hltUnsortedPixelVertices'),

     minSumPt2 = cms.double( -1. ),
     minSumPt2FractionWrtMax = cms.double( -1. ),

     # criterion to rank pixel vertices
     # (utilizes PVClusterComparer to compute
     # the vertex SumPtSquared f.o.m. using a sub-set of tracks)
     ranker = cms.PSet(
       refToPSet_ = cms.string('HLTPSetPvClusterComparerForIT')
#       track_chi2_max = cms.double( 20.0 ),
#       track_pt_max = cms.double( 20.0 ),
#       track_prob_min = cms.double( -1.0 ),
#       track_pt_min = cms.double( 1.0 )
     ),

     # retain only first N vertices
     maxNVertices = cms.int32( -1 ),
   )

   process.HLTRecopixelvertexingSequence.insert(
     process.HLTRecopixelvertexingSequence.index(process.hltPixelVertices),
     process.hltUnsortedPixelVertices
   )

   ## modules
   process.hltParticleFlowNoMu = cms.EDFilter('GenericPFCandidateSelector',
     src = cms.InputTag('hltParticleFlow'),
     cut = cms.string('particleId != 3'),
   )

   process.hltPFMETNoMuProducer = cms.EDProducer('PFMETProducer',
     alias = cms.string('pfMetNoMu'),
     calculateSignificance = cms.bool(False),
     globalThreshold = cms.double(0.0),
     src = cms.InputTag('hltParticleFlowNoMu')
   )

   ## add path: MC_AK4PFJets_v1
   process.hltPreMCAK4PFJets = cms.EDFilter('HLTPrescaler',
     L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
     offset = cms.uint32(0)
   )

   process.hltAK4PFJetCollection20Filter = cms.EDFilter('HLT1PFJet',
     MaxEta = cms.double(3.0),
     MaxMass = cms.double(-1.0),
     MinE = cms.double(-1.0),
     MinEta = cms.double(-1.0),
     MinMass = cms.double(-1.0),
     MinN = cms.int32(1),
     MinPt = cms.double(20.0),
     inputTag = cms.InputTag('hltAK4PFJetsCorrected'),
     saveTags = cms.bool(True),
     triggerType = cms.int32(85)
   )

   process.MC_AK4PFJets_v1 = cms.Path(
       process.HLTBeginSequence
     + process.hltPreMCAK4PFJets
     + process.HLTAK4PFJetsSequence
     + process.hltAK4PFJetCollection20Filter
     + process.HLTEndSequence
   )

   ## add path: MC_PFMETNoMu_v1
   process.hltPreMCPFMET = cms.EDFilter('HLTPrescaler',
     L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
     offset = cms.uint32(0)
   )

   process.hltPFMETOpenFilter = cms.EDFilter('HLT1PFMET',
     MaxEta = cms.double(-1.0),
     MaxMass = cms.double(-1.0),
     MinE = cms.double(-1.0),
     MinEta = cms.double(-1.0),
     MinMass = cms.double(-1.0),
     MinN = cms.int32(1),
     MinPt = cms.double(-1.0),
     inputTag = cms.InputTag('hltPFMETProducer'),
     saveTags = cms.bool(True),
     triggerType = cms.int32(87)
   )

   process.MC_PFMET_v1 = cms.Path(
       process.HLTBeginSequence
     + process.hltPreMCPFMET
     + process.HLTAK4PFJetsSequence
     + process.hltPFMETProducer
     + process.hltPFMETOpenFilter
     + process.HLTEndSequence
   )

   ## add path: MC_CaloMET_v1
   process.hltPreMCCaloMET = process.hltPreMCPFMET.clone()

   process.hltCaloMETOpenFilter = cms.EDFilter('HLT1CaloMET',
     MaxEta = cms.double(-1.0),
     MaxMass = cms.double(-1.0),
     MinE = cms.double(-1.0),
     MinEta = cms.double(-1.0),
     MinMass = cms.double(-1.0),
     MinN = cms.int32(1),
     MinPt = cms.double(0.0),
     inputTag = cms.InputTag('hltMet'),
     saveTags = cms.bool(True),
     triggerType = cms.int32(87)
   )

   process.MC_CaloMET_v1 = cms.Path(
       process.HLTBeginSequence
     + process.hltPreMCCaloMET
     + process.HLTRecoMETSequence
     + process.hltCaloMETOpenFilter
     + process.HLTEndSequence
   )

else:
   raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

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

## remove selected cms.Path objects from HLT config-dump
#for _modname in process.paths_():
#    if _modname.startswith('HLT_') or _modname.startswith('MC_'):
#       _mod = getattr(process, _modname)
#       if type(_mod) == cms.Path:
#          process.__delattr__(_modname)
#          print '> removed cms.Path:', _modname

# delete process.MessaggeLogger from HLT config
if hasattr(process, 'MessageLogger'):
   del process.MessageLogger

## add path: MC_PFMETNoMu_v1
process.hltPreMCPFMETNoMu = process.hltPreMCPFMET.clone()

process.hltPFMETNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPFMETNoMuProducer'
)

process.HLTParticleFlowJMESequence = cms.Sequence(
    process.HLTPreAK4PFJetsRecoSequence
  + process.HLTL2muonrecoSequence
  + process.HLTL3muonrecoSequence
  + process.HLTTrackReconstructionForPF
  + process.HLTParticleFlowSequence
)

process.MC_PFMETNoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPFMETNoMu
  + process.HLTParticleFlowJMESequence
  + process.hltParticleFlowNoMu
  + process.hltPFMETNoMuProducer
  + process.hltPFMETNoMuOpenFilter
  + process.HLTEndSequence
)

## add path: MC_AK4PuppiJets_v1
process.hltPreMCAK4PuppiJets = process.hltPreMCAK4PFJets.clone()

from CommonTools.PileupAlgos.Puppi_cff import *
process.hltPuppi = puppi.clone(
  candName = 'hltParticleFlow',
  vertexName = 'hltPixelVertices',
  vtxNdofCut = 0,
)

process.HLTPuppiSequence = cms.Sequence(
    process.HLTParticleFlowJMESequence
  + process.hltPuppi
)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi
process.hltAK4PuppiJets = ak4PFJetsPuppi.clone(
  src = 'hltPuppi',
)

process.HLTAK4PuppiJetsSequence = cms.Sequence(
    process.HLTPuppiSequence
  + process.hltAK4PuppiJets
)

process.hltAK4PuppiJetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
  inputTag = 'hltAK4PuppiJets'
)

process.MC_AK4PuppiJets_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCAK4PuppiJets
  + process.HLTAK4PuppiJetsSequence
  + process.hltAK4PuppiJetCollection20Filter
  + process.HLTEndSequence
)

## add path: MC_PuppiMETv0_v1
process.hltPreMCPuppiMETv0 = process.hltPreMCPFMET.clone()

process.hltPuppiMETv0 = process.hltPFMETProducer.clone(
  src = 'hltPuppi',
  alias = ''
)

process.HLTPuppiMETv0Sequence = cms.Sequence(
    process.HLTPuppiSequence
  + process.hltPuppiMETv0
)

process.hltPuppiMETv0OpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPuppiMETv0'
)

process.MC_PuppiMETv0_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv0
  + process.HLTPuppiMETv0Sequence
  + process.hltPuppiMETv0OpenFilter
  + process.HLTEndSequence
)

## add path: MC_PuppiMETv0NoMu_v1
process.hltPreMCPuppiMETv0NoMu = process.hltPreMCPFMET.clone()

process.hltPuppiNoMu = process.hltParticleFlowNoMu.clone(src = 'hltPuppi')

process.hltPuppiMETv0NoMu = process.hltPFMETProducer.clone(
  src = 'hltPuppiNoMu',
  alias = ''
)

process.HLTPuppiMETv0NoMuSequence = cms.Sequence(
    process.HLTPuppiSequence
  + process.hltPuppiNoMu
  + process.hltPuppiMETv0NoMu
)

process.hltPuppiMETv0NoMuOpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPuppiMETv0NoMu'
)

process.MC_PuppiMETv0NoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv0NoMu
  + process.HLTPuppiMETv0NoMuSequence
  + process.hltPuppiMETv0NoMuOpenFilter
  + process.HLTEndSequence
)

## add path: MC_PuppiMETv1_v1
process.hltPreMCPuppiMETv1 = process.hltPreMCPFMET.clone()

# Puppi candidates for MET
process.hltParticleFlowNoLeptons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( 1, 2, 22, 111, 130, 310, 2112, 211, -211, 321, -321, 999211, 2212, -2212 )
)
process.hltParticleFlowLeptons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( -11, 11, -13, 13 ),
)
process.hltPuppiNoLeptons = puppi.clone(
  candName = 'hltParticleFlowNoLeptons',
  vertexName = 'hltPixelVertices',
  PtMaxPhotons = 20.,
  vtxNdofCut = 0,
)
process.hltPuppiForMET = cms.EDProducer('CandViewMerger',
  src = cms.VInputTag( 'hltPuppiNoLeptons', 'hltParticleFlowLeptons' ),
)

process.HLTPuppiForMETSequence = cms.Sequence(
    process.HLTParticleFlowJMESequence
  + process.hltParticleFlowNoLeptons
  + process.hltParticleFlowLeptons
  + process.hltPuppiNoLeptons
  + process.hltPuppiForMET
)

process.hltPuppiMETv1 = process.hltPFMETProducer.clone(
  src = 'hltPuppiForMET',
  alias = ''
)

process.HLTPuppiMETv1Sequence = cms.Sequence(
    process.HLTPuppiForMETSequence
  + process.hltPuppiMETv1
)

process.hltPuppiMETv1OpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPuppiMETv1'
)

process.MC_PuppiMETv1_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv1
  + process.HLTPuppiMETv1Sequence
  + process.hltPuppiMETv1OpenFilter
  + process.HLTEndSequence
)

## add path: MC_PuppiMETv1NoMu_v1
process.hltPreMCPuppiMETv1NoMu = process.hltPreMCPFMET.clone()

process.hltParticleFlowElectrons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( -11, 11 ),
)
process.hltPuppiForMETNoMu = process.hltPuppiForMET.clone(
  src = ['hltPuppiNoLeptons', 'hltParticleFlowElectrons'],
)

process.HLTPuppiForMETNoMuSequence = cms.Sequence(
    process.HLTParticleFlowJMESequence
  + process.hltParticleFlowNoLeptons
  + process.hltParticleFlowElectrons
  + process.hltPuppiNoLeptons
  + process.hltPuppiForMETNoMu
)

process.hltPuppiMETv1NoMu = process.hltPFMETProducer.clone(
  src = 'hltPuppiForMETNoMu',
  alias = ''
)

process.HLTPuppiMETv1NoMuSequence = cms.Sequence(
    process.HLTPuppiForMETNoMuSequence
  + process.hltPuppiMETv1NoMu
)

process.hltPuppiMETv1NoMuOpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPuppiMETv1NoMu'
)

process.MC_PuppiMETv1NoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv1NoMu
  + process.HLTPuppiMETv1NoMuSequence
  + process.hltPuppiMETv1NoMuOpenFilter
  + process.HLTEndSequence
)

## add path: MC_AK4PFCHSJets_v1
process.hltPreMCAK4PFCHSJets = process.hltPreMCAK4PFJets.clone()

process.hltParticleFlowPtrs = cms.EDProducer('PFCandidateFwdPtrProducer',
  src = cms.InputTag('hltParticleFlow')
)
process.hltParticleFlowPileUpJME = cms.EDProducer('PFPileUp',
  Enable = cms.bool(True),
  PFCandidates = cms.InputTag('hltParticleFlowPtrs'),
  Vertices = cms.InputTag('hltPixelVertices'),
  checkClosestZVertex = cms.bool(True),
  verbose = cms.untracked.bool(False)
)
process.hltParticleFlowNoPileUpJME = cms.EDProducer('TPPFCandidatesOnPFCandidates',
  enable = cms.bool(True),
  bottomCollection = cms.InputTag('hltParticleFlowPtrs'),
  name = cms.untracked.string('pileUpOnPFCandidates'),
  topCollection = cms.InputTag('hltParticleFlowPileUpJME'),
  verbose = cms.untracked.bool(False)
)

process.HLTParticleFlowCHSPtrsSequence = cms.Sequence(
    process.HLTParticleFlowJMESequence
  + process.hltParticleFlowPtrs
  + process.hltParticleFlowPileUpJME
  + process.hltParticleFlowNoPileUpJME
)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsCHS
process.hltAK4PFCHSJets = ak4PFJetsCHS.clone(
  src = 'hltParticleFlowNoPileUpJME',
)

process.HLTAK4PFCHSJetsSequence = cms.Sequence(
    process.HLTParticleFlowCHSPtrsSequence
  + process.hltAK4PFCHSJets
)

process.hltAK4PFCHSJetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
  inputTag = 'hltAK4PFCHSJets'
)

process.MC_AK4PFCHSJets_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCAK4PFCHSJets
  + process.HLTAK4PFCHSJetsSequence
  + process.hltAK4PFCHSJetCollection20Filter
  + process.HLTEndSequence
)

## add path: MC_PFCHSMET_v1
process.hltPreMCPFCHSMET = process.hltPreMCPFMET.clone()

process.hltParticleFlowCHS = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
  src = process.hltAK4PFCHSJets.src,
)

process.hltPFCHSMET = process.hltPFMETProducer.clone(
  src = 'hltParticleFlowCHS',
  alias = ''
)

process.HLTPFCHSMETSequence = cms.Sequence(
    process.HLTParticleFlowCHSPtrsSequence
  + process.hltParticleFlowCHS
  + process.hltPFCHSMET
)

process.hltPFCHSMETOpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPFCHSMET'
)

process.MC_PFCHSMET_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPFCHSMET
  + process.HLTPFCHSMETSequence
  + process.hltPFCHSMETOpenFilter
  + process.HLTEndSequence
)

## add path: MC_AK4PFCHSJetsV2_v1
if not hasattr(process, 'hltVerticesPF'):
   process.hltVerticesPF = cms.EDProducer('PrimaryVertexProducer',
     TkClusParameters = cms.PSet(
        TkDAClusParameters = cms.PSet(
            Tmin = cms.double(2.4),
            Tpurge = cms.double(2.0),
            Tstop = cms.double(0.5),
            coolingFactor = cms.double(0.6),
            d0CutOff = cms.double(999.0),
            dzCutOff = cms.double(4.0),
            uniquetrkweight = cms.double(0.9),
            use_vdt = cms.untracked.bool(True),
            vertexSize = cms.double(0.15),
            zmerge = cms.double(0.01)
        ),
        algorithm = cms.string('DA_vect')
     ),
     TkFilterParameters = cms.PSet(
        algorithm = cms.string('filter'),
        maxD0Significance = cms.double(999.0),
        maxEta = cms.double(100.0),
        maxNormalizedChi2 = cms.double(20.0),
        minPixelLayersWithHits = cms.int32(2),
        minPt = cms.double(0.0),
        minSiliconLayersWithHits = cms.int32(5),
        trackQuality = cms.string('any')
     ),
     TrackLabel = cms.InputTag('hltPFMuonMerging'),
     beamSpotLabel = cms.InputTag('hltOnlineBeamSpot'),
     verbose = cms.untracked.bool(False),
     vertexCollections = cms.VPSet(
        cms.PSet(
            algorithm = cms.string('AdaptiveVertexFitter'),
            chi2cutoff = cms.double(3.0),
            label = cms.string(''),
            maxDistanceToBeam = cms.double(1.0),
            minNdof = cms.double(0.0),
            useBeamConstraint = cms.bool(False)
        ),
        cms.PSet(
            algorithm = cms.string('AdaptiveVertexFitter'),
            chi2cutoff = cms.double(3.0),
            label = cms.string('WithBS'),
            maxDistanceToBeam = cms.double(1.0),
            minNdof = cms.double(0.0),
            useBeamConstraint = cms.bool(True)
        )
     )
   )

if not hasattr(process, 'hltVerticesPFSelector'):
   process.hltVerticesPFSelector = cms.EDFilter('PrimaryVertexObjectFilter',
     filterParams = cms.PSet(
       maxRho = cms.double(2.0),
       maxZ = cms.double(24.0),
       minNdof = cms.double(4.0),
       pvSrc = cms.InputTag('hltVerticesPF')
     ),
     src = cms.InputTag('hltVerticesPF')
   )

if not hasattr(process, 'hltVerticesPFFilter'):
   process.hltVerticesPFFilter = cms.EDFilter('VertexSelector',
     cut = cms.string('!isFake'),
     filter = cms.bool(True),
     src = cms.InputTag('hltVerticesPFSelector')
   )

process.hltPreMCAK4PFCHSJetsV2 = process.hltPreMCAK4PFJets.clone()

process.hltParticleFlowPileUpJMEv2 = cms.EDProducer('PFPileUp',
  Enable = cms.bool(True),
  PFCandidates = cms.InputTag('hltParticleFlowPtrs'),
  Vertices = cms.InputTag('hltVerticesPFFilter'),
  checkClosestZVertex = cms.bool(False),
  verbose = cms.untracked.bool(True)
)
process.hltParticleFlowNoPileUpJMEv2 = cms.EDProducer('TPPFCandidatesOnPFCandidates',
  enable = cms.bool(True),
  bottomCollection = cms.InputTag('hltParticleFlowPtrs'),
  name = cms.untracked.string('pileUpOnPFCandidates'),
  topCollection = cms.InputTag('hltParticleFlowPileUpJMEv2'),
  verbose = cms.untracked.bool(False)
)

process.HLTParticleFlowCHSPtrsV2Sequence = cms.Sequence(
    process.HLTParticleFlowJMESequence
  + process.hltVerticesPF
  + process.hltVerticesPFSelector
  + process.hltVerticesPFFilter
  + process.hltParticleFlowPtrs
  + process.hltParticleFlowPileUpJMEv2
  + process.hltParticleFlowNoPileUpJMEv2
)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsCHS
process.hltAK4PFCHSJetsV2 = ak4PFJetsCHS.clone(
  src = 'hltParticleFlowNoPileUpJMEv2',
)

process.HLTAK4PFCHSJetsV2Sequence = cms.Sequence(
    process.HLTParticleFlowCHSPtrsV2Sequence
  + process.hltAK4PFCHSJetsV2
)

process.hltAK4PFCHSJetsV2Collection20Filter = process.hltAK4PFJetCollection20Filter.clone(
  inputTag = 'hltAK4PFCHSJetsV2'
)

process.MC_AK4PFCHSJetsV2_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCAK4PFCHSJetsV2
  + process.HLTAK4PFCHSJetsV2Sequence
  + process.hltAK4PFCHSJetsV2Collection20Filter
  + process.HLTEndSequence
)

## add path: MC_PFCHSMETv2_v1
process.hltPreMCPFCHSMETv2 = process.hltPreMCPFMET.clone()

process.hltParticleFlowCHSv2 = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
  src = process.hltAK4PFCHSJetsV2.src,
)

process.hltPFCHSMETv2 = process.hltPFMETProducer.clone(
  src = 'hltParticleFlowCHSv2',
  alias = ''
)

process.HLTPFCHSMETv2Sequence = cms.Sequence(
    process.HLTParticleFlowCHSPtrsV2Sequence
  + process.hltParticleFlowCHSv2
  + process.hltPFCHSMETv2
)

process.hltPFCHSMETv2OpenFilter = process.hltPFMETOpenFilter.clone(
  inputTag = 'hltPFCHSMETv2'
)

process.MC_PFCHSMETv2_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPFCHSMETv2
  + process.HLTPFCHSMETv2Sequence
  + process.hltPFCHSMETv2OpenFilter
  + process.HLTEndSequence
)

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

  recoVertexCollections = cms.PSet(
    hltUnsortedPixelVertices = cms.InputTag('hltUnsortedPixelVertices'),#!!
    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPFFilter = cms.InputTag('hltVerticesPFFilter'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),#!!
    hltParticleFlowCHS = cms.InputTag('hltParticleFlowCHS'),#!!
    hltParticleFlowCHSv2 = cms.InputTag('hltParticleFlowCHSv2'),#!!
  ),

  patPackedCandidateCollections = cms.PSet(
    offlineParticleFlow = cms.InputTag('packedPFCandidates'),#!!
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
  ),

  recoPFJetCollections = cms.PSet(
    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    hltAK4PFCHSJetsV2 = cms.InputTag('hltAK4PFCHSJetsV2'),
    hltAK4PuppiJets = cms.InputTag('hltAK4PuppiJets'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
  ),

  patJetCollections = cms.PSet(
    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
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
    hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    hltPFCHSMETv2 = cms.InputTag('hltPFCHSMETv2'),
    hltPuppiMETv0 = cms.InputTag('hltPuppiMETv0'),
    hltPuppiMETv0NoMu = cms.InputTag('hltPuppiMETv0NoMu'),
    hltPuppiMETv1 = cms.InputTag('hltPuppiMETv1'),
    hltPuppiMETv1NoMu = cms.InputTag('hltPuppiMETv1NoMu'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
    offlineMETs = cms.InputTag('slimmedMETs'),
    offlineMETsPuppi = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(
    offlineMuons = cms.InputTag(userMuonsCollection)
  ),

  patElectronCollections = cms.PSet(
  ),

  stringCutObjectSelectors = cms.PSet(
    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    hltAK4CaloJets = cms.string('pt > 20'),
    hltAK4CaloJetsCorrected = cms.string('pt > 20'),

    hltAK8CaloJets = cms.string('pt > 80'),
    hltAK8CaloJetsCorrected = cms.string('pt > 80'),

    hltAK4PFJets = cms.string('pt > 20'),
    hltAK4PFCHSJets = cms.string('pt > 20'),
    hltAK4PFCHSJetsV2 = cms.string('pt > 20'),
    hltAK4PuppiJets = cms.string('pt > 20'),
    hltAK4PFJetsCorrected = cms.string('pt > 20'),

    hltAK8PFJets = cms.string('pt > 80'),
    hltAK8PFJetsCorrected = cms.string('pt > 80'),

    offlineAK4PFCHSJetsCorrected = cms.string('pt > 20'),
    offlineAK4PuppiJetsCorrected = cms.string('pt > 20'),
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
     'hltMergedTracks',
     'hltIter0PFlowTrackSelectionHighPurity',
   ]:
     if hasattr(process, _trkColl):
        setattr(process, 'TrackHistograms_'+_trkColl, TrackHistogrammer.clone(src = _trkColl))
        process.trkMonitoringSeq += getattr(process, 'TrackHistograms_'+_trkColl)

   # vertices
   from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
   for _vtxColl in [
     'hltPixelVertices',
     'hltTrimmedPixelVertices',
     'hltVerticesPFFilter',
   ]:
     if hasattr(process, _vtxColl):
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
if opts.pfdqm:
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate

   _candTags = [
     ('_hltParticleFlow', 'hltParticleFlow', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltParticleFlowCHS', 'hltParticleFlowCHS', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltParticleFlowCHSv2', 'hltParticleFlowCHSv2', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPuppi', 'hltPuppi', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
     ('_offlineParticleFlow', 'packedPFCandidates', '', pfCandidateHistogrammerPatPackedCandidate),
   ]

   _regTags = [
     ['', ''],
     ['_HB', '(0.0<=abs(eta) && abs(eta)<1.3)'],
     ['_HE', '(1.3<=abs(eta) && abs(eta)<3.0)'],
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
