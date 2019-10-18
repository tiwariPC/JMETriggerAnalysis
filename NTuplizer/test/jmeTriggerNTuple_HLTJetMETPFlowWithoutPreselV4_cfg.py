from HLT_JetMETPFlowWithoutPreselV4_cfg import cms, process

# remove RECO step (EDM output file will not be produced)
process.schedule.remove(process.RECOSIMoutput_step)

# analysis sequence (JMETrigger NTuple)
process.jmeTriggerNTuplizer = cms.EDAnalyzer('NTuplizer',

  recoPFCandidateCollections = cms.PSet(

    hltParticleFlow = cms.InputTag('hltParticleFlow'+'::'+process.name_()),
  ),

#  recoPFJetCollections = cms.PSet(
#
#    hltAK4PFJets = cms.InputTag('hltAK4PFJets'+'::'+process.name_()),
#  ),

  recoCaloMETCollections = cms.PSet(

    hltMet = cms.InputTag('hltMet'+'::'+process.name_()),
    hltMetClean = cms.InputTag('hltMetClean'+'::'+process.name_()),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMet = cms.InputTag('hltPFMETProducer'+'::'+process.name_()),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'+'::'+process.name_()),
  ),
)

process.analysisSequence = cms.Sequence(
  process.jmeTriggerNTuplizer
)

process.analysis_step = cms.EndPath(process.analysisSequence)

process.schedule.extend([process.analysis_step])

# create TFileService to be accessed by NTuplizer plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string( 'out.root' ))

#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()

process.maxEvents.input = 10
