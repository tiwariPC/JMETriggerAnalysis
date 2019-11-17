from WMCore.Configuration import Configuration

store_dir = 'jme_trigger/jmeTriggerNtuples/Phase2/trackingV2/191114'
sample_name = 'TTTo2L2Nu_14TeV_PU200'

MIN_DSET = '/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM'
RAW_DSET = '/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW'

config = Configuration()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_'+sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jmeTriggerNTuple_cfg.py'
config.JobType.inputFiles = []
config.JobType.pyCfgParams = ['output='+sample_name+'.root']
config.JobType.maxJobRuntimeMin = 2880
config.JobType.maxMemoryMB = 10000
config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDataset = MIN_DSET
config.Data.secondaryInputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/missirol/'+store_dir+'/'+sample_name
config.Data.unitsPerJob = 100
config.Data.totalUnits = 250000

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
