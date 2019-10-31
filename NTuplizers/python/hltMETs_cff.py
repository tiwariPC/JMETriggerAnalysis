import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import *
from CommonTools.PileupAlgos.PhotonPuppi_cff import puppiPhoton
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi

def hltMETsSeq(proc, particleFlow, primaryVertices):

    ### Puppi MET

    # Puppi candidates for MET
    proc.pfNoLepPUPPI = cms.EDFilter('PdgIdCandViewSelector',
        src = cms.InputTag( particleFlow ),
        pdgId = cms.vint32( 1, 2, 22, 111, 130, 310, 2112, 211, -211, 321, -321, 999211, 2212, -2212 )
    )
    proc.pfLeptonsPUPPET = cms.EDFilter('PdgIdCandViewSelector',
        src = cms.InputTag( particleFlow ),
        pdgId = cms.vint32( -11, 11, -13, 13 ),
    )
    proc.puppiNoLep = puppi.clone(
        candName = 'pfNoLepPUPPI',
        vertexName = primaryVertices,
    )
    proc.puppiMerged = cms.EDProducer('CandViewMerger',
        src = cms.VInputTag('puppiNoLep', 'pfLeptonsPUPPET'),
    )
    proc.hltPuppiForMET = puppiPhoton.clone(
        candName = particleFlow,
        # Line below points puppi-MET to puppi-no-lepton, which increases the response
        puppiCandName = 'puppiMerged',
        # Line below replaces reference linking with delta-R matching
        # because the puppi references after merging are not consistent with those of the original PF collection
        useRefs = False,
    )
    proc.hltPuppiMET = cms.EDProducer( 'PFMETProducer',
        src = cms.InputTag( 'hltPuppiForMET' ),
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
    )
    proc.hltPuppiMETsRawSeq = cms.Sequence(
       (proc.pfNoLepPUPPI
      * proc.puppiNoLep
      + proc.pfLeptonsPUPPET)
      * proc.puppiMerged
      * proc.hltPuppiForMET
      * proc.hltPuppiMET
    )

    ### Puppi MET Type-1

    # Puppi candidates for Jets
    proc.hltPuppi = puppi.clone(
        candName = particleFlow,
        vertexName = primaryVertices,
    )
    proc.ak4PuppiJetsForPuppiMETTypeOne = ak4PFJetsPuppi.clone(
        src = 'hltPuppi',
    )
    proc.hltAK4PuppiFastJetCorrector = cms.EDProducer( 'L1FastjetCorrectorProducer',
        srcRho = cms.InputTag( 'fixedGridRhoFastjetAll'+'::'+proc.name_() ),
        algorithm = cms.string( 'AK4PFPuppi' ),
        level = cms.string( 'L1FastJet' )
    )
    proc.hltAK4PuppiRelativeCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFPuppi' ),
        level = cms.string( 'L2Relative' )
    )
    proc.hltAK4PuppiAbsoluteCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFPuppi' ),
        level = cms.string( 'L3Absolute' )
    )
    proc.hltAK4PuppiResidualCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFPuppi' ),
        level = cms.string( 'L2L3Residual' )
    )
    proc.hltAK4PuppiCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
        correctors = cms.VInputTag( 'hltAK4PuppiFastJetCorrector','hltAK4PuppiRelativeCorrector','hltAK4PuppiAbsoluteCorrector','hltAK4PuppiResidualCorrector' )
    )
    proc.hltcorrPuppiMETTypeOne = cms.EDProducer( 'PFJetMETcorrInputProducer',
        src = cms.InputTag( 'ak4PuppiJetsForPuppiMETTypeOne' ),
        type1JetPtThreshold = cms.double( 35.0 ),
        skipEMfractionThreshold = cms.double( 0.9 ),
        skipEM = cms.bool( True ),
        jetCorrLabelRes = cms.InputTag( 'hltAK4PuppiCorrector' ),
        offsetCorrLabel = cms.InputTag( 'hltAK4PuppiFastJetCorrector' ),
        skipMuons = cms.bool( True ),
        skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
        jetCorrEtaMax = cms.double( 9.9 ),
        jetCorrLabel = cms.InputTag( 'hltAK4PuppiCorrector' )
    )
    proc.hltPuppiMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
        src = cms.InputTag( 'hltPuppiMET' ),
        srcCorrections = cms.VInputTag( 'hltcorrPuppiMETTypeOne:type1' )
    )
    proc.hltPuppiMETsTypeOneSeq = cms.Sequence(
        proc.hltPuppi
      * proc.ak4PuppiJetsForPuppiMETTypeOne
      * proc.hltAK4PuppiFastJetCorrector
      * proc.hltAK4PuppiRelativeCorrector
      * proc.hltAK4PuppiAbsoluteCorrector
      * proc.hltAK4PuppiResidualCorrector
      * proc.hltAK4PuppiCorrector
      * proc.hltcorrPuppiMETTypeOne
      * proc.hltPuppiMETTypeOne
    )

    # [testing] Puppi MET with Puppi-For-Jets inputs
    proc.hltPuppiMETWithPuppiForJets = cms.EDProducer( 'PFMETProducer',
        src = cms.InputTag( 'hltPuppi' ),
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
    )
    proc.hltPuppiMETsRawSeq += cms.Sequence(
        proc.hltPuppi
      * proc.hltPuppiMETWithPuppiForJets
    )

    ### SoftKiller MET

    proc.hltSoftKiller = cms.EDProducer('SoftKillerProducer',
        PFCandidates = cms.InputTag(particleFlow),
        Rho_EtaMax = cms.double( 5.0 ),
        rParam = cms.double( 0.4 )
    )
    proc.hltSoftKillerMET = cms.EDProducer( 'PFMETProducer',
        src = cms.InputTag( 'hltSoftKiller' ),
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
    )
    proc.hltSoftKillerMETsSeq = cms.Sequence(
        proc.hltSoftKiller
      * proc.hltSoftKillerMET
    )

    ### METs Sequence

    proc.hltMETsSeq = cms.Sequence(
        proc.hltPuppiMETsRawSeq
#      * proc.hltPuppiMETsTypeOneSeq --> HLT JECs for PuppiJets not available
      + proc.hltSoftKillerMETsSeq
    )
