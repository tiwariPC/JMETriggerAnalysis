### Tools for JME studies on the Run-3 HLT reconstruction

* [Setup](#setup)
* [Configuration files for HLT Run-3 reconstruction](#configuration-files-for-hlt-run-3-reconstruction)
* [Configuration with JME trigger paths for testing](#configuration-with-jme-trigger-paths-for-testing)
* [Inputs for HLT Jet Energy Scale Corrections workflow](#inputs-for-hlt-jet-energy-scale-corrections-workflow)
* [Additional Notes](#additional-notes)

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

 * [Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5.py](https://github.com/missirol/JMETriggerAnalysis/blob/run3/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V5.py) :
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

### Notes

 * [SWGuideGlobalHLT TWiki: Instructions for `CMSSW_11_1_X`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Using_CMSSW_10_6_or_CMSSW_11_0_o)

 * DAS query for Run-3 MC samples (RAW):
   ```
   dasgoclient --query="dataset dataset=/*/Run3Winter20*/*RAW*"
   ```

----------
