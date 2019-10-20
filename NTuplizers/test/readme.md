**Step 1**: create configuration file to run customized HLT menu on RAW Data:
```
./create_HLT_JetMETPFlowWithoutPreselV4_cfg.sh
```
  This will create the file `HLT_JetMETPFlowWithoutPreselV4_cfg.py`

**Step 2**: produce a test NTuple
```
cmsRun jmeTriggerNTuple_HLTJetMETPFlowWithoutPreselV4_cfg.py n=10
```
