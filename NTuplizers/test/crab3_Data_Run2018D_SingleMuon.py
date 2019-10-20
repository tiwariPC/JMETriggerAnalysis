from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_Data_Run2018D_SingleMuon'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.psetName = 'jmeTriggerNTuple_HLTJetMETPFlowWithoutPreselV4_cfg.py'
config.JobType.inputFiles = ['HLT_JetMETPFlowWithoutPreselV4_cfg.py']
config.JobType.pyCfgParams = ['output=Data_Run2018D_SingleMuon.root']

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'Automatic'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
config.Data.inputDataset = '/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD'
config.Data.secondaryInputDataset = '/SingleMuon/Run2018D-v1/RAW'
config.Data.outLFNDirBase = '/store/user/missirol/jme_trigger/jmeTriggerNtuples/191020/Data_Run2018D_SingleMuon'
#config.Data.unitsPerJob = 100
config.Data.totalUnits = 100000
