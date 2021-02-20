import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets as _ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi as _ak8PFJetsPuppi
from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
from JMETriggerAnalysis.Common.multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble_cfi\
 import multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble as _nSiPixelClusters

def addPaths_MC_PFClusterJME(process):
    process.hltPreMCAK4PFClusterJets = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPreMCAK8PFClusterJets = process.hltPreMCAK4PFClusterJets.clone()

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

    process.hltAK8PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
      rParam = 0.8,
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

    process.MC_AK8PFClusterJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PFClusterJets
      + process.HLTParticleFlowClusterSequence
      + process.HLTParticleFlowClusterRefsSequence
      + process.hltAK8PFClusterJets
      + process.HLTEndSequence
    )

    ## MET
    process.hltPreMCPFClusterMET = process.hltPreMCPFMET.clone()

    process.hltPFClusterMET = cms.EDProducer('PFClusterMETProducer',
      src = cms.InputTag('hltParticleFlowClusterRefs'),
      globalThreshold = cms.double(0.0),
      alias = cms.string(''),
    )

    process.HLTPFClusterMETSequence = cms.Sequence(
        process.HLTParticleFlowClusterSequence
      + process.HLTParticleFlowClusterRefsSequence
      + process.hltPFClusterMET
    )

    process.MC_PFClusterMET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFClusterMET
      + process.HLTPFClusterMETSequence
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_AK4PFClusterJets_v1)
       process.schedule_().append(process.MC_AK8PFClusterJets_v1)
       process.schedule_().append(process.MC_PFClusterMET_v1)

    return process

def addPaths_MC_PFPuppiJME(process):

    process.hltPreMCAK4PFPuppiJets = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPreMCAK8PFPuppiJets = process.hltPreMCAK4PFPuppiJets.clone()

    process.hltPixelClustersMultiplicity = _nSiPixelClusters.clone(src = 'siPixelClusters', defaultValue = -1.)

    process.hltPFPuppi = _puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltVerticesPF',
      usePUProxyValue = True,
      PUProxyValue = 'hltPixelClustersMultiplicity',
    )

    process.HLTPFPuppiSequence = cms.Sequence(
        process.HLTDoCaloSequencePF
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltVerticesPF
      + process.hltPixelClustersMultiplicity
      + process.hltPFPuppi
    )

    ## AK4
    process.hltAK4PFPuppiJets = _ak4PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK4PFPuppiCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK4PFPuppiCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK4PFPuppiCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag('hltAK4PFPuppiCorrectorL2', 'hltAK4PFPuppiCorrectorL3')
    )

    process.hltAK4PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK4PFPuppiJets'),
      correctors = cms.VInputTag('hltAK4PFPuppiCorrector')
    )

    process.HLTAK4PFPuppiJetsSequence = cms.Sequence(
        process.HLTPFPuppiSequence
      + process.hltAK4PFPuppiJets
      + process.hltAK4PFPuppiCorrectorL2
      + process.hltAK4PFPuppiCorrectorL3
      + process.hltAK4PFPuppiCorrector
      + process.hltAK4PFPuppiJetsCorrected
    )

    process.MC_AK4PFPuppiJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFPuppiJets
      + process.HLTAK4PFPuppiJetsSequence
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_AK4PFPuppiJets_v1)

    ## AK8
    process.hltAK8PFPuppiJets = _ak8PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK8PFPuppiCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK8PFPuppiCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK8PFPuppiCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag('hltAK8PFPuppiCorrectorL2', 'hltAK8PFPuppiCorrectorL3')
    )

    process.hltAK8PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK8PFPuppiJets'),
      correctors = cms.VInputTag('hltAK8PFPuppiCorrector')
    )

    process.HLTAK8PFPuppiJetsSequence = cms.Sequence(
        process.HLTPFPuppiSequence
      + process.hltAK8PFPuppiJets
      + process.hltAK8PFPuppiCorrectorL2
      + process.hltAK8PFPuppiCorrectorL3
      + process.hltAK8PFPuppiCorrector
      + process.hltAK8PFPuppiJetsCorrected
    )

    process.MC_AK8PFPuppiJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PFPuppiJets
      + process.HLTAK8PFPuppiJetsSequence
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_AK8PFPuppiJets_v1)

    ## MET
    process.hltPreMCPFPuppiMET = process.hltPreMCPFMET.clone()

    process.hltPFPuppiNoLep = _puppiNoLep.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltVerticesPF',
      usePUProxyValue = True,
      PUProxyValue = 'hltPixelClustersMultiplicity',
    )

    process.hltPFPuppiMET = cms.EDProducer('PFMETProducer',
      alias = cms.string(''),
      applyWeight = cms.bool(True),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.0),
      parameters = cms.PSet(),
      src = cms.InputTag('hltParticleFlow'),
      srcWeights = cms.InputTag('hltPFPuppiNoLep'),
    )

    process.HLTPFPuppiMETSequence = cms.Sequence(
        process.HLTDoCaloSequencePF
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltVerticesPF
      + process.hltPixelClustersMultiplicity
      + process.hltPFPuppiNoLep
      + process.hltPFPuppiMET
    )

    process.hltPFPuppiMETOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPFPuppiMET'
    )

    process.MC_PFPuppiMET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFPuppiMET
      + process.HLTPFPuppiMETSequence
      + process.hltPFPuppiMETOpenFilter
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_PFPuppiMET_v1)

    ## Puppi parameters
    for mod_i in [process.hltPFPuppi, process.hltPFPuppiNoLep]:
      for algo_idx in range(len(mod_i.algos)):
        if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
          raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())

        for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
          mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += 20.7 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
          mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= 0.000634

    return process
