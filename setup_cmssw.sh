#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#

scramv1 project CMSSW_11_2_0_Patatrack
cd CMSSW_11_2_0_Patatrack/src
eval `scramv1 runtime -sh`

git cms-merge-topic missirol:devel_1120pa_kineParticleFilter -u
git cms-merge-topic missirol:devel_puppiPUProxy_1120patatrack -u
git cms-merge-topic mmasciov:tracking-allPVs -u

#git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
#
## Run-3 PFHC: copy preliminary HLT-PFHC for Run-3
#mkdir -p ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data
#cp /afs/cern.ch/user/c/chuh/public/PFCalibration/run3/PFCalibration.db ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db
