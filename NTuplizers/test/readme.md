
```
hltGetConfiguration --full --offline --process HLT2 --unprescale \
 --data --globaltag 101X_dataRun2_HLT_v7 \
   /frozen/2018/2e34/v3.6/HLT/V2 \
 >  frozen_2018_2e34_v3p6_HLT_V2.py

edmConfigDump frozen_2018_2e34_v3p6_HLT_V2.py > ../python/frozen_2018_2e34_v3p6_HLT_V2_configDump.py
rm frozen_2018_2e34_v3p6_HLT_V2.py

cmsRun jmeTriggerNTuple_HLT_cfg.py \
 inputFiles=root://cms-xrd-global.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/Run2018D/EphemeralHLTPhysics/RAW/Run_323775/FBF117EE-5699-F147-BBFC-07815D5A2582.root \
 reco=HLT_2018 \
 maxEvents=10
```
