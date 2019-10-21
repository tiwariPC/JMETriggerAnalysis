import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets

userAK4PFCHSJetsPt10 = selectedPatJets.clone(
  src = 'slimmedJets',
  cut = 'pt > 10',
)

userJetsSequence = cms.Sequence(
  userAK4PFCHSJetsPt10
)
