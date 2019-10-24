from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_VBF_HToInvisible_M125_14TeV_PU140'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.psetName = 'jmeTriggerNTuple_step3_CHSPFJets_11_0_0_pre7_cfg.py'
config.JobType.inputFiles = ['step3_CHSPFJets_11_0_0_pre7.py']
config.JobType.pyCfgParams = ['output=VBF_HToInvisible_M125_14TeV_PU140.root']
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDataset = '/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-PU140_106X_upgrade2023_realistic_v3-v1/MINIAODSIM'
config.Data.secondaryInputDataset = '/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19DR-PU140_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW'
config.Data.outLFNDirBase = '/store/user/missirol/jme_trigger/jmeTriggerNtuples/Phase2/191026/VBF_HToInvisible_M125_14TeV_PU140'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 100000

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
