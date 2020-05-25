from JMETriggerAnalysis.NTuplizers.hltPhase2_TRKv06_TICL_cfg import cms, process

# command-line options
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

# EDM output
process.RECOoutput = cms.OutputModule('PoolOutputModule',
  dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RECO'),
    filterName = cms.untracked.string('')
  ),
  fileName = cms.untracked.string(opts.output),
  outputCommands = cms.untracked.vstring((
    'drop *',
    'keep GenEventInfoProduct_generator_*_*',
    'keep *_addPileupInfo_*_*',
    'keep *_fixedGridRhoFastjetAll*_*_*',
    'keep *_hltFixedGridRhoFastjetAll*_*_*',
    'keep *_hlt*Jets__*',
    'keep *_ak*GenJets__*',
    'keep *_ak*GenJetsNoNu__*',
  )),
  splitLevel = cms.untracked.int32(0)
)

process.RECOoutput_step = cms.EndPath(process.RECOoutput)
process.schedule.append(process.RECOoutput_step)

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/02C1FCCC-315F-404C-ABF7-A65154C46C28.root',
   ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())
