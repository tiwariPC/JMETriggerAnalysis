#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#
scramv1 project CMSSW CMSSW_11_1_2_patch3
cd CMSSW_11_1_2_patch3/src
eval `scramv1 runtime -sh`

# updates to use l1t::PFJet with HLT plugins
git cms-merge-topic missirol:devel_hltPhase2_l1tPFJet_1112pa3 -u

# updates to Puppi (required only for TRK-vX, with X>=7.2)
git cms-merge-topic missirol:devel_hltPhase2_puppi_usePUProxyValue_1112pa3 -u

# [optional; required only for PF-Hadron calibrations]
# workaround for PFSimParticle::trackerSurfaceMomentum
# ref: hatakeyamak:FBaseSimEvent_ProtectAgainstMissingTrackerSurfaceMomentum
git cms-addpkg FastSimulation/Event
git remote add hatakeyamak https://github.com/hatakeyamak/cmssw.git
git fetch hatakeyamak
git diff 0cf67551731c80dc85130e4b8ec73c8f44d53cb0^ 0cf67551731c80dc85130e4b8ec73c8f44d53cb0 | git apply

# [optional; required only for JME-Trigger NTuple]
# selected manual backport of BadPFMuonDz MET-filter
# https://github.com/cms-sw/cmssw/pull/30015
git cms-addpkg RecoMET/METFilters
git diff 442ae0775276f4388f8d51742ea915c1b91e1506 bb38311862c83068b2434f35850c9a17e29dd2f7 RecoMET/METFilters/python | git apply
git checkout bb38311862c83068b2434f35850c9a17e29dd2f7 RecoMET/METFilters/plugins/BadParticleFilter.cc

# [optional; required only for JME-Trigger NTuple workflow with 'pvdqm > 1']
# analyzer for primary vertices (courtesy of W. Erdmann)
git clone https://github.com/missirol/PVAnalysis.git usercode -o missirol -b phase2
