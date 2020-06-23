#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#
scram project CMSSW_11_1_0_pre6
cd CMSSW_11_1_0_pre6/src
eval `scram runtime -sh`

# [HGCal] fix to PID+EnergyRegression in TICL
git cms-merge-topic cms-sw:29799

# workaround for PFSimParticle::trackerSurfaceMomentum
# ref: hatakeyamak:FBaseSimEvent_ProtectAgainstMissingTrackerSurfaceMomentum
git cms-addpkg FastSimulation/Event
git remote add hatakeyamak https://github.com/hatakeyamak/cmssw.git
git fetch hatakeyamak
git cherry-pick 0cf67551731c80dc85130e4b8ec73c8f44d53cb0

# [L1T]
git cms-merge-topic -u cms-L1TK:L1TK-integration-CMSSW_11_1_0_pre4
git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v3.0.2
