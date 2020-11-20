from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg import cms, process

process.maxEvents.input = 50

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.source.fileNames = [
  '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MultiPion_PT0to200/GEN-SIM-DIGI-RAW-MINIAOD/NoPU_111X_mcRun4_realistic_T15_v1-v1/250000/5749D223-89ED-C448-AB1A-555597E20D98.root',
]

process.pfHadCalibNTuple = cms.EDAnalyzer('PFHadCalibNTuple',
  genParTag = cms.InputTag("genParticles"),
  HLTPFCandidates = cms.InputTag("pfTICL"),
  PFSimParticles = cms.InputTag("particleFlowSimParticle"),

  ptMin = cms.double(0.01), # Minimum pt
  pMin = cms.double(0.01),  # Minimum p
  nPixMin = cms.int32(2), # Nb of pixel hits for pion
  nHitMin = cms.vint32(8, 8, 8, 8),          # Nb of track hits for pion
  nEtaMin = cms.vdouble(1.4, 1.6, 2.0, 2.5), #  in these eta ranges

  hcalMin = cms.double(0.0),  # Minimum hcal energy
  ecalMax = cms.double(1e12), # Maximum ecal energy 
  rootOutputFile = cms.string('PFHadCalibration.root')
)

process.particleFlowSimParticle = cms.EDProducer("PFSimParticleProducer",
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
  RecTracks = cms.InputTag("trackerDrivenElectronSeeds"),
  TTRHBuilder = cms.string('WithTrackAngle'),
  ecalRecHitsEB = cms.InputTag("caloRecHits","EcalRecHitsEB"),
  ecalRecHitsEE = cms.InputTag("caloRecHits","EcalRecHitsEE"),
  fastSimProducer = cms.untracked.InputTag("fastSimProducer","EcalHitsEB"),
  process_Particles = cms.untracked.bool(True),
  process_RecTracks = cms.untracked.bool(False),
  sim = cms.InputTag("g4SimHits"),
  verbose = cms.untracked.bool(False)
)

process.pfSimParticleSeq = cms.Sequence(process.particleFlowSimParticle)
process.pfSimParticlePath = cms.Path(process.pfSimParticleSeq)

process.pfHadCalibNTupleEndPath = cms.EndPath(process.pfHadCalibNTuple)
process.setSchedule_(cms.Schedule(process.MC_JME, process.pfSimParticlePath, process.pfHadCalibNTupleEndPath))
