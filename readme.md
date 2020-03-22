JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

### Setup

Set up CMSSW area:

 * `10_2_X`:
```shell
cmsrel CMSSW_10_2_21
cd CMSSW_10_2_21/src
cmsenv

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run2
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```
