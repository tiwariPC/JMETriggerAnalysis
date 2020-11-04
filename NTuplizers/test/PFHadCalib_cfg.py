import FWCore.ParameterSet.Config as cms

process = cms.Process("PFHadCalib")

from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_TICL_cfg import *

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
 # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
      '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MultiPion_PT0to200/GEN-SIM-DIGI-RAW-MINIAOD/NoPU_111X_mcRun4_realistic_T15_v1-v1/250000/5749D223-89ED-C448-AB1A-555597E20D98.root',
    )
)

process.pfhadhlt = cms.EDAnalyzer('PFHadHLT',
		   genParTag        = cms.InputTag("genParticles"),
                   HLTPFCandidates  = cms.InputTag("particleFlowTmp"),
                   PFSimParticles   = cms.InputTag("particleFlowSimParticle"),

                   ptMin = cms.double(0.01),                     # Minimum pt
                   pMin = cms.double(0.01),                      # Minimum p
                   nPixMin = cms.int32(2),                     # Nb of pixel hits for pion
						 #nPixMin = cms.int32(0),          # Nb of pixel hits for neutron

                   nHitMin = cms.vint32(8, 8, 8, 8),          # Nb of track hits for pion
						 #nHitMin = cms.vint32(0,0,0,0),       # Nb of track hits for neutron

		   nEtaMin = cms.vdouble(1.4, 1.6, 2.0, 2.5),  # in these eta ranges
                   hcalMin = cms.double(0.0),                   # Minimum hcal energy
                   ecalMax = cms.double(1e12),                  # Maximum ecal energy 
                   rootOutputFile = cms.string('PFHadCalibration.root')
)

process.printGenParticleList = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(10),
  printVertex = cms.untracked.bool(False),
  printOnlyHardInteraction = cms.untracked.bool(False), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
  src = cms.InputTag("genParticles")
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
        zMax = cms.double(317.0)
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

process.HLTJMESequence += process.particleFlowSimParticle

process.AOutput = cms.EndPath( process.pfhadhlt )
process.setSchedule_(cms.Schedule(process.MC_JME, process.AOutput))

process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)

