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

# [optional] PR#29007
git cms-addpkg RecoParticleFlow/PFClusterProducer
git cherry-pick a3c21e57ed1899a071c5ca1059e3407917763ca9
git cherry-pick 267d0bb1ada0cddcff815422a7e85c502cb3ecb5

git cms-merge-topic missirol:devel_pixvtx_buildfile_1100pre13
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

 * `11_1_X`:
```shell
cmsrel CMSSW_11_1_0_pre3
cd CMSSW_11_1_0_pre3/src
cmsenv

# [optional] PR#28976
git cms-addpkg RecoParticleFlow/PFClusterProducer
git cherry-pick 445d74b1df707d06a208d5f1a95b8492fc187239
git cherry-pick e68e48a95b4d20a9904d35b94dc4772b4298b135

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

Set up crab3 and VOMS proxy:

```shell
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms
```
