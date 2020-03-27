JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

### Setup

Set up CMSSW area:

 * `11_1_X`:
```shell
cmsrel CMSSW_11_1_0_pre4
cd CMSSW_11_1_0_pre4/src
cmsenv

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```
