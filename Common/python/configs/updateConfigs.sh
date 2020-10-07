#!/bin/bash

opts=(
 TRKv00
 TRKv00_TICL
 TRKv02
 TRKv02_TICL
 TRKv06
 TRKv06_TICL
 TRKv06p1
 TRKv06p1_TICL
 TRKv07p2
 TRKv07p2_TICL
)

for opt_i in "${opts[@]}"; do
  cmsDriver.py step3 \
    --geometry Extended2026D49 --era Phase2C9 \
    --conditions 111X_mcRun4_realistic_T15_v2 \
    --processName RECO2 \
    --step RAW2DIGI,RECO \
    --eventcontent RECO \
    --datatier RECO \
    --filein /store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/FEVT/PU200_castor_111X_mcRun4_realistic_T15_v1-v1/100000/DA18C0FC-1189-D64B-B3B6-44F3F96F1840.root \
    --mc \
    --nThreads 4 \
    --nStreams 4 \
    --no_exec \
    -n 10 \
    --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
    --customise JMETriggerAnalysis/Common/customizeHLTForPhase2.customise_hltPhase2_scheduleJMETriggers_${opt_i} \
    --customise_commands 'process.prune()\n' \
    --python_filename hltPhase2_${opt_i}_cfg.py
done
unset opt_i opts
