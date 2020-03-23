import FWCore.ParameterSet.Config as cms

process = cms.Process('JESCTXT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('gt', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.parseArguments()

if opts.gt is None:
   raise RuntimeError('name of GlobalTag not specified [use command-line argument "gt=X"]')

process.GlobalTag.globaltag = opts.gt

if not opts.tag:
   opts.tag = opts.gt

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.source = cms.Source('EmptySource')

process.readAK4PF = cms.EDAnalyzer('JetCorrectorDBReader',  
  # below is the communication to the database 
  payloadName = cms.untracked.string('AK4PF'),
  # this is used ONLY for the name of the printed txt files.
  # You can use any name that you like, but it is recommended to use the GT name that you retrieved the files from.
  globalTag = cms.untracked.string(opts.tag),
  printScreen = cms.untracked.bool(False),
  createTextFile = cms.untracked.bool(True),
)

process.readAK4PFchs   = process.readAK4PF.clone(payloadName = 'AK4PFchs')
process.readAK4PFPuppi = process.readAK4PF.clone(payloadName = 'AK4PFPuppi')

process.readAK8PF      = process.readAK4PF.clone(payloadName = 'AK8PF')
process.readAK8PFchs   = process.readAK4PF.clone(payloadName = 'AK8PFchs')
process.readAK8PFPuppi = process.readAK4PF.clone(payloadName = 'AK8PFPuppi')

process.p = cms.Path(
    process.readAK4PF
  * process.readAK4PFchs
  * process.readAK4PFPuppi
  * process.readAK8PF
  * process.readAK8PFchs
  * process.readAK8PFPuppi
)
