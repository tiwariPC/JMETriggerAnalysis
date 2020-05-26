### Tools for JME studies on the Phase-2 HLT reconstruction

* [Setup](#setup)
* [Instructions to generate configuration files for HLT Phase-2 reconstruction](#instructions-to-generate-configuration-files-for-hlt-phase-2-reconstruction)
* [Inputs for HLT Jet Energy Scale Corrections workflow](#inputs-for-hlt-jet-energy-scale-corrections-workflow)
* [Additional Notes](#additional-notes)

----------

### Setup
```shell
cmsrel CMSSW_11_1_0_pre6
cd CMSSW_11_1_0_pre6/src
cmsenv

# [HGCal] fix to PID+EnergyRegression in TICL
git cms-merge-topic cms-sw:29799

# workaround for PFSimParticle::trackerSurfaceMomentum
# ref: hatakeyamak:FBaseSimEvent_ProtectAgainstMissingTrackerSurfaceMomentum
git cms-addpkg FastSimulation/Event
git remote add hatakeyamak https://github.com/hatakeyamak/cmssw.git
git fetch hatakeyamak
git cherry-pick 0cf67551731c80dc85130e4b8ec73c8f44d53cb0

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b
```

----------

### Instructions to generate configuration files for HLT Phase-2 reconstruction

Configuration files are created via `cmsDriver.py`,
adding (HLT) customizations to the Phase-2 Offline reconstruction;
for an example of a `cmsDriver.py` for the Offline reconstruction (RECO step)
can be found from the setup commands of a AOD/MINIAOD sample in McM
([example](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/TSG-Phase2HLTTDRWinter20RECOMiniAOD-00010)).

 * Customization functions are available under
   [`Common/python/`](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python):

   - [**TRKv00**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv00.py#L3),
     [**TRKv02**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv02.py#L3),
     [**TRKv06**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv06.py#L3):
     customizations extracted from standalone configs developed by the TRK POG;
     guidelines to create such a customization function
     from a standalone `trackingOnly` configuration can be found in
     [Common/test/makeTRKCustomizationFunction.md](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/test/makeTRKCustomizationFunction.md).

   - [**''skimmed tracks''**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_skimmedTracks.py#L3):
     an addon to the standard TRK sequence,
     to select a subset of tracks based on their compatibility
     with the leading pixel vertices.
     If using one of the TRK customization functions,
     apply the ''skimmed tracks'' customization only after the TRK customization function;
     this function can be applied after any of TRK customization functions.

   - [**JME**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_JME.py#L13):
     customizations to build HLT-like Jets and MET collections;
     currently, the JME function also includes the backbone of
     the reconstruction sequence (largely taken from the `RECO` step),
     incl. some HLT-like modifications to the ParticleFlow modules.

   - [**TICL**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_JME.py#L885):
     a wrapper to apply the customization function maintained
     by HGCal to include TICL in the reconstruction;
     apply this customization only after the JME customization function.

 * A set of configuration files for different TRK (v0, v2, v6) and HGCal (with, or without, TICL) inputs can be found in
   [Common/python/configs/hltPhase2_*_cfg.py](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python/configs).

 * **Example**: configuration file to run TRK(v06)+TICL+JME HLT-like reconstruction on RAW.
   ```shell
   cmsDriver.py step3 \
     --geometry Extended2026D49 --era Phase2C9 \
     --conditions auto:phase2_realistic_T15 \
     --processName RECO2 \
     --step RAW2DIGI,RECO \
     --eventcontent RECO \
     --datatier RECO \
     --filein /store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/05BFAD3E-3F91-1843-ABA2-2040324C7567.root \
     --mc \
     --nThreads 4 \
     --nStreams 4 \
     --no_exec \
     -n 10 \
     --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
     --customise JMETriggerAnalysis/Common/hltPhase2_TRKv06.customize_hltPhase2_TRKv06 \
     --customise JMETriggerAnalysis/Common/hltPhase2_JME.customize_hltPhase2_JME \
     --customise JMETriggerAnalysis/Common/hltPhase2_JME.customize_hltPhase2_TICL \
     --customise_commands 'process.schedule.remove(process.RECOoutput_step)\ndel process.RECOoutput\ndel process.RECOoutput_step\n' \
     --python_filename hltPhase2_TRKv06_TICL_cfg.py
   ```

----------

### Inputs for HLT Jet Energy Scale Corrections workflow

A standalone configuration file to create inputs
for the HLT Jet Energy Scale Corrections (JESC) derivation
can be found under
[Common/python/configs/hltPhase2_rawJets_cfg.py](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/configs/hltPhase2_rawJets_cfg.py).

  * The configuration file loads the latest baseline reconstruction sequence
    (usually, as defined in one of the files in
    [Common/python/configs/hltPhase2_*_cfg.py](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python/configs)

  * It runs on RAW (without 2-file solution),
    and creates an EDM file that contains
    only the products needed for
    the HLT-JESCs derivation
    (e.g. uncorrected jets).

  * **Example**: outputs can be produced as follows
    (parts in parentheses denote some of the optional command-line parameters).
    ```
    cmsRun hltPhase2_rawJets_cfg.py [inputFiles=file:raw.root] [output=out.root] [globalTag=TheGT] [maxEvents=1]
    ```

----------

### Additional Notes

 * [HLT Phase-2 Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HighLevelTriggerPhase2)

 * DAS query for the latest Phase-2 MC samples (RAW):
   ```shell
   dasgoclient --query="dataset dataset=/*/Phase2HLTTDRWinter20*/*RAW*"
   ```

----------
