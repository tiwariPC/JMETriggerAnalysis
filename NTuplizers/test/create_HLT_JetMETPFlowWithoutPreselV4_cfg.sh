#!/bin/bash

printf "\n%s\n\n" " >>> cff of simplified HLT Menu to run unbiased PF@HLT"
hltGetConfiguration --cff --unprescale --paths HLTriggerFirstPath,HLTriggerFinalPath /dev/CMSSW_10_6_0/GRun > HLT_JetMETPFlowWithoutPreselV4_cff.py
hltGetConfiguration --cff --unprescale --globaltag auto:run2_hlt_GRun /users/missirol/testing/2018/JMEPFlow/JetMETPFlowWithoutPresel/V4 >> HLT_JetMETPFlowWithoutPreselV4_cff.py

# comment duplicates of "import FWCore.ParameterSet.Config as cms" and "fragment = cms.ProcessFragment"
sed -i -e 's|import FWCore.ParameterSet.Config as cms|#import FWCore.ParameterSet.Config as cms|g' \
       -e '0,/#import FWCore.ParameterSet.Config as cms/{s/#import FWCore.ParameterSet.Config as cms/import FWCore.ParameterSet.Config as cms/}' \
       -e 's|fragment = cms.ProcessFragment|#fragment = cms.ProcessFragment|g' \
       -e '0,/#fragment = cms.ProcessFragment/{s/#fragment = cms.ProcessFragment/fragment = cms.ProcessFragment/}' \
 HLT_JetMETPFlowWithoutPreselV4_cff.py

printf "\n%s\n\n" " >>> copy HLT-cff to HLTrigger/Configuration/python/ to access it via cmsDriver.py"
cp HLT_JetMETPFlowWithoutPreselV4_cff.py ${CMSSW_BASE}/src/HLTrigger/Configuration/python

printf "\n%s\n\n" " >>> cfg file to re-run HLT menu on RAW Data"
cmsDriver.py HLT2 \
 --processName HLT2 \
 -n 100 --no_exec \
 --python_filename HLT_JetMETPFlowWithoutPreselV4_cfg.py \
 --step HLT:JetMETPFlowWithoutPreselV4 \
 --era Run2_2018 --data \
 --conditions auto:run2_hlt_GRun \
 --filein root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/110000/12952201-BFB3-4142-B24C-983B753A4300.root \
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
