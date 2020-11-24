###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('output', 'PFHadronCalibration.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
###
from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg import cms, process

process.particleFlowSimParticle = cms.EDProducer('PFSimParticleProducer',
  Fitter = cms.string('KFFittingSmoother'),
  MCTruthMatchingInfo = cms.untracked.bool(False),
  ParticleFilter = cms.PSet(
    EMin = cms.double(0),
    chargedPtMin = cms.double(0),
    etaMax = cms.double(5.3),
    invisibleParticles = cms.vint32(),
    protonEMin = cms.double(5000.0),
    rMax = cms.double(129.0),
    zMax = cms.double(317.0),
  ),
  Propagator = cms.string('PropagatorWithMaterial'),
  RecTracks = cms.InputTag('trackerDrivenElectronSeeds'),
  TTRHBuilder = cms.string('WithTrackAngle'),
  ecalRecHitsEB = cms.InputTag('caloRecHits','EcalRecHitsEB'),
  ecalRecHitsEE = cms.InputTag('caloRecHits','EcalRecHitsEE'),
  fastSimProducer = cms.untracked.InputTag('fastSimProducer','EcalHitsEB'),
  process_Particles = cms.untracked.bool(True),
  process_RecTracks = cms.untracked.bool(False),
  sim = cms.InputTag('g4SimHits'),
  verbose = cms.untracked.bool(False)
)

process.pfHadCalibNTuplePFBarrel = cms.EDAnalyzer('PFHadCalibNTuple',
  TTreeName = cms.string('Candidates'),

  genParticles = cms.InputTag('genParticles'),
  pfSimParticles = cms.InputTag('particleFlowSimParticle'),
  recoPFCandidates = cms.InputTag('particleFlowTmpBarrel'),

  genParticleStatus = cms.int32(1), # status code of selected GEN particles
  genParticlePdgId = cms.int32(-211), # pdgID of selected GEN particles
  genParticleIsoMinDeltaR = cms.double(1.0), # min deltaR between "isolated" GEN particles and other GEN particles

  minPt = cms.double(0.01), # min pt
  minTrackP = cms.double(0.01),  # min track momentum
  minTrackPt = cms.double(0.01),  # min track transverse momentum
  minCaloEnergy = cms.double(0.0),  # min ecal+hcal energy
  maxECalEnergy = cms.double(1e12), # max ecal energy

  # min nb of pixel and pixel+strip hits (per track-eta range)
  minPixelHits = cms.vuint32(2, 2, 2, 2, 2),
  minTrackerHits = cms.vuint32(2, 2, 2, 2, 2),
  maxEtaForMinTrkHitsCuts = cms.vdouble(1.4, 1.6, 2.0, 2.5, 999.0),

  usePFBlockElements = cms.bool(True),
)

process.pfHadCalibNTuplePFTICL = process.pfHadCalibNTuplePFBarrel.clone(
  recoPFCandidates = 'pfTICL',
  usePFBlockElements = False,
)

process.pfSimParticleSeq = cms.Sequence(process.particleFlowSimParticle)
process.pfSimParticlePath = cms.Path(process.pfSimParticleSeq)

process.pfHadCalibNTupleSeq = cms.Sequence(
    process.pfHadCalibNTuplePFBarrel
  + process.pfHadCalibNTuplePFTICL
)
process.pfHadCalibNTupleEndPath = cms.EndPath(process.pfHadCalibNTupleSeq)

process.setSchedule_(cms.Schedule(
  process.MC_JME,
  process.pfSimParticlePath,
  process.pfHadCalibNTupleEndPath,
))

# number of events
process.maxEvents.input = opts.maxEvents

# number of threads/streams
process.options.numberOfThreads = opts.numThreads
process.options.numberOfStreams = opts.numStreams

# input files
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MultiPion_PT0to200/GEN-SIM-DIGI-RAW-MINIAOD/NoPU_111X_mcRun4_realistic_T15_v1-v1/250000/5749D223-89ED-C448-AB1A-555597E20D98.root',
  ]

# output file
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))
