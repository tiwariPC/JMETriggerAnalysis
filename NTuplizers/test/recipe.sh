#!/bin/bash

# [1] 2018 HLT menu (10_1_X)
# Comment: HLT menu used in Run-2 (2018)
cmsrel CMSSW_10_1_10
cd CMSSW_10_1_10_patch1/src
cmsenv
scram b
hltConfigFromDB \
 --runNumber 323775 \
 --v2 \
 --offline \
 --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
 --output hlt_run323775_reference.root \
 > hlt_run323775_cfg.py

# [2] default Run-3 HLT menu (11_1_X) on Run-2 Data
# Comments:
#  - current (default) HLT menu for Run-3 (in the 11_1_X release) customized to run on Run-2
#  - expected to give results comparable to [1]
cmsrel CMSSW_11_1_0_Patatrack
cd CMSSW_11_1_0_Patatrack/src
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3_devel
cmsenv
scram b
hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
 --full \
 --offline \
 --timing \
 --process HLT2 \
 --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
 --globaltag 103X_dataRun2_HLT_v1 \
 --customise HLTrigger/Configuration/customizeHLTforCMSSW.synchronizeHCALHLTofflineRun3on2018data \
 --customise JMETriggerAnalysis/Common/customise_SiPixelClusterProducerForRun2.customise_SiPixelClusterProducerForRun2 \
 --max-events 30 \
 --data \
 > hlt_Run2_112X_default.py

## Run-3 MC
#hltGetConfiguration /dev/CMSSW_11_2_0/GRun/V5 \
# --full \
# --offline \
# --mc \
# --unprescale \
# --timing \
# --process HLT2 \
# --max-events 10 \
# --input /store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/1E007C6B-0236-774C-AE76-16FF40129ED8.root \
# --globaltag 110X_mcRun3_2021_realistic_v10 \
# --path HLTriggerFirstPath,MC_PFMET_v17,MC_CaloMET_v8,MC_AK4PFJets_v17,MC_AK4CaloJets_v9,HLTriggerFinalPath,HLTAnalyzerEndpath > dev_CMSSW_11_2_0_GRun_V5_MCPaths_cfg.py
#
#edmConfigDump dev_CMSSW_11_2_0_GRun_V5_MCPaths_cfg.py > dev_CMSSW_11_2_0_GRun_V5_MCPaths_configDump.py
