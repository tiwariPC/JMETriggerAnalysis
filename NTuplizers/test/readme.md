### Instructions to generate configuration file(s) for HLT Phase-2 reconstruction:

* [Step #1] create local CMSSW area and add relevant packages:
```
cmsrel CMSSW_11_1_0_pre3
cd CMSSW_11_1_0_pre3/src
cmsenv

# [optional] PR#28976
git cms-addpkg RecoParticleFlow/PFClusterProducer
git cherry-pick 445d74b1df707d06a208d5f1a95b8492fc187239
git cherry-pick e68e48a95b4d20a9904d35b94dc4772b4298b135

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2_devel
scram b
```

* [Step #2] generate configuration file to run on RAW files:
```
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
  --python_filename hltPhase2_cfg.py \
  --no_exec \
  -n 10 \
  --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
  --customise JMETriggerAnalysis/Common/hltPhase2_JME.customize_hltPhase2_JME \
  --customise_commands 'process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.endjob_step)\ndel process.RECOoutput\ndel process.RECOoutput_step\n'
```

### Useful Links

TWiki: `https://twiki.cern.ch/twiki/bin/viewauth/CMS/HighLevelTriggerPhase2#MC_samples`
