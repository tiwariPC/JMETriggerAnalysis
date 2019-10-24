import FWCore.ParameterSet.Config as cms

def hltMETSeq(proc, particleFlow, ak4PFJetsForMETTypeOne, primaryVertices, pfNoPileUpJME=None):

    proc.hltPFMET = cms.EDProducer( 'PFMETProducer',
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
        src = cms.InputTag( particleFlow )
    )
    proc.hltAK4PFFastJetCorrector = cms.EDProducer( 'L1FastjetCorrectorProducer',
        srcRho = cms.InputTag( 'fixedGridRhoFastjetAll'+'::'+proc.name_() ),
        algorithm = cms.string( 'AK4PFHLT' ),
        level = cms.string( 'L1FastJet' )
    )
    proc.hltAK4PFRelativeCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFHLT' ),
        level = cms.string( 'L2Relative' )
    )
    proc.hltAK4PFAbsoluteCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFHLT' ),
        level = cms.string( 'L3Absolute' )
    )
    proc.hltAK4PFResidualCorrector = cms.EDProducer( 'LXXXCorrectorProducer',
        algorithm = cms.string( 'AK4PFHLT' ),
        level = cms.string( 'L2L3Residual' )
    )
    proc.hltAK4PFCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
        correctors = cms.VInputTag( 'hltAK4PFFastJetCorrector','hltAK4PFRelativeCorrector','hltAK4PFAbsoluteCorrector','hltAK4PFResidualCorrector' )
    )
    proc.hltcorrPFMETTypeOne = cms.EDProducer( 'PFJetMETcorrInputProducer',
        src = cms.InputTag( ak4PFJetsForMETTypeOne ),
        type1JetPtThreshold = cms.double( 35.0 ),
        skipEMfractionThreshold = cms.double( 0.9 ),
        skipEM = cms.bool( True ),
        jetCorrLabelRes = cms.InputTag( 'hltAK4PFCorrector' ),
        offsetCorrLabel = cms.InputTag( 'hltAK4PFFastJetCorrector' ),
        skipMuons = cms.bool( True ),
        skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
        jetCorrEtaMax = cms.double( 9.9 ),
        jetCorrLabel = cms.InputTag( 'hltAK4PFCorrector' )
    )
    proc.hltPFMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
        src = cms.InputTag( 'hltPFMET' ),
        srcCorrections = cms.VInputTag( 'hltcorrPFMETTypeOne:type1' )
    )

    # Puppi candidates
    proc.pfNoLepPUPPI = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag(particleFlow),
      pdgId = cms.vint32( 1,2,22,111,130,310,2112,211,-211,321,-321,999211,2212,-2212 )
    )
    proc.pfLeptonsPUPPET = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag(particleFlow),
      pdgId = cms.vint32(-11,11,-13,13),
    )

    proc.load('CommonTools.PileupAlgos.Puppi_cff')
    proc.puppiNoLep = proc.puppi.clone(candName = 'pfNoLepPUPPI', vertexName=primaryVertices)

    proc.puppiMerged = cms.EDProducer('CandViewMerger', src = cms.VInputTag( 'puppiNoLep','pfLeptonsPUPPET'))

    proc.load('CommonTools.PileupAlgos.PhotonPuppi_cff')
    proc.hltPuppiForMET = proc.puppiPhoton.clone(

      candName = particleFlow,

      # Line below points puppi-MET to puppi-no-lepton, which increases the response
      puppiCandName = 'puppiMerged',

      # Line below replaces reference linking with delta-R matching
      # because the puppi references after merging are not consistent with those of the original PF collection
      useRefs = False,
    )

    proc.hltPuppiMET = cms.EDProducer( 'PFMETProducer',
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
        src = cms.InputTag( 'hltPuppiForMET' )
    )

    proc.hltPuppi = proc.puppi.clone(candName=particleFlow, vertexName=primaryVertices)

    proc.hltPuppiMETWithPuppiForJets = cms.EDProducer( 'PFMETProducer',
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
        src = cms.InputTag( 'hltPuppi' )
    )

    proc.hltPuppiMETSeq = cms.Sequence(
        proc.pfNoLepPUPPI
      * proc.puppiNoLep
      * proc.pfLeptonsPUPPET
      * proc.puppiMerged
      * proc.hltPuppiForMET
      * proc.hltPuppiMET
      * proc.hltPuppi
      * proc.hltPuppiMETWithPuppiForJets
    )

    proc.hltMETSeq = cms.Sequence(
        proc.hltPFMET
      * proc.hltAK4PFFastJetCorrector
      * proc.hltAK4PFRelativeCorrector
      * proc.hltAK4PFAbsoluteCorrector
      * proc.hltAK4PFResidualCorrector
      * proc.hltAK4PFCorrector
      * proc.hltcorrPFMETTypeOne
      * proc.hltPFMETTypeOne
      * proc.hltPuppiMETSeq
    )

    if pfNoPileUpJME is not None:
       proc.hltPFMETNoPileUpJME = cms.EDProducer( 'PFMETProducer',
           globalThreshold = cms.double( 0.0 ),
           calculateSignificance = cms.bool( False ),
           src = cms.InputTag( pfNoPileUpJME ),
       )
       proc.hltMETSeq *= proc.hltPFMETNoPileUpJME
