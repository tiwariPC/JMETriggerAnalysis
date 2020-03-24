import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')

process.load('Configuration.StandardSequences.Services_cff')

import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

#!!opts.register('gt', None,
#!!              vpo.VarParsing.multiplicity.singleton,
#!!              vpo.VarParsing.varType.string,
#!!              'argument of process.GlobalTag.globaltag')

opts.parseArguments()

#!!process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#!!if opts.gt is not None:
#!!#   raise RuntimeError('name of GlobalTag not specified [use command-line argument "gt=X"]')
#!!   process.GlobalTag.globaltag = opts.gt

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opts.maxEvents))

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('file:EGamma_Run2018D_22Jan2019_v2_MINIAOD.root'),
  secondaryFileNames = cms.untracked.vstring(),
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v15'

from JMETriggerAnalysis.NTuplizers.hltPrinter_cfi import hltPrinter
process.hltPrinter = hltPrinter.clone()

process.p = cms.Path(
  process.hltPrinter
)
