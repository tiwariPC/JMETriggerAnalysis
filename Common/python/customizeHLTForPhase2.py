import FWCore.ParameterSet.Config as cms

from JMETriggerAnalysis.Common.hltPhase2_L1T import customise_hltPhase2_L1T
from JMETriggerAnalysis.Common.hltPhase2_TRKv00 import customise_hltPhase2_TRKv00
from JMETriggerAnalysis.Common.hltPhase2_TRKv02 import customise_hltPhase2_TRKv02
from JMETriggerAnalysis.Common.hltPhase2_TRKv06 import customise_hltPhase2_TRKv06
from JMETriggerAnalysis.Common.hltPhase2_PF import customise_hltPhase2_PF
from JMETriggerAnalysis.Common.hltPhase2_JME import customise_hltPhase2_JME

from HLTrigger.Configuration.common import producers_by_type

from RecoHGCal.TICL.iterativeTICL_cff import injectTICLintoPF

def customise_hltPhase2_enableTICLInHGCalReconstruction(process):
    if not hasattr(process, 'iterTICLTask'):
       raise RuntimeError('process.iterTICLTask not found')

    process.iterTICLSequence = cms.Sequence(process.iterTICLTask)
    process.globalreco += process.iterTICLSequence
    process = injectTICLintoPF(process)

    return process

def customise_hltPhase2_disableMTDReconstruction(process):
    for _tmp1 in [
      'fastTimingLocalReco',
      'fastTimingGlobalReco',
      'tofPIDSequence',
    ]:
      if hasattr(process, _tmp1):
        for _tmp2 in getattr(process, _tmp1).moduleNames():
          if hasattr(process, _tmp2):
            process.__delattr__(_tmp2)
        process.__delattr__(_tmp1)

    # disable use of timing information in simPFProducer
    if hasattr(process, 'simPFProducer') and hasattr(process.simPFProducer, 'trackTimeValueMap'):
       del process.simPFProducer.trackTimeValueMap

    # remove MTD element from PFBlock inputs
    process.particleFlowBlock.elementImporters = [
      _tmp for _tmp in process.particleFlowBlock.elementImporters if _tmp.importerName != 'TrackTimingImporter'
    ]

    return process

def customise_hltPhase2_redefineReconstructionSequencesCommon(process):
    if not hasattr(process, 'reconstruction'):
       raise RuntimeError('reconstruction sequence process.reconstruction not found')

    # redefine input to fixedGridRhoFastjetAll
    # (in principle, this is not needed, since JESC modules are configured with 'fixedGridRhoFastjetAllTmp';
    #  nevertheless, this modification is applied, in order to make sure _particleFlowCands is consistently used)
    process.fixedGridRhoFastjetAll.pfCandidatesTag = 'particleFlowTmp'

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
#     + process.egammaGlobalReco

        # tracking
      + process.globalreco_tracking
      + process.standalonemuontracking # needs to be included for early muons of PF

        # timing
      + process.fastTimingGlobalReco # necessary for MTD inputs to PF
      + process.tofPIDSequence # contains tofPID maps

        # insert CaloJets sequence in process.globalreco
        # (module muons1stStep from muonGlobalReco requires AK4CaloJets [1])
      + process.hltAK4CaloJets # was: process.jetGlobalReco

      + process.muonGlobalReco
#      + process.muoncosmicreco
      + process.particleFlowCluster
#      + process.pfTrackingGlobalReco
    )

    if hasattr(process, 'hltAK4CaloJets'):
       process.globalreco += process.hltAK4CaloJets
       # modify CaloJets input to muons1stStep
       process.muons1stStep.JetExtractorPSet.JetCollectionLabel = 'hltAK4CaloJets'
    else:
       process.globalreco += process.jetGlobalReco

    process.highlevelreco = cms.Sequence(
        process.particleFlowReco
    )

    process.reconstruction = cms.Sequence(
        process.localreco
      + process.globalreco
      + process.highlevelreco
    )

    return process

def customise_hltPhase2_redefineReconstructionSequences(process, useL1T=False, TRK='v06', useTICL=True, useMTD=False):
    if useL1T:
       process = customise_hltPhase2_L1T(process)

    _trkCustomFuncDict = {
      'v00': customise_hltPhase2_TRKv00,
      'v02': customise_hltPhase2_TRKv02,
      'v06': customise_hltPhase2_TRKv06,
    }
    process = _trkCustomFuncDict[TRK](process)

    process = customise_hltPhase2_PF(process)
    process = customise_hltPhase2_JME(process)
    process = customise_hltPhase2_redefineReconstructionSequencesCommon(process)

    if not useMTD:
       process = customise_hltPhase2_disableMTDReconstruction(process)

    if useTICL:
       process = customise_hltPhase2_enableTICLInHGCalReconstruction(process)

    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process):
    process.HLTJMESequence = cms.Sequence(
        process.HLTCaloMETReconstruction
#     + process.HLTCaloJetsReconstruction
      + process.HLTPFClusterJMEReconstruction
      + process.HLTAK4PFJetsReconstruction
      + process.HLTAK8PFJetsReconstruction
      + process.HLTPFJetsCHSReconstruction
      + process.HLTPFMETsReconstruction
      + process.HLTPFCHSMETReconstruction
      + process.HLTPFSoftKillerMETReconstruction
      + process.HLTPuppiJMEReconstruction
    )

    process.reconstruction += process.HLTJMESequence

    process.p = cms.Path(process.RawToDigi + process.reconstruction)

    ## schedule
    # FIXME: if the original schedule contains paths for L1T reco, the command below will remove them
    # so this needs to be improved if one wants to be able to run (part of) the L1T reco on a separate path
    process.setSchedule_(cms.Schedule(process.p))

    return process

def customise_hltPhase2_scheduleJMETriggers(process):
    ## sequence: HLT-JME objects (without filters)
    ## (kept for now to study object performance without preselections)
    process.HLTJMESequence = cms.Sequence(
        process.HLTCaloMETReconstruction
#     + process.HLTCaloJetsReconstruction
      + process.HLTPFClusterJMEReconstruction
      + process.HLTAK4PFJetsReconstruction
      + process.HLTAK8PFJetsReconstruction
      + process.HLTPFJetsCHSReconstruction
      + process.HLTPFMETsReconstruction
      + process.HLTPFCHSMETReconstruction
      + process.HLTPFSoftKillerMETReconstruction
      + process.HLTPuppiJMEReconstruction
    )

    ## sequence: ParticleFlow
    process.HLTParticleFlowSequence = cms.Sequence(
        process.RawToDigi
      + process.localreco
      + process.globalreco
      + process.highlevelreco
    )

    ## sequence: AK4 Jets, PFCHS
    process.HLTAK4PFCHSJetsReconstruction = cms.Sequence(
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
    )

    ## sequence: AK8 Jets, PFCHS
    process.HLTAK8PFCHSJetsReconstruction = cms.Sequence(
        process.particleFlowPtrs
      + process.goodOfflinePrimaryVertices
      + process.pfPileUpJME
      + process.pfNoPileUpJME
      + process.hltAK8PFCHSJets
      + process.hltAK8PFCHSJetCorrectorL1
      + process.hltAK8PFCHSJetCorrectorL2
      + process.hltAK8PFCHSJetCorrectorL3
      + process.hltAK8PFCHSJetCorrectorL2L3
      + process.hltAK8PFCHSJetCorrector
      + process.hltAK8PFCHSJetsCorrected
    )

    ## sequence: AK4 Jets, Puppi
    process.HLTAK4PuppiJetsReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPuppi
      + process.hltAK4PuppiJets
      + process.hltAK4PuppiJetCorrectorL1
      + process.hltAK4PuppiJetCorrectorL2
      + process.hltAK4PuppiJetCorrectorL3
      + process.hltAK4PuppiJetCorrectorL2L3
      + process.hltAK4PuppiJetCorrector
      + process.hltAK4PuppiJetsCorrected
    )

    ## sequence: AK8 Jets, Puppi
    process.HLTAK8PuppiJetsReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPuppi
      + process.hltAK8PuppiJets
      + process.hltAK8PuppiJetCorrectorL2
      + process.hltAK8PuppiJetCorrectorL3
      + process.hltAK8PuppiJetCorrectorL2L3
      + process.hltAK8PuppiJetCorrector
      + process.hltAK8PuppiJetsCorrected
    )

    ## sequence: Puppi MET (Raw)
    process.HLTPuppiMETReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPuppiNoLep
      + process.hltPuppiMET
    )

    ## Single-Jet triggers: modules
    _l1tSinglePFJet100 = cms.EDFilter('HLT1PFJet',
      MaxEta = cms.double(5.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(100.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(85),
    )

    _hltSinglePFJet100 = cms.EDFilter('HLT1PFJet',
      MaxEta = cms.double(5.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(100.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(85),
    )

    process.l1tSingleAK4PFPuppiJet200 = _l1tSinglePFJet100.clone(inputTag = 'ak4PFL1Puppi', MinPt = 200.)

    process.hltSingleAK4PFJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PFJetsCorrected', MinPt = 550.)
    process.hltSingleAK4PFCHSJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PFCHSJetsCorrected', MinPt = 550.)
    process.hltSingleAK4PuppiJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PuppiJetsCorrected', MinPt = 550.)

#   process.hltSingleAK8PFJet300 = _hltSinglePFJet100.clone(inputTag = 'hltAK8PFJetsCorrected', MinPt = 300.)
#   process.hltSingleAK8PFCHSJet300 = _hltSinglePFJet100.clone(inputTag = 'hltAK8PFCHSJetsCorrected', MinPt = 300.)
#   process.hltSingleAK8PuppiJet300 = _hltSinglePFJet100.clone(inputTag = 'hltAK8PuppiJetsCorrected', MinPt = 300.)

    ## HT triggers: modules
    _hltHTMHT = cms.EDProducer('HLTHtMhtProducer',
      excludePFMuons = cms.bool(False),
      jetsLabel = cms.InputTag(''),
      maxEtaJetHt = cms.double(4.0),
      maxEtaJetMht = cms.double(999.0),
      minNJetHt = cms.int32(0),
      minNJetMht = cms.int32(0),
      minPtJetHt = cms.double(30.0),
      minPtJetMht = cms.double(0.0),
      pfCandidatesLabel = cms.InputTag(''),
      usePt = cms.bool(True)
    )

    _hltHT100 = cms.EDFilter('HLTHtMhtFilter',
      htLabels = cms.VInputTag(''),
      meffSlope = cms.vdouble(1.0),
      mhtLabels = cms.VInputTag(''),
      minHt = cms.vdouble(100.0),
      minMeff = cms.vdouble(0.0),
      minMht = cms.vdouble(0.0),
      saveTags = cms.bool(True)
    )

    process.l1tPFPuppiHT = _hltHTMHT.clone(jetsLabel = 'ak4PFL1Puppi', maxEtaJetHt = 5.0, minPtJetHt = 30.)
    process.hltPFPuppiHT = _hltHTMHT.clone(jetsLabel = 'hltAK4PuppiJetsCorrected', maxEtaJetHt = 4.0, minPtJetHt = 30.)

    process.l1tPFPuppiHT250 = _hltHT100.clone(htLabels = ['l1tPFPuppiHT'], mhtLabels = ['l1tPFPuppiHT'], minHt = [250.])
    process.hltPFPuppiHT1050 = _hltHT100.clone(htLabels = ['hltPFPuppiHT'], mhtLabels = ['hltPFPuppiHT'], minHt = [1050.])

    ## MET triggers: modules
    _hltPFMET200 = cms.EDFilter('HLT1PFMET',
      MaxEta = cms.double(-1.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(200.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(87),
    )

    process.l1tPFPuppiMET110 = _hltPFMET200.clone(inputTag = 'l1PFMetPuppi', MinPt = 110.)

    process.hltPFMET200 = _hltPFMET200.clone(inputTag = 'hltPFMET', MinPt = 200.)
    process.hltPFCHSMET200 = _hltPFMET200.clone(inputTag = 'hltPFCHSMET', MinPt = 200.)
    process.hltPuppiMET200 = _hltPFMET200.clone(inputTag = 'hltPuppiMET', MinPt = 200.)

    ## trigger paths
    process.MC_JME_v1 = cms.Path(process.HLTParticleFlowSequence + process.HLTJMESequence)

    process.HLT_AK4PFJet550_v1 = cms.Path(process.l1tSingleAK4PFPuppiJet200 + process.HLTParticleFlowSequence + process.HLTAK4PFJetsReconstruction + process.hltSingleAK4PFJet550)
    process.HLT_AK4PFCHSJet550_v1 = cms.Path(process.l1tSingleAK4PFPuppiJet200 + process.HLTParticleFlowSequence + process.HLTAK4PFCHSJetsReconstruction + process.hltSingleAK4PFCHSJet550)
    process.HLT_AK4PuppiJet550_v1 = cms.Path(process.l1tSingleAK4PFPuppiJet200 + process.HLTParticleFlowSequence + process.HLTAK4PuppiJetsReconstruction + process.hltSingleAK4PuppiJet550)

    process.HLT_PFPuppiHT1050_v1 = cms.Path(process.l1tPFPuppiHT + process.l1tPFPuppiHT250 + process.HLTParticleFlowSequence + process.HLTAK4PuppiJetsReconstruction + process.hltPFPuppiHT + process.hltPFPuppiHT1050)

    process.HLT_PFMET200_v1 = cms.Path(process.l1tPFPuppiMET110 + process.HLTParticleFlowSequence + process.hltPFMET + process.hltPFMET200)
    process.HLT_PFCHSMET200_v1 = cms.Path(process.l1tPFPuppiMET110 + process.HLTParticleFlowSequence + process.HLTPFCHSMETReconstruction + process.hltPFCHSMET200)
    process.HLT_PuppiMET200_v1 = cms.Path(process.l1tPFPuppiMET110 + process.HLTParticleFlowSequence + process.HLTPuppiMETReconstruction + process.hltPuppiMET200)

    ## schedule
    # FIXME: if the original schedule contains paths for L1T reco, the command below will remove them
    # so this needs to be improved if one wants to be able to run (part of) the L1T reco on a separate path
    process.setSchedule_(cms.Schedule(*[
      process.MC_JME_v1,

      process.HLT_AK4PFJet550_v1,
      process.HLT_AK4PFCHSJet550_v1,
      process.HLT_AK4PuppiJet550_v1,

      process.HLT_PFPuppiHT1050_v1,

      process.HLT_PFMET200_v1,
      process.HLT_PFCHSMET200_v1,
      process.HLT_PuppiMET200_v1,
    ]))

    return process

# retuning of Puppi parameters for TRK-v06
def customise_hltPhase2_retunePuppiForTRKv06(process):
    for mod_i in producers_by_type(process, 'PuppiProducer'):
       for algo_idx in range(len(mod_i.algos)):
         if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
            raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())
         for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
            mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += 18.5 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
            mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= 1.45

    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv00(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv00_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv02(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv02_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv06(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv06_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv00(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv00_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv02(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv02_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv06(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv06_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process
