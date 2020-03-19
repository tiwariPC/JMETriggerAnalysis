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
hltGetConfiguration /dev/CMSSW_11_1_0/GRun --full --offline --mc --unprescale --process HLT2 --globaltag auto:run3_mc_GRun > \
  ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/python/HLT_dev_CMSSW_11_1_0_GRun.py
```

----

### Links

 * Instructions for `11_1_X`: `https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Using_CMSSW_10_6_or_CMSSW_11_0_o`
