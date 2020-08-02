#!/bin/bash

hltGetConfiguration /dev/CMSSW_11_2_0/GRun/V5 \
 --full \
 --offline \
 --mc \
 --unprescale \
 --timing \
 --process HLT2 \
 --max-events 10 \
 --input /store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/1E007C6B-0236-774C-AE76-16FF40129ED8.root \
 --globaltag 110X_mcRun3_2021_realistic_v10 \
 --path HLTriggerFirstPath,MC_PFMET_v17,MC_CaloMET_v8,MC_AK4PFJets_v17,MC_AK4CaloJets_v9,HLTriggerFinalPath,HLTAnalyzerEndpath > dev_CMSSW_11_2_0_GRun_V5_MCPaths_cfg.py

edmConfigDump dev_CMSSW_11_2_0_GRun_V5_MCPaths_cfg.py > dev_CMSSW_11_2_0_GRun_V5_MCPaths_configDump.py
