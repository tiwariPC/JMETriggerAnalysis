import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import selectedPatMuons

userPreselectedMuons = selectedPatMuons.clone(
  src = 'slimmedMuons',
  cut = '(pt > 10.) && (abs(eta) < 2.4)',
)

userMuonsWithUserData = cms.EDProducer('MuonPATUserData',

  src = cms.InputTag('userPreselectedMuons'),

  primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),

  valueMaps_float = cms.vstring(),

  userFloat_copycat = cms.PSet(),

  userInt_stringSelectors = cms.PSet(),
)

userIsolatedMuons = selectedPatMuons.clone(
  src = 'userMuonsWithUserData',
  cut = '(userInt("IDLoose") > 0) && userFloat("pfIsoR04") < 0.40',
)

userMuonsSequence = cms.Sequence(
    userPreselectedMuons
  * userMuonsWithUserData
  * userIsolatedMuons
)
