### Tools for JME studies on the Run-3 HLT reconstruction

* [Setup](#setup)
* [Configuration files for HLT Run-3 menus](#configuration-files-for-hlt-run-3-menus)
* [Configuration with JME trigger paths for testing](#configuration-with-jme-trigger-paths-for-testing)
* [Inputs for HLT Jet Energy Scale Corrections workflow](#inputs-for-hlt-jet-energy-scale-corrections-workflow)
* [Instructions for testing latest HLT menus on Run-2 data](#instructions-for-testing-latest-hlt-menus-on-run-2-data)
* [Miscellanea](#miscellanea)

----------

### Setup
```shell
cmsrel CMSSW_11_1_0_pre4
cd CMSSW_11_1_0_pre4/src
cmsenv

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
scram b
```

----------

### Configuration files for HLT Run-3 menus

Configuration files corresponding to different types of HLT menus are available under
[Common/python/configs](https://github.com/missirol/JMETriggerAnalysis/tree/run3/Common/python/configs).

 * [Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5_configDump.py](https://github.com/missirol/JMETriggerAnalysis/blob/run3/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5_configDump.py) :
   GRun HLT menu for `CMSSW_11_1_0_pre4`.
   ```shell
   hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V5 --full --offline --mc --unprescale --process HLT2 \
    --globaltag 110X_mcRun3_2021_realistic_Candidate_2020_05_26_16_08_15 \
    --max-events 10 \
    --input /store/mc/Run3Winter20DRPremixMiniAOD/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/40000/A623EE66-618D-FC43-B4FC-6C4029CD68FB.root \
    > ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5.py

   edmConfigDump \
      ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5.py \
    > ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5_configDump.py
   ```

 * [testing] [Common/python/configs/HLT_singleTrkIterWithPatatrack_v01.py](https://github.com/missirol/JMETriggerAnalysis/blob/run3/Common/python/configs/HLT_singleTrkIterWithPatatrack_v01.py) :
   HLT menu with single (global) tracking iteration seeded by Patatrack pixel tracks.

----------

### Configuration with JME trigger paths for testing

A standalone configuration file including
''MC trigger paths'' (i.e. no event selection)
with alternative HLT-Jet collections, e.g. PF-CHS Jets and Puppi Jets,
is available for testing under
[Common/python/configs/jetMCTriggers_configDump.py](https://github.com/missirol/JMETriggerAnalysis/tree/run3/Common/python/configs/jetMCTriggers_configDump.py).

----------

### Inputs for HLT Jet Energy Scale Corrections workflow

A standalone configuration file to create inputs
for the HLT Jet Energy Scale Corrections (JESC) derivation
can be found under
[Common/python/configs/hltRun3_rawJets_cfg.py](https://github.com/missirol/JMETriggerAnalysis/blob/run3/Common/python/configs/hltRun3_rawJets_cfg.py).

  * The configuration file runs on RAW (without 2-file solution),
    and creates an EDM file that contains
    only the products needed for
    the HLT-JESCs derivation
    (e.g. uncorrected jets).

  * **Example**: outputs can be produced as follows
    (parts in parentheses denote some of the optional command-line parameters).
    ```
    cmsRun hltRun3_rawJets_cfg.py [inputFiles=file:raw.root] [output=out.root] [globalTag=GT] [maxEvents=1]
    ```

----------

### Instructions for testing latest HLT menus on Run-2 data

This section contains a list of recipes to test
recent HLT menus on Run-2 data.
This set of instructions is preliminary;
although it heavily draws from tools developed by HLT experts,
this is in no way a set of recommendations by TSG.
The results of the workflow reported below are yet to be validated, so let the buyer beware.

 1. **2018 HLT menu (10_1_X)**:
    HLT configuration as used in Run-2 (2018).
    ```
    export SCRAM_ARCH=slc7_amd64_gcc700
    cmsrel CMSSW_10_1_10
    cd CMSSW_10_1_10/src
    cmsenv
    git cms-addpkg HLTrigger/Configuration
    git cherry-pick a179e5a4c48e8deecf436ac736806a291f9d8d60
    git cherry-pick 36ce09e79c043d39a478ef39e61b329723952ff7
    scram b
    hltGetConfiguration adg:/cdaq/physics/Run2018/2e34/v3.6.0/HLT/V4 \
     --full \
     --timing \
     --process HLT2 \
     --globaltag 101X_dataRun2_HLT_v7 \
     --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
     --max-events 1000 \
     --data \
     > hltOnRun2Data_101X_run323775_cfg.py
    ```

 1. **Run-3 HLT menus (11_1_X) to run on Run-2 data**:
      - Run-3 HLT menus with different customizations to be able to (1) run on Run-2 data, and (2) test modifications/improvements to the menu:
        1. current (default) HLT menu for Run-3 (in the 11_1_X release) customized to run on Run-2; 
        1. HLT menu for Run-3 (in the 11_1_X release), plus improvements for tracking being developed for Run-3
           (improved pixel tracks, from the Patatrack group, and single iteration for tracks used by PF);
        1. HLT menu for Run-3, plus improvements for tracking, and replacing PFMET with a preliminary version of PuppiMET for HLT.
    ```
    export SCRAM_ARCH=slc7_amd64_gcc820
    cmsrel CMSSW_11_1_0_Patatrack
    cd CMSSW_11_1_0_Patatrack/src
    git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3_devel
    cmsenv
    scram b

    # [1] HLT menu for Run-3, with minimal customizations to run on Run-2 data
    hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
     --full \
     --timing \
     --process HLT2 \
     --globaltag 101X_dataRun2_HLT_v9 \
     --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
     --customise \
    HLTrigger/Configuration/customizeHLTforCMSSW.synchronizeHCALHLTofflineRun3on2018data,\
    JMETriggerAnalysis/Common/customise_SiPixelClusterProducerForRun2.customise_SiPixelClusterProducerForRun2 \
     --max-events 1000 \
     --data \
     > hltOnRun2Data_112X_Run3_default_cfg.py

    # [2] HLT menu with improvements for tracking being developed for Run-3
    hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
     --full \
     --timing \
     --process HLT2 \
     --globaltag 101X_dataRun2_HLT_v9 \
     --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
     --customise \
     HLTrigger/Configuration/customizeHLTforPatatrack.customise_for_Patatrack_on_cpu,\
     JMETriggerAnalysis/Common/customise_hltTRK_singleIteration.customise_hltTRK_singleIteration,\
     HLTrigger/Configuration/customizeHLTforCMSSW.synchronizeHCALHLTofflineRun3on2018data,\
     JMETriggerAnalysis/Common/customise_SiPixelClusterProducerForRun2.customise_SiPixelClusterProducerForRun2 \
     --max-events 1000 \
     --data \
     > hltOnRun2Data_112X_Run3_newTRK_cfg.py

    # [3] HLT menu with improvements for tracking being developed for Run-3,
    #     plus replacing PFMET *in every HLT path* with a preliminary version of PuppiMET for HLT (yet to be retuned)
    hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 \
     --full \
     --offline \
     --timing \
     --process HLT2 \
     --globaltag 101X_dataRun2_HLT_v9 \
     --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
     --customise \
     HLTrigger/Configuration/customizeHLTforPatatrack.customise_for_Patatrack_on_cpu,\
     JMETriggerAnalysis/Common/customise_hltTRK_singleIteration.customise_hltTRK_singleIteration,\
     HLTrigger/Configuration/customizeHLTforCMSSW.synchronizeHCALHLTofflineRun3on2018data,\
     JMETriggerAnalysis/Common/customise_SiPixelClusterProducerForRun2.customise_SiPixelClusterProducerForRun2,\
     JMETriggerAnalysis/Common/customise_hlt_MET.customise_replacePFMETWithPuppiMETBasedOnPatatrackPixelVertices \
     --max-events 1000 \
     --data \
     > hltOnRun2Data_112X_Run3_newTRK_hltPuppiMET_cfg.py
    ```

----------

### Miscellanea

 * [SWGuideGlobalHLT TWiki: Instructions for `CMSSW_11_1_X`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Using_CMSSW_10_6_or_CMSSW_11_0_o)

 * DAS query for Run-3 MC samples (RAW):
   ```
   dasgoclient --query="dataset dataset=/*/Run3Winter20*/*RAW*"
   ```

----------
