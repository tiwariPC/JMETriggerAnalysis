###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

#opts.register('globalTag', None,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.string,
#              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_GRun',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining HLT reconstruction')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### HLT configuration
###
if opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3Tracking
  process = customizeHLTRun3Tracking(process)

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3TrackingAllPixelVertices
  process = customizeHLTRun3TrackingAllPixelVertices(process)

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.OutputModule:', _modname

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.EndPath:', _modname

# remove selected cms.Path objects from HLT config-dump
print '-'*108
print '{:<99} | {:<4} |'.format('cms.Path', 'keep')
print '-'*108
for _modname in sorted(process.paths_()):
    _keepPath = _modname.startswith('MC_') and ('Jets' in _modname or 'MET' in _modname)
#    _keepPath |= _modname.startswith('MC_ReducedIterativeTracking')
    if _keepPath:
      print '{:<99} | {:<4} |'.format(_modname, '+')
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print '{:<99} | {:<4} |'.format(_modname, '')
print '-'*108

# remove FastTimerService
#
# SPS removing the removal of FastTimeService - not needed? caused crash...
#
#del process.FastTimerService

# remove MessageLogger
del process.MessageLogger

###
### customizations
###
from JMETriggerAnalysis.Common.customise_hlt import *
process = addPaths_MC_PFClusterJME(process)
process = addPaths_MC_PFPuppiJME(process)

###
### Jet Response Analyzer (JRA) NTuple
###
import JetMETAnalysis.JetAnalyzers.DefaultsHLT_cff as Defaults
from JetMETAnalysis.JetAnalyzers.addAlgorithmHLT import addAlgorithm
for algorithm in [
  'ak4puppiHLT',
  'ak4caloHLT',
  'ak4pfclusterHLT',
  'ak4pfHLT',
  'ak8caloHLT',
  'ak8pfclusterHLT',
  'ak8pfHLT',
  'ak8puppiHLT',
]:
  addAlgorithm(process, algorithm, Defaults)
  getattr(process, algorithm).srcRho = 'hltFixedGridRhoFastjetAll'
  getattr(process, algorithm).srcRhoHLT = ''
  getattr(process, algorithm).srcRhos = ''
  getattr(process, algorithm).deltaRMax = 0.2

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JRA-NTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
   )

# input EDM files

#
# SPS removing secondaryFileNames - not found when running, not needed?
#
#process.source.secondaryFileNames = []
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     #'/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/07569899-8384-6444-AD42-613509DEE3E1.root',
     # SPS  DoublePhoton sample only for testing!
     '/store/mc/Run3Winter20DRMiniAOD/DoublePhoton_FlatPt-5To300/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6-v2/40000/7BA83802-8EF6-B246-893F-09A1657B7CC7.root'
   ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
if opts.verbosity > 0:
   print '--- hltJRA_mcRun4_cfg.py ---'
   print ''
   print 'option: output =', opts.output
   print 'option: reco =', opts.reco
   print 'option: dumpPython =', opts.dumpPython
   print ''
   print 'process.GlobalTag =', process.GlobalTag.dumpPython()
   print 'process.source =', process.source.dumpPython()
   print 'process.maxEvents =', process.maxEvents.dumpPython()
   print 'process.options =', process.options.dumpPython()
   print '----------------------------'

###
### HLT configuration
###
if opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3Tracking
  process = customizeHLTRun3Tracking(process)

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3TrackingAllPixelVertices
  process = customizeHLTRun3TrackingAllPixelVertices(process)

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.OutputModule:', _modname

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.EndPath:', _modname

# remove selected cms.Path objects from HLT config-dump
print '-'*108
print '{:<99} | {:<4} |'.format('cms.Path', 'keep')
print '-'*108
for _modname in sorted(process.paths_()):
    _keepPath = _modname.startswith('MC_') and ('Jets' in _modname or 'MET' in _modname)
    _keepPath |= _modname.startswith('MC_ReducedIterativeTracking')
    if _keepPath:
      print '{:<99} | {:<4} |'.format(_modname, '+')
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print '{:<99} | {:<4} |'.format(_modname, '')
print '-'*108

# remove FastTimerService
#
# SPS removing the removal of FastTimeService - not needed? caused crash...
#
#del process.FastTimerService

# ###
# ### customizations
# ###
# from JMETriggerAnalysis.Common.customise_hlt import *
# process = addPath_MC_AK4PFClusterJets(process)
# process = addPath_MC_AK4PFPuppiJets(process)


