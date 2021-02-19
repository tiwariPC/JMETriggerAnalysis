### Tools for JME studies on the Run-3 HLT reconstruction

* [Tests on HLT Tracking for Run-3](#tests-on-hlt-tracking-for-run-3)

----------

### Tests on HLT Tracking for Run-3

```
cmsrel CMSSW_11_2_0_Patatrack
cd CMSSW_11_2_0_Patatrack/src
cmsenv
git cms-remote add mmasciov
git checkout -b run3tracking mmasciov/tracking-allPVs
git cms-addpkg $(git diff $CMSSW_VERSION --name-only | cut -d/ -f-2 | uniq)
git cms-checkdeps -a
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3_devel_112X
scram b -j 12
```

The baseline HLT menu for Run-3 in 11_2_X can be found in
[Common/python/configs/HLT_dev_CMSSW_11_2_0_GRun_V19_configDump.py](https://github.com/missirol/JMETriggerAnalysis/blob/run3_devel_112X/Common/python/configs/HLT_dev_CMSSW_11_2_0_GRun_V19_configDump.py).

It was created with `hltGetConfiguration` via the commands listed in
[`Common/test/dumpHLTMenus_mcRun3.sh`](https://github.com/missirol/JMETriggerAnalysis/blob/run3_devel_112X/Common/test/dumpHLTMenus_mcRun3.sh).

An example of how to enable the different tracking customisations can be found in
[`NTuplizers/test/jmeTriggerNTuple_cfg.py`](https://github.com/missirol/JMETriggerAnalysis/blob/run3_devel_112X/NTuplizers/test/jmeTriggerNTuple_cfg.py)
(see option `reco`).
Test commands:
```
# (a) Run-3 tracking: standard
cmsRun jmeTriggerNTuple_cfg.py maxEvents=1 reco=HLT_Run3TRK output=out_HLT_Run3TRK.root

# (b) Run-3 tracking: all pixel vertices
cmsRun jmeTriggerNTuple_cfg.py maxEvents=1 reco=HLT_Run3TRKWithPU output=out_HLT_Run3TRKWithPU.root
```

----------
