import FWCore.ParameterSet.Config as cms

process = cms.Process("PFHadCalib")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

#process.load("PFHadHLT.hlt83X_JME_PFHadCal")

#from PFHCalib.PFHadHLT.dump_hlt_SinglePion import *
#from PFHCalib.PFHadHLT.step3_TrackingV2_11_0_0 import *
from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv06_cfg import *
#from JMETriggerAnalysis.NTuplizers.tmp import *
#from PFHCalib.PFHadHLT.hltPhase2_TRKv02_cfg import *

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))

process.source = cms.Source("PoolSource",
 # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/Phase2HLTTDRWinter20DIGI/MultiPion_PT0to200/GEN-SIM-DIGI-RAW/NoPU_110X_mcRun4_realistic_v3-v2/250000/71269CFE-FE69-2445-A303-8920BEEA1B72.root'
    )
)

process.pfhadhlt = cms.EDAnalyzer('PFHadHLT',
    #src = cms.InputTag("prunedGenParticles"),
    #maxEventsToPrint = cms.untracked.int32(1)
		   #genEvnTag = cms.InputTag("generator"),
		   genParTag        = cms.InputTag("genParticles"),
                   #HLTPFCandidates  = cms.InputTag("particleFlowTmpBarrel"),
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


#process.reconstruction += process.simPFProducer
process.reconstruction += process.particleFlowSimParticle

#process.p = cms.Path(process.pfhadhlt)

#process.AOutput = cms.EndPath( process.hltPreAOutput + process.pfhadhlt + process.printGenParticleList)
#process.AOutput = cms.EndPath( process.hltPreAOutput + process.pfhadhlt)
#process.AOutput = cms.EndPath( process.printGenParticleList)
process.AOutput = cms.EndPath( process.pfhadhlt )
process.schedule.extend([process.AOutput])
