hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
 --full \
 --offline \
 --mc \
 --unprescale \
 --process HLT2 \
 --max-events 10 \
 --input /store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/50000/1E007C6B-0236-774C-AE76-16FF40129ED8.root \
 --globaltag 110X_mcRun3_2021_realistic_v10 \
 --path HLTriggerFirstPath,MC_PFMET_v17,MC_CaloMET_v8,MC_AK4PFJets_v17,MC_AK4CaloJets_v9,HLTriggerFinalPath,HLTAnalyzerEndpath > dev__CMSSW_11_1_0__GRun__V11__cfg.py

edmConfigDump dev__CMSSW_11_1_0__GRun__cfg.py > dev__CMSSW_11_1_0__GRun__V11__configDump.py
