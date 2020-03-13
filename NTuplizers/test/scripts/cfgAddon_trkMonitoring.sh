#!/bin/bash

echo """
process.TFileService = cms.Service('TFileService', fileName = cms.string('trackStudy.root'))
process.source.fileNames = [
 '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/05BFAD3E-3F91-1843-ABA2-2040324C7567.root',
]
from JMETriggerAnalysis.Common.TrackHistogrammer_cfi import TrackHistogrammer
process.TrackHistograms_generalTracks = TrackHistogrammer.clone(src = cms.InputTag('generalTracks'))
from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
process.VertexHistograms_offlinePrimaryVertices = VertexHistogrammer.clone(src = cms.InputTag('offlinePrimaryVertices'))
process.trkMonitoringSeq = cms.Sequence(
    process.TrackHistograms_generalTracks
  + process.VertexHistograms_offlinePrimaryVertices
)
process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
process.schedule.extend([process.trkMonitoringEndPath])
process.maxEvents.input = 20"""
