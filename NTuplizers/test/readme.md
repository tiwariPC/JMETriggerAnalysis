**Step 1**: create configuration file to run customized HLT menu on RAW Data:
```
./create_HLT_JetMETPFlowWithoutPreselV4_cfg.sh
```
  This will create the file `HLT_JetMETPFlowWithoutPreselV4_cfg.py`

**Step 2**: produce a test NTuple
```
cmsRun jmeTriggerNTuple_HLTJetMETPFlowWithoutPreselV4_cfg.py n=10
```

### Notes

TWiki: `https://twiki.cern.ch/twiki/bin/viewauth/CMS/HighLevelTriggerPhase2#MC_samples`

```
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM
```

```
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19DR-PU140_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-PU140_106X_upgrade2023_realistic_v3-v1/MINIAODSIM
```

```
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW
/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM
```
