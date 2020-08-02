import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets as _ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi
from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi

def addPath_MC_AK4PFClusterJets(process):
    process.hltPreMCAK4PFClusterJets = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.HLTParticleFlowClusterSequence = cms.Sequence(
        process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence
      + process.HLTDoLocalHcalSequence
      + process.HLTPreshowerSequence
      + process.hltParticleFlowRecHitECALUnseeded
      + process.hltParticleFlowRecHitHBHE
      + process.hltParticleFlowRecHitHF
      + process.hltParticleFlowRecHitPSUnseeded
      + process.hltParticleFlowClusterECALUncorrectedUnseeded
      + process.hltParticleFlowClusterPSUnseeded
      + process.hltParticleFlowClusterECALUnseeded
      + process.hltParticleFlowClusterHBHE
      + process.hltParticleFlowClusterHCAL
      + process.hltParticleFlowClusterHF
    )

    process.hltParticleFlowClusterRefsECALUnseeded = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterECALUnseeded'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHCAL = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHCAL'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHF = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHF'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefs = cms.EDProducer('PFClusterRefCandidateMerger',
      src = cms.VInputTag(
        'hltParticleFlowClusterRefsECALUnseeded',
        'hltParticleFlowClusterRefsHCAL',
        'hltParticleFlowClusterRefsHF',
      )
    )

    process.hltAK4PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
    )

    process.HLTParticleFlowClusterRefsSequence = cms.Sequence(
        process.hltParticleFlowClusterRefsECALUnseeded
      + process.hltParticleFlowClusterRefsHCAL
      + process.hltParticleFlowClusterRefsHF
      + process.hltParticleFlowClusterRefs
    )

    process.MC_AK4PFClusterJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFClusterJets
      + process.HLTParticleFlowClusterSequence
      + process.HLTParticleFlowClusterRefsSequence
      + process.hltAK4PFClusterJets
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().extend([process.MC_AK4PFClusterJets_v1])

    return process

def addPath_MC_AK4PFPuppiJets(process):
    process.hltPreMCAK4PFPuppiJets = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPFPuppi = _puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltPixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
    )

    process.HLTPFPuppiSequence = cms.Sequence(
        process.HLTPreAK4PFJetsRecoSequence
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltPFPuppi
    )

    process.hltAK4PFPuppiJets = _ak4PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

#    process.hltAK4PFPuppiCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
#      algorithm = cms.string('AK4PFHLT'),
#      level = cms.string('L2Relative')
#    )
#
#    process.hltAK4PFPuppiCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
#      algorithm = cms.string('AK4PFHLT'),
#      level = cms.string('L3Absolute')
#    )
#
#    process.hltAK4PFPuppiCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
#      correctors = cms.VInputTag('hltAK4PFPuppiCorrectorL2', 'hltAK4PFPuppiCorrectorL3')
#    )
#
#    process.hltAK4PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
#      src = cms.InputTag('hltAK4PFPuppiJets'),
#      correctors = cms.VInputTag('hltAK4PFPuppiCorrector')
#    )

    process.HLTAK4PFPuppiJetsSequence = cms.Sequence(
        process.HLTPFPuppiSequence
      + process.hltAK4PFPuppiJets
#      + process.hltAK4PFPuppiCorrectorL2
#      + process.hltAK4PFPuppiCorrectorL3
#      + process.hltAK4PFPuppiCorrector
#      + process.hltAK4PFPuppiJetsCorrected
    )

    process.MC_AK4PFPuppiJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFPuppiJets
      + process.HLTAK4PFPuppiJetsSequence
      + process.HLTEndSequence
    )

    return process
