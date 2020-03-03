JMETriggerAnalysis
==================

CMSSW Packages for JetMET Trigger Studies

### Setup

Set up CMSSW area:

 * `11_0_X`:
```shell
cmsrel CMSSW_11_0_1
cd CMSSW_11_0_1/src
cmsenv
git cms-merge-topic missirol:devel_pixvtx_buildfile_1100pre13
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

 * `11_1_X`:
```shell
cmsrel CMSSW_11_1_0_pre3
cd CMSSW_11_1_0_pre3/src
cmsenv
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```
