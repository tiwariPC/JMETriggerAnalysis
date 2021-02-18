#!/bin/bash

set -e

hltGetConfiguration /dev/CMSSW_11_2_0/GRun/V19 \
 --full \
 --offline \
 --unprescale \
 --process HLT2 \
 --globaltag 112X_mcRun3_2021_realistic_v13 \
 --input /store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6-v1/130003/1D612E3B-8CAC-9D4B-B773-79C37D3F9D12.root \
 --max-events 10 \
 > tmp.py

edmConfigDump tmp.py > ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_2_0_GRun_V19_configDump.py
rm -f tmp.py
