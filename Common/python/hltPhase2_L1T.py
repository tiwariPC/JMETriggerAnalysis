import FWCore.ParameterSet.Config as cms

from L1Trigger.L1CaloTrigger.Phase1L1TJets_cff import *

def customise_hltPhase2_L1T(process):

    process.l1tSlwPFPuppiJets = Phase1L1TJetProducer.clone(
      inputCollectionTag = 'l1pfCandidates:Puppi',
      outputCollectionName = 'UncalibratedPhase1L1TJetFromPfCandidates',
    )

    process.l1tSlwPFPuppiJetsCorrected = Phase1L1TJetCalibrator.clone(
      inputCollectionTag = 'l1tSlwPFPuppiJets:UncalibratedPhase1L1TJetFromPfCandidates',
      outputCollectionName = 'Phase1L1TJetFromPfCandidates',
    )

    process.l1tReconstructionSeq = cms.Sequence(
        process.l1tSlwPFPuppiJets
      + process.l1tSlwPFPuppiJetsCorrected
    )

    process.l1tReconstructionPath = cms.Path(process.l1tReconstructionSeq)

    if process.schedule_() is not None:
       process.schedule_().extend([process.l1tReconstructionPath])

    return process
