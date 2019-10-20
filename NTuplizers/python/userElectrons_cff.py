import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi import selectedPatElectrons

userPreselectedElectrons = selectedPatElectrons.clone(
  src = 'slimmedElectrons',
  cut = '(pt > 10.) && (abs(superCluster.eta) < 2.5) && !((1.4442 < abs(superCluster.eta)) && (abs(superCluster.eta) < 1.5660))',
)

_elecID_dxydzCuts  =     '((abs(superCluster.eta) < 1.4442) && (abs(userFloat("dxyPV")) < 0.05) && (abs(userFloat("dzPV")) < 0.10))'
_elecID_dxydzCuts += ' || ((abs(superCluster.eta) > 1.5660) && (abs(userFloat("dxyPV")) < 0.10) && (abs(userFloat("dzPV")) < 0.20))'

userElectronsWithUserData = cms.EDProducer('ElectronPATUserData',

  src = cms.InputTag('userPreselectedElectrons'),

  primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),

  effAreas_file = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt'),

  rho = cms.InputTag('fixedGridRhoFastjetAll'),

  userFloat_copycat = cms.PSet(

    mva_Iso   = cms.string('ElectronMVAEstimatorRun2Fall17'+  'IsoV1Values'),
    mva_NoIso = cms.string('ElectronMVAEstimatorRun2Fall17'+'NoIsoV1Values'),
  ),

  userInt_stringSelectors = cms.PSet(

    IDCutBasedVeto   = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V1-veto") > 0.5)'),
    IDCutBasedLoose  = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V1-loose") > 0.5)'),
    IDCutBasedMedium = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V1-medium") > 0.5)'),
    IDCutBasedTight  = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V1-tight") > 0.5)'),

    IDMVAIsoWP80 = cms.string('(electronID("mvaEleID-Fall17-iso-V1-wp80") > 0.5)'),
    IDMVAIsoWP90 = cms.string('(electronID("mvaEleID-Fall17-iso-V1-wp90") > 0.5)'),
  ),
)

userIsolatedElectrons = selectedPatElectrons.clone(
  src = 'userElectronsWithUserData',
  cut = 'userInt("IDCutBasedLoose") > 0',
)

userElectronsSequence = cms.Sequence(
    userPreselectedElectrons
  * userElectronsWithUserData
  * userIsolatedElectrons
)
