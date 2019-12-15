JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

### Setup

Set up CMSSW area:

```shell
cmsrel CMSSW_11_0_0_pre7
cd CMSSW_11_0_0_pre7/src
cmsenv
git cms-merge-topic missirol:devel_pixvtx_buildfile
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```
