JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

Set up CMSSW area:

```
cmsrel CMSSW_10_6_1_patch3
cd CMSSW_10_6_1_patch3/src
cmsenv
git cms-addpkg HLTrigger/Configuration
git clone https://missirol@github.com/missirol/JMETriggerAnalysis.git
scram b
```

Set up VOMS proxy:
```
voms-proxy-init --voms cms
```

Create configuration file to run customized HLT menu on RAW
```
cd JMETriggerAnalysis/NTuplizer/test
./create_HLT_JetMETPFlowWithoutPreselV4_cfg.py
```

Notes:

* Golden JSON for 2018 (PromptReco):
```
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt
```

* Golden JSON for 2018 (ABC-ReReco + D-PromptReco):
```
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
```

* Input Samples:

  - Data:
```
dasgoclient --query="file dataset=/SingleMuon/Run2018D-v1/RAW"
dasgoclient --query="file dataset=/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD"
hltInfo root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/110000/12952201-BFB3-4142-B24C-983B753A4300.root
```

  - MC (special TSG samples in 10_2_X):
```
dasgoclient --query="dataset dataset=/*/*102X_upgrade2018_realistic_v15*/GEN-SIM-RAW"
```
