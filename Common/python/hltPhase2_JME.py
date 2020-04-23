import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import *
from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets, ak4PFJetsCHS, ak4PFJetsPuppi
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJets, ak8PFJetsCHS, ak8PFJetsPuppi
from RecoMET.METProducers.PFClusterMET_cfi import pfClusterMet

from CondCore.CondDB.CondDB_cfi import CondDB

from RecoHGCal.TICL.iterativeTICL_cff import injectTICLintoPF

def customize_hltPhase2_JME(process, name='HLTJMESequence'):

    ### Guidelines to browse the code below:
    ###  - jet (MET) collections are indicated by comments starting with "## Jets: " ("## MET:")
    ###  - sequences are indicated by comments starting with "## Sequence: "
    ###  - HLT-related collections (sequences) start with "hlt" ("HLT")
    ###  - modifications that are temporary and/or likely to change in a more realistic HLT menu are indicated by "#!!"
    ###    (at the moment, these might simply indicate differences between the current configuration and the one used in the 2018 HLT-Menu)

    #### check if process member with target output name already exists
    if hasattr(process, name):
       raise RuntimeError('process already has member named "'+name+'"')

    #### check if reconstruction sequence exists
    if not hasattr(process, 'reconstruction'):
       raise RuntimeError('reconstruction sequence process.reconstruction not found')

    _particleFlowCands = 'particleFlowTmp'
    if not hasattr(process, _particleFlowCands):
       raise RuntimeError('process has no member named "'+_particleFlowCands+'"')

    _primaryVertices = 'offlinePrimaryVertices'
    if not hasattr(process, _primaryVertices):
       raise RuntimeError('process has no member named "'+_primaryVertices+'"')

    _primaryVerticesGood = 'goodOfflinePrimaryVertices'

    process.particleFlowTmpBarrel.useEGammaFilters = False
    process.particleFlowTmpBarrel.useEGammaElectrons = False
    process.particleFlowTmpBarrel.usePFConversions = False
    process.particleFlowTmpBarrel.usePFDecays = False
    process.particleFlowTmpBarrel.usePFNuclearInteractions = False
    process.particleFlowTmpBarrel.useProtectionsForJetMET = False
    process.pfTrack.GsfTracksInEvents = False

    # redefining the PFBlockProducer removing displaced tracks
    process.particleFlowBlock = cms.EDProducer("PFBlockProducer",
        debug = cms.untracked.bool(False),
        elementImporters = cms.VPSet(
#            cms.PSet(
#                gsfsAreSecondary = cms.bool(False),
#                importerName = cms.string('GSFTrackImporter'),
#                source = cms.InputTag("pfTrackElec"),
#                superClustersArePF = cms.bool(True)
#            ), 
#            cms.PSet(
#                importerName = cms.string('ConvBremTrackImporter'),
#                source = cms.InputTag("pfTrackElec")
#            ), 
            cms.PSet(
                importerName = cms.string('SuperClusterImporter'),
                maximumHoverE = cms.double(0.5),
                minPTforBypass = cms.double(100.0),
                minSuperClusterPt = cms.double(10.0),
                source_eb = cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALBarrel"),
                source_ee = cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALEndcapWithPreshower"),
                source_towers = cms.InputTag("towerMaker"),
                superClustersArePF = cms.bool(True)
            ), 
#            cms.PSet(	
#                importerName = cms.string('ConversionTrackImporter'),
#                source = cms.InputTag("pfConversions")
#            ), 
#            cms.PSet(
#                importerName = cms.string('NuclearInteractionTrackImporter'),
#                source = cms.InputTag("pfDisplacedTrackerVertex")
#            ), 
            cms.PSet(
                DPtOverPtCuts_byTrackAlgo = cms.vdouble(
                    10.0, 10.0, 10.0, 10.0, 10.0, 
                    5.0
                ),
                NHitCuts_byTrackAlgo = cms.vuint32(
                    3, 3, 3, 3, 3, 
                    3
                ),
                cleanBadConvertedBrems = cms.bool(True),
                importerName = cms.string('GeneralTracksImporterWithVeto'),
                maxDPtOPt = cms.double(1.0),
                muonSrc = cms.InputTag("muons1stStep"),
                source = cms.InputTag("pfTrack"),
                useIterativeTracking = cms.bool(True),
                veto = cms.InputTag("hgcalTrackCollection","TracksInHGCal")
            ), 
            cms.PSet(
                BCtoPFCMap = cms.InputTag("particleFlowSuperClusterECAL","PFClusterAssociationEBEE"),
                importerName = cms.string('ECALClusterImporter'),
                source = cms.InputTag("particleFlowClusterECAL")
            ), 
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHCAL")
            ), 
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowBadHcalPseudoCluster")
            ), 
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHO")
            ), 
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHF")
            ), 
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterPS")
            ), 
            cms.PSet(
                importerName = cms.string('TrackTimingImporter'),
                timeErrorMap = cms.InputTag("tofPID","sigmat0"),
                timeErrorMapGsf = cms.InputTag("tofPID","sigmat0"),
                timeValueMap = cms.InputTag("tofPID","t0"),
                timeValueMapGsf = cms.InputTag("tofPID","t0")
            )
        ),
        linkDefinitions = cms.VPSet(
            cms.PSet(
                linkType = cms.string('PS1:ECAL'),
                linkerName = cms.string('PreshowerAndECALLinker'),
                useKDTree = cms.bool(True)
            ), 
            cms.PSet(
                linkType = cms.string('PS2:ECAL'),
                linkerName = cms.string('PreshowerAndECALLinker'),
                useKDTree = cms.bool(True)
            ), 
            cms.PSet(
                linkType = cms.string('TRACK:ECAL'),
                linkerName = cms.string('TrackAndECALLinker'),
                useKDTree = cms.bool(True)
            ), 
            cms.PSet(
                linkType = cms.string('TRACK:HCAL'),
                linkerName = cms.string('TrackAndHCALLinker'),
                useKDTree = cms.bool(True),
                trajectoryLayerEntrance = cms.string('HCALEntrance'),
                trajectoryLayerExit = cms.string('HCALExit')
            ), 
            cms.PSet(
                linkType = cms.string('TRACK:HO'),
                linkerName = cms.string('TrackAndHOLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('ECAL:HCAL'),
                linkerName = cms.string('ECALAndHCALLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('HCAL:HO'),
                linkerName = cms.string('HCALAndHOLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('HFEM:HFHAD'),
                linkerName = cms.string('HFEMAndHFHADLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('TRACK:TRACK'),
                linkerName = cms.string('TrackAndTrackLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('ECAL:ECAL'),
                linkerName = cms.string('ECALAndECALLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('GSF:ECAL'),
                linkerName = cms.string('GSFAndECALLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('TRACK:GSF'),
                linkerName = cms.string('TrackAndGSFLinker'),
                useConvertedBrems = cms.bool(True),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('GSF:BREM'),
                linkerName = cms.string('GSFAndBREMLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('GSF:GSF'),
                linkerName = cms.string('GSFAndGSFLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('ECAL:BREM'),
                linkerName = cms.string('ECALAndBREMLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('GSF:HCAL'),
                linkerName = cms.string('GSFAndHCALLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('HCAL:BREM'),
                linkerName = cms.string('HCALAndBREMLinker'),
                useKDTree = cms.bool(False)
            ), 
            cms.PSet(
                linkType = cms.string('SC:ECAL'),
                linkerName = cms.string('SCAndECALLinker'),
                useKDTree = cms.bool(False),
                SuperClusterMatchByRef = cms.bool(True)
            ),
            cms.PSet(
              linkType   = cms.string("TRACK:HFEM"),
              linkerName = cms.string("TrackAndHCALLinker"),
              useKDTree  = cms.bool(True),
              trajectoryLayerEntrance = cms.string("VFcalEntrance"),
              trajectoryLayerExit = cms.string("")
            ),
            cms.PSet(
              linkType   = cms.string("TRACK:HFHAD"),
              linkerName = cms.string("TrackAndHCALLinker"),
              useKDTree  = cms.bool(True),
              trajectoryLayerEntrance = cms.string("VFcalEntrance"),
              trajectoryLayerExit = cms.string("")
            ),
        ),
        verbose = cms.untracked.bool(False)
    )

    ## Jets: AK4 Calo
    process.hltAK4CaloJets = process.ak4CaloJets.clone(
      src = 'towerMaker', #!! hltTowerMakerForAll
      useDeterministicSeed = True,
      doAreaDiskApprox = True,
      doAreaFastjet = False,
      doPUOffsetCorr = False,
      doRhoFastjet = False,
      srcPVs = 'NotUsed',
      doPVCorrection = False,
    )

    ## Jets: AK8 Calo
    process.hltAK8CaloJets = process.hltAK4CaloJets.clone(rParam = 0.8)

### --------------------------------------------------------------------------
### Comment: JESCs to Calo Jets currently disabled (not available for Phase-2)
### --------------------------------------------------------------------------
#    ## Jets: AK4 Calo Corrected
#    process.hltFixedGridRhoFastjetAllCalo = cms.EDProducer("FixedGridRhoProducerFastjet",
#        gridSpacing = cms.double(0.55),
#        maxRapidity = cms.double(5.0),
#        pfCandidatesTag = cms.InputTag("towerMaker") #!! hltTowerMakerForAll
#    )
#    process.hltAK4CaloJetCorrectorL1 = cms.EDProducer( "L1FastjetCorrectorProducer",
#        srcRho = cms.InputTag( "hltFixedGridRhoFastjetAllCalo" ),
#        algorithm = cms.string( "AK4Calo" ), #!! AK4CaloHLT
#        level = cms.string( "L1FastJet" )
#    )
#    process.hltAK4CaloJetCorrectorL2 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK4Calo" ), #!! AK4CaloHLT
#        level = cms.string( "L2Relative" )
#    )
#    process.hltAK4CaloJetCorrectorL3 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK4Calo" ), #!! AK4CaloHLT
#        level = cms.string( "L3Absolute" )
#    )
#    process.hltAK4CaloJetCorrectorL2L3 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK4Calo" ), #!! AK4CaloHLT
#        level = cms.string( "L2L3Residual" )
#    )
#    process.hltAK4CaloJetCorrector = cms.EDProducer( "ChainedJetCorrectorProducer",
#        correctors = cms.VInputTag( 'hltAK4CaloJetCorrectorL1','hltAK4CaloJetCorrectorL2','hltAK4CaloJetCorrectorL3','hltAK4CaloJetCorrectorL2L3' )
#    )
#    process.hltAK4CaloJetsCorrected = cms.EDProducer( "CorrectedCaloJetProducer",
#        src = cms.InputTag( "hltAK4CaloJets" ),
#        correctors = cms.VInputTag( 'hltAK4CaloJetCorrector' ),
#    )
#    
#    ## Jets: AK8 Calo Corrected
#    process.hltAK8CaloJetCorrectorL1 = cms.EDProducer( "L1FastjetCorrectorProducer",
#        srcRho = cms.InputTag( "hltFixedGridRhoFastjetAllCalo" ),
#        algorithm = cms.string( "AK8Calo" ), #!! AK8CaloHLT
#        level = cms.string( "L1FastJet" )
#    )
#    process.hltAK8CaloCorrectorL2 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK8Calo" ), #!! AK8CaloHLT
#        level = cms.string( "L2Relative" )
#    )
#    process.hltAK8CaloJetCorrectorL3 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK8Calo" ), #!! AK8CaloHLT
#        level = cms.string( "L3Absolute" )
#    )
#    process.hltAK8CaloJetCorrectorL2L3 = cms.EDProducer( "LXXXCorrectorProducer",
#        algorithm = cms.string( "AK8Calo" ), #!! AK8CaloHLT
#        level = cms.string( "L2L3Residual" )
#    )
#    process.hltAK8CaloCorrector = cms.EDProducer( "ChainedJetCorrectorProducer",
#        correctors = cms.VInputTag( 'hltAK8CaloJetCorrectorL1','hltAK8CaloCorrectorL2','hltAK8CaloJetCorrectorL3','hltAK8CaloJetCorrectorL2L3' )
#    )
#    process.hltAK8CaloJetsCorrected = cms.EDProducer( "CorrectedCaloJetProducer",
#        src = cms.InputTag( "hltAK8CaloJets" ),
#        correctors = cms.VInputTag( 'hltAK8CaloCorrector' ),
#    )
### --------------------------------------------------------------------------

    ## Sequence: Calo Jets
    process.HLTCaloJetsReconstruction = cms.Sequence(
      process.hltAK4CaloJets
    + process.hltAK8CaloJets
#    + process.hltFixedGridRhoFastjetAllCalo
#    *(process.hltAK4CaloJetCorrectorL1
#    * process.hltAK4CaloJetCorrectorL2
#    * process.hltAK4CaloJetCorrectorL3
#    * process.hltAK4CaloJetCorrectorL2L3
#    * process.hltAK4CaloJetCorrector
#    * process.hltAK4CaloJetsCorrected
#    + process.hltAK4CaloJetCorrectorL1
#    * process.hltAK4CaloJetCorrectorL2
#    * process.hltAK4CaloJetCorrectorL3
#    * process.hltAK4CaloJetCorrectorL2L3
#    * process.hltAK4CaloJetCorrector
#    * process.hltAK4CaloJetsCorrected)
    )

    ## MET: Calo
    process.hltCaloMET = cms.EDProducer("CaloMETProducer",
      alias = cms.string('RawCaloMET'),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.3),
      noHF = cms.bool(False),
      src = cms.InputTag("towerMaker") #!! hltTowerMakerForAll
    )

    ## Sequence: Calo MET
    process.HLTCaloMETReconstruction = cms.Sequence(
      process.hltCaloMET
    )

    ## Jets: AK4 PFClusters
    process.load('RecoJets.JetProducers.PFClustersForJets_cff')

    # add PFClusters from HGCal
    process.pfClusterRefsForJetsHGCAL = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('particleFlowClusterHGCal'),
      particleType = cms.string('pi+'),
    )
    process.pfClusterRefsForJets_stepTask.add(process.pfClusterRefsForJetsHGCAL)
    process.pfClusterRefsForJets.src += ['pfClusterRefsForJetsHGCAL']

    process.hltAK4PFClusterJets = ak4PFClusterJets.clone(
      doPVCorrection = False,
      srcPVs = 'NotUsed',
    )

    ## Jets: AK8 PFClusters
    process.hltAK8PFClusterJets = process.hltAK4PFClusterJets.clone(rParam = 0.8)

    ## MET: PFClusters
    process.hltPFClusterMET = cms.EDProducer("PFClusterMETProducer",
      src = cms.InputTag('pfClusterRefsForJets'),
      alias = cms.string('pfClusterMet'),
      globalThreshold = cms.double(0.0)
    )

    ## Sequence: PFClusterJets and PFClusterMET
    process.HLTPFClusterJMEReconstruction = cms.Sequence(
        process.pfClusterRefsForJets_step
      *(process.hltAK4PFClusterJets
      + process.hltAK8PFClusterJets
      + process.hltPFClusterMET)
    )

    ## Jets: AK4 PF
    process.hltAK4PFJets = ak4PFJets.clone(
      src = _particleFlowCands,
#      jetPtMin = 10.,
    )
    process.hltAK4PFJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PFJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PFJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PFJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK4PFJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK4PFJetCorrectorL1', 'hltAK4PFJetCorrectorL2', 'hltAK4PFJetCorrectorL3', 'hltAK4PFJetCorrectorL2L3' )
    )
    process.hltAK4PFJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PFJets' ),
      correctors = cms.VInputTag( 'hltAK4PFJetCorrector' ),
    )

    ## Sequence: AK4 PF Jets
    process.HLTAK4PFJetsReconstruction = cms.Sequence(
        process.hltAK4PFJets
      * process.hltAK4PFJetCorrectorL1
      * process.hltAK4PFJetCorrectorL2
      * process.hltAK4PFJetCorrectorL3
      * process.hltAK4PFJetCorrectorL2L3
      * process.hltAK4PFJetCorrector
      * process.hltAK4PFJetsCorrected
    )

    ## Jets: AK8 PF
    process.hltAK8PFJets = ak8PFJets.clone(
      src = _particleFlowCands,
#      jetPtMin = 80.,
    )
    process.hltAK8PFJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK8PFJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PFJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PFJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK8PFJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK8PFJetCorrectorL1', 'hltAK8PFJetCorrectorL2', 'hltAK8PFJetCorrectorL3', 'hltAK8PFJetCorrectorL2L3' )
    )
    process.hltAK8PFJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK8PFJets' ),
      correctors = cms.VInputTag( 'hltAK8PFJetCorrector' ),
    )

    ## Sequence: AK8 PF Jets
    process.HLTAK8PFJetsReconstruction = cms.Sequence(
        process.hltAK8PFJets
      * process.hltAK8PFJetCorrectorL1
      * process.hltAK8PFJetCorrectorL2
      * process.hltAK8PFJetCorrectorL3
      * process.hltAK8PFJetCorrectorL2L3
      * process.hltAK8PFJetCorrector
      * process.hltAK8PFJetsCorrected
    )

    ## Jets: AK4 PF+CHS
    process.hltAK4PFCHSJets = ak4PFJetsCHS.clone(
#      jetPtMin = 10.,
    )

    process.hltAK4PFCHSJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PFCHSJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PFCHSJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PFCHSJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK4PFCHSJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK4PFCHSJetCorrectorL1', 'hltAK4PFCHSJetCorrectorL2', 'hltAK4PFCHSJetCorrectorL3', 'hltAK4PFCHSJetCorrectorL2L3' )
    )
    process.hltAK4PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PFCHSJets' ),
      correctors = cms.VInputTag( 'hltAK4PFCHSJetCorrector' ),
    )

    ## Jets: AK8 PF+CHS
    process.hltAK8PFCHSJets = ak8PFJetsCHS.clone(
#      jetPtMin = 80.,
    )

    process.hltAK8PFCHSJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK8PFCHSJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PFCHSJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PFCHSJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK8PFCHSJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK8PFCHSJetCorrectorL1', 'hltAK8PFCHSJetCorrectorL2', 'hltAK8PFCHSJetCorrectorL3', 'hltAK8PFCHSJetCorrectorL2L3' )
    )
    process.hltAK8PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK8PFCHSJets' ),
      correctors = cms.VInputTag( 'hltAK8PFCHSJetCorrector' ),
    )

    ## Sequence: PF+CHS Jets, AK4 and AK8
    process.particleFlowPtrs.src = _particleFlowCands

    process.goodOfflinePrimaryVertices.src = _primaryVertices

    process.HLTPFJetsCHSReconstruction = cms.Sequence(
        process.particleFlowPtrs
      + process.goodOfflinePrimaryVertices
      + process.pfPileUpJME
      + process.pfNoPileUpJME
      + process.hltAK4PFCHSJets
      + process.hltAK4PFCHSJetCorrectorL1
      + process.hltAK4PFCHSJetCorrectorL2
      + process.hltAK4PFCHSJetCorrectorL3
      + process.hltAK4PFCHSJetCorrectorL2L3
      + process.hltAK4PFCHSJetCorrector
      + process.hltAK4PFCHSJetsCorrected
      + process.hltAK8PFCHSJets
      + process.hltAK8PFCHSJetCorrectorL1
      + process.hltAK8PFCHSJetCorrectorL2
      + process.hltAK8PFCHSJetCorrectorL3
      + process.hltAK8PFCHSJetCorrectorL2L3
      + process.hltAK8PFCHSJetCorrector
      + process.hltAK8PFCHSJetsCorrected
    )

    ## MET: PF Raw
    process.hltPFMET = cms.EDProducer( 'PFMETProducer',
        src = cms.InputTag( _particleFlowCands ),
        globalThreshold = cms.double( 0.0 ),
        calculateSignificance = cms.bool( False ),
    )

    ## MET: PF Type-1
    _jescLabelForPFMETTypeOne = 'AK4PFchs'
    _jetsForPFMETTypeOne = 'hltAK4PFCHSJets'

    process.hltPFMETJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltPFMETJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L2Relative' )
    )
    process.hltPFMETJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltPFMETJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltPFMETJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltPFMETJetCorrectorL1','hltPFMETJetCorrectorL2','hltPFMETJetCorrectorL3','hltPFMETJetCorrectorL2L3' )
    )
    process.hltPFMETTypeOneCorrector = cms.EDProducer( 'PFJetMETcorrInputProducer',
      src = cms.InputTag( _jetsForPFMETTypeOne ),
      type1JetPtThreshold = cms.double( 15.0 ),
      skipEMfractionThreshold = cms.double( 0.9 ),
      skipEM = cms.bool( True ),
      jetCorrLabelRes = cms.InputTag( 'hltPFMETJetCorrector' ),
      offsetCorrLabel = cms.InputTag( 'hltPFMETJetCorrectorL1' ),
      skipMuons = cms.bool( True ),
      skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
      jetCorrEtaMax = cms.double( 9.9 ),
      jetCorrLabel = cms.InputTag( 'hltPFMETJetCorrector' ),
    )
    process.hltPFMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
      src = cms.InputTag( 'hltPFMET' ),
      srcCorrections = cms.VInputTag( 'hltPFMETTypeOneCorrector:type1' )
    )

    ## Sequence: MET PF, Raw and Type-1
    process.HLTPFMETReconstruction = cms.Sequence(
        process.hltPFMET
      +(process.hltPFMETJetCorrectorL1
      * process.hltPFMETJetCorrectorL2
      * process.hltPFMETJetCorrectorL3
      * process.hltPFMETJetCorrectorL2L3
      * process.hltPFMETJetCorrector
      * process.hltPFMETTypeOneCorrector
      * process.hltPFMETTypeOne)
    )

    ## MET: CHS
    process.hltParticleFlowCHS = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
      src = process.hltAK4PFCHSJets.src,
    )
    process.hltPFCHSMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( 'hltParticleFlowCHS' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    ## Sequence: MET CHS
    process.HLTPFCHSMETReconstruction = cms.Sequence(
        process.hltParticleFlowCHS
      * process.hltPFCHSMET
    )

    ## MET: SoftKiller
    process.hltParticleFlowSoftKiller = cms.EDProducer('SoftKillerProducer',
      PFCandidates = cms.InputTag( _particleFlowCands ),
      Rho_EtaMax = cms.double( 5.0 ),
      rParam = cms.double( 0.4 )
    )
    process.hltPFSoftKillerMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( 'hltParticleFlowSoftKiller' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False )
    )

    ## Sequence: MET SoftKiller
    process.HLTPFSoftKillerMETReconstruction = cms.Sequence(
        process.hltParticleFlowSoftKiller
      * process.hltPFSoftKillerMET
    )

    ## Jets: Puppi AK4
    process.hltPuppi = puppi.clone(
      candName = _particleFlowCands,
      vertexName = _primaryVerticesGood,
    )
    process.hltAK4PuppiJets = ak4PFJetsPuppi.clone(
      src = _particleFlowCands,
      applyWeight = True,
      srcWeights = 'hltPuppi',
#      jetPtMin = 10.,
    )
    process.hltAK4PuppiJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PFPuppi' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PuppiJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFPuppi' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PuppiJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFPuppi' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PuppiJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFPuppi' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK4PuppiJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK4PuppiJetCorrectorL1', 'hltAK4PuppiJetCorrectorL2', 'hltAK4PuppiJetCorrectorL3', 'hltAK4PuppiJetCorrectorL2L3' )
    )
    process.hltAK4PuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PuppiJets' ),
      correctors = cms.VInputTag( 'hltAK4PuppiJetCorrector' ),
    )

    ## Jets: Puppi AK8
    process.hltAK8PuppiJets = ak8PFJetsPuppi.clone(
      src = _particleFlowCands,
      applyWeight = True,
      srcWeights = 'hltPuppi',
#      jetPtMin = 80.,
    )
    process.hltAK8PuppiJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFPuppi' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PuppiJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFPuppi' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PuppiJetCorrectorL2L3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFPuppi' ),
      level = cms.string( 'L2L3Residual' )
    )
    process.hltAK8PuppiJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltAK8PuppiJetCorrectorL2','hltAK8PuppiJetCorrectorL3','hltAK8PuppiJetCorrectorL2L3' )
    )
    process.hltAK8PuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK8PuppiJets'),
      correctors = cms.VInputTag('hltAK8PuppiJetCorrector'),
    )

    ## MET: Puppi Raw

    # Puppi candidates for MET
    process.pfNoLepPUPPI = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag( _particleFlowCands ),
      pdgId = cms.vint32( 1, 2, 22, 111, 130, 310, 2112, 211, -211, 321, -321, 999211, 2212, -2212 )
    )
    process.pfLeptonsPUPPET = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag( _particleFlowCands ),
      pdgId = cms.vint32( -11, 11, -13, 13 ),
    )
    process.puppiNoLep = puppi.clone(
      candName = 'pfNoLepPUPPI',
      vertexName = _primaryVerticesGood,
      PtMaxPhotons = 20.,
    )
    process.hltPuppiForMET = cms.EDProducer('CandViewMerger',
      src = cms.VInputTag( 'puppiNoLep','pfLeptonsPUPPET' ),
    )
    process.hltPuppiMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( 'hltPuppiForMET' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    ## MET: Puppi Type-1
    process.hltPuppiMETTypeOneCorrector = cms.EDProducer( 'PFJetMETcorrInputProducer',
      src = cms.InputTag( 'hltAK4PuppiJets' ),
      type1JetPtThreshold = cms.double( 15.0 ),
      skipEMfractionThreshold = cms.double( 0.9 ),
      skipEM = cms.bool( True ),
      jetCorrLabelRes = cms.InputTag( 'hltAK4PuppiJetCorrector' ),
      offsetCorrLabel = cms.InputTag( 'hltAK4PuppiJetCorrectorL1' ),
      skipMuons = cms.bool( True ),
      skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
      jetCorrEtaMax = cms.double( 9.9 ),
      jetCorrLabel = cms.InputTag( 'hltAK4PuppiJetCorrector' )
    )
    process.hltPuppiMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
      src = cms.InputTag( 'hltPuppiMET' ),
      srcCorrections = cms.VInputTag( 'hltPuppiMETTypeOneCorrector:type1' )
    )

    ## Sequence: Puppi Jets and MET
    process.HLTPuppiJMEReconstruction = cms.Sequence(
       (process.pfNoLepPUPPI
      * process.puppiNoLep
      + process.pfLeptonsPUPPET)
      * process.hltPuppiForMET
      * process.hltPuppiMET
      + process.hltPuppi
      *(process.hltAK4PuppiJets
      * process.hltAK4PuppiJetCorrectorL1
      * process.hltAK4PuppiJetCorrectorL2
      * process.hltAK4PuppiJetCorrectorL3
      * process.hltAK4PuppiJetCorrectorL2L3
      * process.hltAK4PuppiJetCorrector
      * process.hltAK4PuppiJetsCorrected
      * process.hltPuppiMETTypeOneCorrector
      * process.hltPuppiMETTypeOne
      + process.hltAK8PuppiJets
      * process.hltAK8PuppiJetCorrectorL2
      * process.hltAK8PuppiJetCorrectorL3
      * process.hltAK8PuppiJetCorrectorL2L3
      * process.hltAK8PuppiJetCorrector
      * process.hltAK8PuppiJetsCorrected)
    )

    ## Sequence: JME Reconstruction
    setattr(process, name, cms.Sequence(
#        process.HLTCaloJetsReconstruction
        process.HLTCaloMETReconstruction
      + process.HLTPFClusterJMEReconstruction
      + process.HLTAK4PFJetsReconstruction
      + process.HLTAK8PFJetsReconstruction
      + process.HLTPFJetsCHSReconstruction
      + process.HLTPFMETReconstruction
      + process.HLTPFCHSMETReconstruction
      + process.HLTPFSoftKillerMETReconstruction
      + process.HLTPuppiJMEReconstruction
    ))

    ####
    #### Redefine process.reconstruction
    ####

    # redefine input to fixedGridRhoFastjetAll
    # (in principle, this is not needed, since JESC modules are configured with 'fixedGridRhoFastjetAllTmp';
    #  nevertheless, this modification is applied, in order to make sure _particleFlowCands is consistently used)
    process.fixedGridRhoFastjetAll.pfCandidatesTag = _particleFlowCands

    # redefine process.hgcalLocalReco sequence
    # to disable unnecessary producers in HGCal local reconstruction
    process.hgcalLocalRecoSequence = cms.Sequence(
        process.HGCalUncalibRecHit
      + process.HGCalRecHit
      + process.hgcalLayerClusters
      + process.hgcalMultiClusters
      + process.particleFlowRecHitHGC
      + process.particleFlowClusterHGCal
      + process.particleFlowClusterHGCalFromMultiCl
    )

    process.calolocalreco = cms.Sequence(
        process.ecalLocalRecoSequence
      + process.hcalLocalRecoSequence
      + process.hgcalLocalRecoSequence
    )

    process.localreco = cms.Sequence(
        process.bunchSpacingProducer
      + process.calolocalreco
      + process.muonlocalreco
      + process.trackerlocalreco
      + process.fastTimingLocalReco
    )

    process.reconstruction = cms.Sequence(
        process.localreco
      + process.globalreco
      + process.highlevelreco
      + process.logErrorHarvester
    )

    # process.globalreco: reconstruction up to PFClusters
    if (not hasattr(process, 'globalreco_tracking')) and hasattr(process, 'globalreco_trackingTask'):
       process.globalreco_tracking = cms.Sequence(process.globalreco_trackingTask)

    process.tofPIDSequence = cms.Sequence(
        process.unsortedOfflinePrimaryVertices4DnoPID
      + process.tofPID4DnoPID
      + process.unsortedOfflinePrimaryVertices4D
      + process.tofPID
    )

    process.globalreco = cms.Sequence(
        process.caloTowersRec
      + process.ecalClusters
#      + process.egammaGlobalReco

        # tracking
      + process.globalreco_tracking
      + process.standalonemuontracking # needs to be included for early muons of PF

        # timing
      + process.fastTimingGlobalReco # necessary for MTD inputs to PF
      + process.tofPIDSequence # contains tofPID maps

        # insert CaloJets sequence in process.globalreco
        # (module muons1stStep from muonGlobalReco requires AK4CaloJets [*])
      + process.HLTCaloJetsReconstruction # was: process.jetGlobalReco

      + process.muonGlobalReco
#      + process.muoncosmicreco
      + process.particleFlowCluster
#      + process.pfTrackingGlobalReco
    )

    # [*] modify CaloJets input to muons1stStep
    process.muons1stStep.JetExtractorPSet.JetCollectionLabel = 'hltAK4CaloJets'

    # process.highlevelreco: PF + JME (w/o CaloJets)
    process.highlevelreco = cms.Sequence(
        process.particleFlowReco
      * getattr(process, name)
    )

#    # disable use of timing information in simPFProducer
#    del process.simPFProducer.trackTimeValueMap

    #### ------------------------------------------------------------

    # update JESC via local SQLite file
    CondDBJECFile = CondDB.clone(connect = 'sqlite_file:/afs/cern.ch/work/m/missirol/public/phase2/JESC/PhaseIIFall17_V5b_MC.db' )
    process.jec = cms.ESSource('PoolDBESSource', CondDBJECFile, toGet = cms.VPSet())
    for _tmp in [
      'AK4PF',
#      'AK4PFchs',
#      'AK4PFPuppi',
#      'AK8PF',
#      'AK8PFchs',
#      'AK8PFPuppi',
    ]:
      process.jec.toGet.append(
        cms.PSet(
          record = cms.string('JetCorrectionsRecord'),
          tag = cms.string('JetCorrectorParametersCollection_PhaseIIFall17_V5b_MC_'+_tmp),
          label = cms.untracked.string(_tmp),
        )
      )

    # Add an ESPrefer to override JEC that might be available from the global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')

    return process

def customize_hltPhase2_TICL(process):

    # Note: at the moment, this is not really a self-contained customization function
    # please use it only after "customize_hltPhase2_JME"

    #### check if TICL task exists
    if not hasattr(process, 'iterTICLTask'):
       raise RuntimeError('process.iterTICLTask not found')

    process.iterTICLSequence = cms.Sequence(process.iterTICLTask)
    process.globalreco += process.iterTICLSequence
    process = injectTICLintoPF(process)

    return process
