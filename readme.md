
* Golden JSON for 2018 (PromptReco):

/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt

* Golden JSON for 2018 (ABC-ReReco + D-PromptReco):

/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt

* Input Samples:

  - Data:

dasgoclient --query="file dataset=/SingleMuon/Run2018D-v1/RAW"
  process HLT (release CMSSW_10_1_10)
     HLT menu:   '/cdaq/physics/Run2018/2e34/v3.6.1/HLT/V2'
     global tag: '101X_dataRun2_HLT_v7'

dasgoclient --query="file dataset=/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD"

 hltInfo root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/110000/12952201-BFB3-4142-B24C-983B753A4300.root

  - MC (special TSG samples in 10_2_X): dasgoclient --query="dataset dataset=/*/*102X_upgrade2018_realistic_v15*/GEN-SIM-RAW"



Collections:
 hltParticleFlow
 hltAK4PFJets
 hltPFMet
 hltPFMETTypeOne




# set up CMSSW area
cmsrel CMSSW_10_2_17
cd CMSSW_10_2_17/src
cmsenv
git cms-addpkg HLTrigger/Configuration
scram b

# set up VOMS proxy
voms-proxy-init --voms cms

# cff of simplified HLT Menu to run unbiased PF@HLT
hltGetConfiguration --unprescale --cff --globaltag auto:run2_hlt_GRun /users/mdjordje/10_1_8/PFJetMETDummyStripped/V6 > HLT_PFJetMETDummyStripped_cff.py

# copy HLT-cff to HLTrigger/Configuration/python/ to access it via cmsDriver.py
cp HLT_PFJetMETDummyStripped_cff.py ${CMSSW_BASE}/src/HLTrigger/Configuration/python

# cfg file to re-run HLT menu on RAW Data
cmsDriver.py HLT2 --step=HLT:PFJetMETDummyStripped \
  --era=Run2_2018 --data \
  --conditions auto:run2_hlt_GRun \
  --filein root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/110000/12952201-BFB3-4142-B24C-983B753A4300.root
  --secondfilein \
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/457/00000/32D606CE-8AA3-E811-8205-02163E01A154.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/457/00000/CABE78CC-8AA3-E811-9A4F-FA163E5E460D.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/457/00000/E8902496-89A3-E811-B163-FA163EE76E1A.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/457/00000/F868B307-AAA4-E811-8749-FA163EBD89BA.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/917/00000/701A552E-57AB-E811-ADC9-FA163E249C0F.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/917/00000/C4E7B52E-57AB-E811-A067-FA163E69B278.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/917/00000/C62DBD70-57AB-E811-82C1-FA163E79726F.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/321/917/00000/EEF4242E-57AB-E811-BEA7-FA163E516F48.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/322/348/00000/002342F6-DFB1-E811-9B7A-FA163E943E70.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/322/348/00000/620452F8-DFB1-E811-BD44-FA163EEAACDE.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/322/348/00000/7665824C-E1B1-E811-8D0B-FA163E78EE04.root,\
root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/RAW/v1/000/322/348/00000/D2198A48-E1B1-E811-8446-FA163E3EA47F.root
