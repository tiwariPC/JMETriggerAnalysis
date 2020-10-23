#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#
scramv1 project CMSSW CMSSW_11_1_4
cd CMSSW_11_1_4/src
eval `scramv1 runtime -sh`

# L1T
git cms-merge-topic cms-l1t-offline:l1t-phase2-v3.1.9

# HLT: interface for L1T seeds
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface

# HGCal
git cms-merge-topic rovere:TICLv2_11_1_X
cp -r ${CMSSW_DATA_PATH}/data-RecoHGCal-TICL/V00-01-00/RecoHGCal/TICL/data/ ${CMSSW_BASE}/src/RecoHGCal/TICL
cp /afs/cern.ch/work/m/missirol/public/phase2/HGCal/frozen_graph.pb ${CMSSW_BASE}/src/RecoHGCal/TICL/data/tf_models/energy_id_v0.pb

# JME: updates to Puppi (required only for TRK-vX, with X>=7.2)
git cms-merge-topic missirol:devel_hltPhase2_puppi_usePUProxyValue_1114

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
