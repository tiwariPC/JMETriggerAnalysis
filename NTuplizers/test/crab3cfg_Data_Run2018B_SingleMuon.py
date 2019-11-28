from WMCore.Configuration import Configuration

sample_name = 'Data_Run2018B_SingleMuon'

store_dir = 'jme_trigger/jmeTriggerNtuples/pfMET/v02/191103'

MIN_DSET = '/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD'
RAW_DSET = '/SingleMuon/Run2018B-v1/RAW'

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
config.JobType.maxJobRuntimeMin = 2500
config.JobType.maxMemoryMB = 3000
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'EventAwareLumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
config.Data.inputDataset = MIN_DSET
config.Data.secondaryInputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/missirol/'+store_dir+'/'+sample_name
config.Data.unitsPerJob = 20000
#config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
