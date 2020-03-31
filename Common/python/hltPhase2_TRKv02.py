import FWCore.ParameterSet.Config as cms

from RecoLocalTracker.SiPixelRecHits._generic_default_cfi import _generic_default
from RecoLocalTracker.SiPixelClusterizer.SiPixelClusterizerDefault_cfi import SiPixelClusterizerDefault as _SiPixelClusterizerDefault
from RecoLocalTracker.SubCollectionProducers.phase2trackClusterRemover_cfi import phase2trackClusterRemover as _phase2trackClusterRemover
from RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi import looseMTS as _looseMTS
from RecoTracker.FinalTrackSelectors.trackAlgoPriorityOrderDefault_cfi import trackAlgoPriorityOrderDefault as _trackAlgoPriorityOrderDefault
from RecoTracker.MeasurementDet._MeasurementTrackerESProducer_default_cfi import _MeasurementTrackerESProducer_default
from RecoTracker.TkSeedGenerator.trackerClusterCheckDefault_cfi import trackerClusterCheckDefault as _trackerClusterCheckDefault
from RecoTracker.TrackProducer.TrackProducer_cfi import TrackProducer as _TrackProducer

### Needed for initialStepSeeds
from RecoTracker.TkSeedGenerator.seedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer_cfi import seedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer as _seedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer

### Needed for sorting of primary vertices
from RecoJets.JetProducers.caloJetsForTrk_cff import caloTowerForTrk as _caloTowerForTrk

### Rationale: define HLT tracking as "offline tracking" + modifications. The modifications are those in this file.

# Initial step
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepSeedLayers as _initialStepSeedLayers
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepTrackingRegions as _initialStepTrackingRegions
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepHitDoublets as _initialStepHitDoublets
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepHitQuadruplets as _initialStepHitQuadruplets
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepTracks as _initialStepTracks
from RecoTracker.IterativeTracking.InitialStep_cff import initialStepSelector as _initialStepSelector
# High-pt triplet
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepSeedLayers as _highPtTripletStepSeedLayers
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepTrackingRegions as _highPtTripletStepTrackingRegions
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepHitDoublets as _highPtTripletStepHitDoublets
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepHitTriplets as _highPtTripletStepHitTriplets
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepSeeds as _highPtTripletStepSeeds
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepTrackCandidates as _highPtTripletStepTrackCandidates
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepTracks as _highPtTripletStepTracks
from RecoTracker.IterativeTracking.HighPtTripletStep_cff import highPtTripletStepSelector as _highPtTripletStepSelector

def customize_hltPhase2_TRKv02(process):

    ###
    ### Modules (taken from configuration developed by TRK POG)
    ###

    ### The rationale is to take from the release as much as possible, 
    ### and use clone() calls with changes to the parameters if needed

    process.TrackProducer = _TrackProducer.clone(
      TTRHBuilder = 'WithTrackAngle',
    )

    process.trackAlgoPriorityOrder = _trackAlgoPriorityOrderDefault.clone(
        algoOrder = [
            'initialStep',
            'highPtTripletStep'
        ],
    )    

    process.PixelCPEGenericESProducer = _generic_default.clone(
        LoadTemplatesFromDB = False,
        TruncatePixelCharge = False,
        Upgrade = True,
        UseErrorsFromTemplates = False,
    )

    process.MeasurementTracker = _MeasurementTrackerESProducer_default.clone(
        Phase2StripCPE = 'Phase2StripCPE'
    )
    del process.MeasurementTracker.appendToDataLabel

    process.siPixelClustersPreSplitting = _SiPixelClusterizerDefault.clone(
        ElectronPerADCGain = 600.0,
        MissCalibrate = False,
        Phase2Calibration = True,
        src = 'simSiPixelDigis:Pixel'
    )
    del process.siPixelClustersPreSplitting.ClusterMode

    process.siPixelClusters = _SiPixelClusterizerDefault.clone(
        ElectronPerADCGain = 600.0,
        MissCalibrate = False,
        Phase2Calibration = True,
        src = 'simSiPixelDigis:Pixel'
    )
    del process.siPixelClusters.ClusterMode

    process.trackerClusterCheck = _trackerClusterCheckDefault.clone(
        doClusterCheck = False,
    )

    process.caloTowerForTrk = _caloTowerForTrk.clone(
        HBThreshold = 0.3,
        HBThreshold1 = 0.1,
        HBThreshold2 = 0.2,
        HEDThreshold = 0.2,
        HEDThreshold1 = 0.1,
        HESThreshold = 0.2,
        HESThreshold1 = 0.1,
        HcalPhase = 1,
        hbheInput = 'hbhereco'
    )

    ### INITIAL STEP
    process.initialStepSeedLayers = _initialStepSeedLayers.clone(
                layerList = [
                    'BPix1+BPix2+BPix3+BPix4', 
                    'BPix1+BPix2+BPix3+FPix1_pos', 
                    'BPix1+BPix2+BPix3+FPix1_neg', 
                    'BPix1+BPix2+FPix1_pos+FPix2_pos', 
                    'BPix1+BPix2+FPix1_neg+FPix2_neg', 
                    'BPix1+FPix1_pos+FPix2_pos+FPix3_pos', 
                    'BPix1+FPix1_neg+FPix2_neg+FPix3_neg', 
                    'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos', 
                    'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg', 
                    'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos', 
                    'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg', 
                    'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos', 
                    'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg', 
                    'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos', 
                    'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg', 
                    'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos', 
                    'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
                ]
    )

    process.initialStepTrackingRegions = _initialStepTrackingRegions.clone(
        RegionPSet = dict(
            originRadius = 0.03,
        ),
    )

    process.initialStepHitDoublets = _initialStepHitDoublets.clone(
        layerPairs = [0, 1, 2],
    )

    process.initialStepHitQuadruplets = _initialStepHitQuadruplets.clone(
        CAPhiCut = 0.175,
        CAThetaCut = 0.001,
        mightGet = [
            'IntermediateHitDoublets_initialStepHitDoublets__RECO', 
            'IntermediateHitDoublets_initialStepHitDoublets__RECO'
        ],
    )

    # The usual "initialStepSeeds" from "InitialStep_cff" is a
    # "SeedCreatorFromRegionConsecutiveHitsEDProducer", but in this configuration we want a
    # "SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer"
    process.initialStepSeeds = _seedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer.clone(
        SeedComparitorPSet = dict(
            ComponentName = 'PixelClusterShapeSeedComparitor',
            ClusterShapeCacheSrc = cms.InputTag('siPixelClusterShapeCache'),
            ClusterShapeHitFilterName = cms.string('ClusterShapeHitFilter'),
            FilterAtHelixStage = cms.bool(False),
            FilterPixelHits = cms.bool(True),
            FilterStripHits = cms.bool(False)
        ),
        magneticField = '',
        mightGet = [
            'RegionsSeedingHitSets_initialStepHitQuadruplets__RECO', 
            'RegionsSeedingHitSets_initialStepHitQuadruplets__RECO'
        ],
        propagator = 'PropagatorWithMaterial',
        seedingHitSets = 'initialStepHitQuadruplets'
    )

    # process.initialStepTrackCandidates ### Where does this come from?

    process.initialStepTracks = _initialStepTracks.clone(
        AlgorithmName = 'initialStep',
        Fitter = 'FlexibleKFFittingSmoother',
        src = 'initialStepTrackCandidates',
        TTRHBuilder = 'WithTrackAngle',
    )

    # Some PSets for TrackSelector
    hltInitialStepLoose = _looseMTS.clone(
        chi2n_par = 2.0,
        d0_par1 = [0.8, 4.0],
        d0_par2 = [0.6, 4.0],
        dz_par1 = [0.9, 4.0],
        dz_par2 = [0.8, 4.0],
        maxNumberLostLayers = 3,
        minNumber3DLayers = 3,
        minNumberLayers = 3,
        name = 'initialStepLoose',
        res_par = [0.003, 0.002],
    )
    hltInitialStepTight = _looseMTS.clone(
        chi2n_par = 1.4,
        d0_par1 = [0.7, 4.0],
        d0_par2 = [0.5, 4.0],
        dz_par1 = [0.8, 4.0],
        dz_par2 = [0.7, 4.0],
        keepAllTracks = True,
        maxNumberLostLayers = 2,
        minNumber3DLayers = 3,
        minNumberLayers = 3,
        name = 'initialStepTight',
        preFilterName = 'initialStepLoose',
        qualityBit = 'tight',
        res_par = [0.003, 0.002],
    )
    hltInitialStep = _looseMTS.clone(
        chi2n_par = 1.2,
        d0_par1 = [0.6, 4.0],
        d0_par2 = [0.45, 4.0],
        dz_par1 = [0.7, 4.0],
        dz_par2 = [0.55, 4.0],
        maxNumberLostLayers = 2,
        minNumber3DLayers = 3,
        minNumberLayers = 3,
        name = 'initialStep',
        preFilterName = 'initialStepTight',
        qualityBit = 'highPurity',
        res_par = [0.003, 0.001],
        keepAllTracks = True,
    )

    process.initialStepSelector = _initialStepSelector.clone(
        #beamspot = 'offlineBeamSpot', #Already default
        src = 'initialStepTracks',
        trackSelectors = [
            hltInitialStepLoose,
            hltInitialStepTight,
            hltInitialStep
        ]
        #vertices = 'firstStepPrimaryVertices', #Already default
    )

    process.siPixelClusterShapeCache = cms.EDProducer('SiPixelClusterShapeCacheProducer',
        onDemand = cms.bool(False),
        src = cms.InputTag('siPixelClusters')
    )
   
    ### HIGH PT TRIPLET ITERATION
    
    process.highPtTripletStepClusters = _phase2trackClusterRemover.clone(
        maxChi2 = 9.0,
        overrideTrkQuals = 'initialStepSelector:initialStep',
        trackClassifier = ':QualityMasks',
        trajectories = 'initialStepTracks'
    )

    process.highPtTripletStepSeedLayers =  _highPtTripletStepSeedLayers.clone(
        layerList = [
            'BPix1+BPix2+BPix3', 
            'BPix2+BPix3+BPix4', 
            'BPix1+BPix3+BPix4', 
            'BPix1+BPix2+BPix4', 
            'BPix2+BPix3+FPix1_pos', 
            'BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos', 
            'BPix1+BPix2+FPix1_neg', 
            'BPix2+FPix1_pos+FPix2_pos', 
            'BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos', 
            'BPix1+FPix1_neg+FPix2_neg', 
            'FPix1_pos+FPix2_pos+FPix3_pos', 
            'FPix1_neg+FPix2_neg+FPix3_neg', 
            'BPix1+FPix2_pos+FPix3_pos', 
            'BPix1+FPix2_neg+FPix3_neg', 
            'FPix2_pos+FPix3_pos+FPix4_pos', 
            'FPix2_neg+FPix3_neg+FPix4_neg', 
            'FPix3_pos+FPix4_pos+FPix5_pos', 
            'FPix3_neg+FPix4_neg+FPix5_neg', 
            'FPix4_pos+FPix5_pos+FPix6_pos', 
            'FPix4_neg+FPix5_neg+FPix6_neg', 
            'FPix5_pos+FPix6_pos+FPix7_pos', 
            'FPix5_neg+FPix6_neg+FPix7_neg', 
            'FPix6_pos+FPix7_pos+FPix8_pos', 
            'FPix6_neg+FPix7_neg+FPix8_neg'
        ]
    )

    process.highPtTripletStepTrackingRegions = _highPtTripletStepTrackingRegions.clone(
        RegionPSet = dict(
            originRadius = 0.02,
            ptMin = 0.7,
        )
    )
    
    process.highPtTripletStepHitDoublets = _highPtTripletStepHitDoublets.clone()
    
    process.highPtTripletStepHitTriplets = _highPtTripletStepHitTriplets.clone(
        CAHardPtCut = 0.5,
        CAPhiCut = 0.06,
        CAThetaCut = 0.003,
        #doublets = 'highPtTripletStepHitDoublets', # default
        mightGet = [
            'IntermediateHitDoublets_highPtTripletStepHitDoublets__RECO', 
            'IntermediateHitDoublets_highPtTripletStepHitDoublets__RECO'
        ],
    )
    
    process.highPtTripletStepSeeds = _highPtTripletStepSeeds.clone(
        magneticField = '',
        mightGet = [
            'RegionsSeedingHitSets_highPtTripletStepHitTriplets__RECO', 
            'RegionsSeedingHitSets_highPtTripletStepHitTriplets__RECO'
        ],
        propagator = 'PropagatorWithMaterial',
        #seedingHitSets = 'highPtTripletStepHitTriplets', # default
    )
    
    process.highPtTripletStepTracks = _highPtTripletStepTracks.clone(
        TTRHBuilder = 'WithTrackAngle',
        alias = 'ctfWithMaterialTracks',
        #beamSpot = 'offlineBeamSpot', # default
        
        src = 'highPtTripletStepTrackCandidates',
        useHitsSplitting = False,
        useSimpleMF = False
    )
    
    # Some PSets for TrackSelector
    hltHighPtTripletStepLoose = _looseMTS.clone(
        chi2n_par = 2.0,
        d0_par1 = [0.7, 4.0],
        d0_par2 = [0.6, 4.0],
        dz_par1 = [0.8, 4.0],
        dz_par2 = [0.6, 4.0],
        maxNumberLostLayers = 3,
        minNumber3DLayers = 3,
        minNumberLayers = 3,
        name = 'highPtTripletStepLoose',
        res_par = [0.003, 0.002],
    )
    hltHighPtTripletStepTight = _looseMTS.clone(
        chi2n_par = 1.0,
        d0_par1 = [0.6, 4.0],
        d0_par2 = [0.5, 4.0],
        dz_par1 = [0.7, 4.0],
        dz_par2 = [0.6, 4.0],
        keepAllTracks = True,
        maxNumberLostLayers = 2,
        minNumber3DLayers = 3,
        minNumberLayers = 3,
        name = 'highPtTripletStepTight',
        preFilterName = 'highPtTripletStepLoose',
        qualityBit = 'tight',
        res_par = [0.003, 0.002],
    )
    hltHighPtTripletStep = _looseMTS.clone(
        chi2n_par = 0.8,
        d0_par1 = [0.6, 4.0],
        d0_par2 = [0.45, 4.0],
        dz_par1 = [0.7, 4.0],
        dz_par2 = [0.55, 4.0],
        keepAllTracks = True,
        maxNumberLostLayers = 2,
        minNumber3DLayers = 4,
        minNumberLayers = 4,
        min_nhits = 4,
        name = 'highPtTripletStep',
        preFilterName = 'highPtTripletStepTight',
        qualityBit = 'highPurity',
        res_par = [0.003, 0.001],
    )

    process.highPtTripletStepSelector = _highPtTripletStepSelector.clone(
        #beamspot = 'offlineBeamSpot',
        #src = 'highPtTripletStepTracks',
        trackSelectors = [
            hltHighPtTripletStepLoose,
            hltHighPtTripletStepTight,
            hltHighPtTripletStep,
        ],
        #vertices = 'firstStepPrimaryVertices'
    )

    ### The two iterations ended here, now put them together and do vertices.

    process.MeasurementTrackerEvent = cms.EDProducer('MeasurementTrackerEventProducer',
        Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'),
        badPixelFEDChannelCollectionLabels = cms.VInputTag('siPixelDigis'),
        inactivePixelDetectorLabels = cms.VInputTag(),
        inactiveStripDetectorLabels = cms.VInputTag('siStripDigis'),
        measurementTracker = cms.string(''),
        pixelCablingMapLabel = cms.string(''),
        pixelClusterProducer = cms.string('siPixelClusters'),
        skipClusters = cms.InputTag(''),
        stripClusterProducer = cms.string(''),
        switchOffPixelsIfEmpty = cms.bool(True)
    )
        
    process.generalTracks = cms.EDProducer('TrackListMerger',
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(5.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag('initialStepTracks', 'highPtTripletStepTracks'),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(True),
        hasSelector = cms.vint32(1, 1),
        indivShareFrac = cms.vdouble(1.0, 0.16),
        makeReKeyedSeeds = cms.untracked.bool(False),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag(
            cms.InputTag('initialStepSelector','initialStep'),
            cms.InputTag('highPtTripletStepSelector','highPtTripletStep')),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(True),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('trackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )
    
    process.inclusiveVertexFinder = cms.EDProducer('InclusiveVertexFinder',
        beamSpot = cms.InputTag('offlineBeamSpot'),
        clusterizer = cms.PSet(
            clusterMaxDistance = cms.double(0.05),
            clusterMaxSignificance = cms.double(4.5),
            clusterMinAngleCosine = cms.double(0.5),
            distanceRatio = cms.double(20),
            maxTimeSignificance = cms.double(3.5),
            seedMax3DIPSignificance = cms.double(9999),
            seedMax3DIPValue = cms.double(9999),
            seedMin3DIPSignificance = cms.double(1.2),
            seedMin3DIPValue = cms.double(0.005)
        ),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3),
        fitterTini = cms.double(256),
        maxNTracks = cms.uint32(30),
        maximumLongitudinalImpactParameter = cms.double(0.3),
        maximumTimeSignificance = cms.double(3),
        minHits = cms.uint32(8),
        minPt = cms.double(0.8),
        primaryVertices = cms.InputTag('offlinePrimaryVertices'),
        tracks = cms.InputTag('generalTracks'),
        useDirectVertexFitter = cms.bool(True),
        useVertexReco = cms.bool(True),
        vertexMinAngleCosine = cms.double(0.95),
        vertexMinDLen2DSig = cms.double(2.5),
        vertexMinDLenSig = cms.double(0.5),
        vertexReco = cms.PSet(
            finder = cms.string('avr'),
            primcut = cms.double(1),
            seccut = cms.double(3),
            smoothing = cms.bool(True)
        )
    )
    
    process.trackVertexArbitrator = cms.EDProducer('TrackVertexArbitrator',
        beamSpot = cms.InputTag('offlineBeamSpot'),
        dLenFraction = cms.double(0.333),
        dRCut = cms.double(0.4),
        distCut = cms.double(0.04),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3),
        fitterTini = cms.double(256),
        maxTimeSignificance = cms.double(3.5),
        primaryVertices = cms.InputTag('offlinePrimaryVertices'),
        secondaryVertices = cms.InputTag('vertexMerger'),
        sigCut = cms.double(5),
        trackMinLayers = cms.int32(4),
        trackMinPixels = cms.int32(1),
        trackMinPt = cms.double(0.4),
        tracks = cms.InputTag('generalTracks')
    )

    ###
    ### Sequences
    ###

    process.itLocalReco = cms.Sequence(
        process.siPhase2Clusters
      + process.siPixelClusters
      + process.siPixelClusterShapeCache
      + process.siPixelClustersPreSplitting
      + process.siPixelRecHits
      + process.siPixelRecHitsPreSplitting
    )

    process.otLocalReco = cms.Sequence(
        process.MeasurementTrackerEvent
    )

    process.initialStepPVSequence = cms.Sequence(
        process.firstStepPrimaryVerticesUnsorted #uses beamspot
      + process.initialStepTrackRefsForJets
      + process.hcalGlobalRecoSequence
      + process.caloTowerForTrk
      + process.ak4CaloJetsForTrk
      + process.firstStepPrimaryVertices
    )

    process.initialStepSequence = cms.Sequence(
        process.initialStepSeedLayers
      + process.initialStepTrackingRegions
      + process.initialStepHitDoublets
      + process.initialStepHitQuadruplets
      + process.initialStepSeeds
      + process.initialStepTrackCandidates
      + process.initialStepTracks
      + process.initialStepPVSequence
      + process.initialStepSelector
    )

    process.highPtTripletStepSequence = cms.Sequence(
        process.highPtTripletStepClusters
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepTrackingRegions
      + process.highPtTripletStepHitDoublets
      + process.highPtTripletStepHitTriplets
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepSeeds
      + process.highPtTripletStepTrackCandidates
      + process.highPtTripletStepTracks
      + process.highPtTripletStepSelector
      + process.initialStepSeedClusterMask # needed by electron, but also by highPtTripletStepSeedClusterMask
      + process.highPtTripletStepSeedClusterMask
    )

    process.vertexReco = cms.Sequence(
        process.unsortedOfflinePrimaryVertices4DnoPID
      + process.unsortedOfflinePrimaryVertices
      + process.trackWithVertexRefSelectorBeforeSorting4DnoPID
      + process.trackWithVertexRefSelectorBeforeSorting
      + process.trackRefsForJetsBeforeSorting4DnoPID
      + process.trackRefsForJetsBeforeSorting
      + process.tpClusterProducer
      + process.tofPID4DnoPID
      + process.unsortedOfflinePrimaryVertices4D
      + process.trackWithVertexRefSelectorBeforeSorting4D
      + process.trackRefsForJetsBeforeSorting4D
      + process.tofPID
      + process.quickTrackAssociatorByHits
      + process.trackTimeValueMapProducer
      + process.caloTowerForTrk
      + process.ak4CaloJetsForTrk
#      + process.offlinePrimaryVertices4DnoPIDWithBS
#      + process.offlinePrimaryVertices4DWithBS
#      + process.offlinePrimaryVertices4D
      + process.offlinePrimaryVerticesWithBS
      + process.offlinePrimaryVertices
#      + process.generalV0Candidates
      + process.inclusiveVertexFinder
      + process.vertexMerger
      + process.trackVertexArbitrator
      + process.inclusiveSecondaryVertices
#      + process.offlinePrimaryVertices4DnoPID
    )

    process.globalreco_tracking = cms.Sequence(
        process.itLocalReco
      + process.otLocalReco
      + process.offlineBeamSpot #cmssw_10_6
      + process.trackerClusterCheck
      + process.initialStepSequence
      + process.highPtTripletStepSequence
      + process.generalTracks
      + process.vertexReco 
      + process.standalonemuontracking # needs to be included for early muons of PF
    )

    # remove globalreco_trackingTask to avoid any ambiguities
    # with the updated sequence process.globalreco_tracking
    if hasattr(process, 'globalreco_trackingTask'):
       del process.globalreco_trackingTask

    return process
