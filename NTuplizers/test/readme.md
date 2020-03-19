### Instructions to generate configuration file(s) for HLT Run-3 reconstruction:

----

* **Step #1** : create local CMSSW area and add the relevant packages.
```
cmsrel CMSSW_11_1_0_pre4
cd CMSSW_11_1_0_pre4/src
cmsenv

git cms-addpkg HLTrigger/Configuration
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
scram b
```

----

* **Step #2** : 
```
hltGetConfiguration /dev/CMSSW_11_1_0/GRun --full --offline --mc --unprescale --process HLT2 \
 --globaltag auto:phase1_2021_realistic \
 --max-events 10 \
 --input /store/mc/Run3Winter20DRPremixMiniAOD/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/40000/A623EE66-618D-FC43-B4FC-6C4029CD68FB.root \
 > ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/python/HLT_dev_CMSSW_11_1_0_GRun.py

edmConfigDump \
   ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/python/HLT_dev_CMSSW_11_1_0_GRun.py \
 > ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/python/HLT_dev_CMSSW_11_1_0_GRun_configDump.py
```

----

### Links

 * Instructions for `11_1_X`: `https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Using_CMSSW_10_6_or_CMSSW_11_0_o`
