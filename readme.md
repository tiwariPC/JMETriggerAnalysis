JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

### Setup

Set up CMSSW area:

```shell
cmsrel CMSSW_11_0_0_pre7
cd CMSSW_11_0_0_pre7/src
cmsenv
git cms-addpkg HLTrigger/Configuration
git clone https://missirol@github.com/missirol/JMETriggerAnalysis.git -o missirol
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```

Create configuration file to run customized HLT menu on RAW

```shell
cd JMETriggerAnalysis/NTuplizers/test
./create_HLT_JetMETPFlowWithoutPreselV4_cfg.py
```

### Notes

* Golden JSON for 2018 (PromptReco):
```shell
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt
```

* Golden JSON for 2018 (ABC-ReReco + D-PromptReco):
```shell
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
```

* Data Samples:
```shell
dasgoclient --query="file dataset=/SingleMuon/Run2018D-v1/RAW"
dasgoclient --query="file dataset=/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD"
hltInfo root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/110000/12952201-BFB3-4142-B24C-983B753A4300.root
```

* MC Samples (special TSG samples in CMSSW_10_2_X):
```shell
dasgoclient --query="dataset dataset=/*/*102X_upgrade2018_realistic_v15*/GEN-SIM-RAW"
```
