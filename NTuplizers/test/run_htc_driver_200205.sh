#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  echo ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=1000

TRKV=trkV2

ODIR=$1/${TRKV}

if [ -d ${ODIR} ]; then
  echo "output directory already exists: ${ODIR}"
  return
fi

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19MiniAOD-NoPU_castor_106X_upgrade2023_realistic_v3-v2/MINIAODSIM \
 -o ${ODIR}/PhaseIITDRSpring19_QCD_Pt_15to3000_Flat_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19MiniAOD-PU200_castor_106X_upgrade2023_realistic_v3-v2/MINIAODSIM \
 -o ${ODIR}/PhaseIITDRSpring19_QCD_Pt_15to3000_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -o ${ODIR}/PhaseIITDRSpring19_TT_14TeV_NoPU \
 -d /TT_TuneCP5_14TeV-powheg-pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -o ${ODIR}/PhaseIITDRSpring19_TT_14TeV_PU200 \
 -d /TT_TuneCP5_14TeV-powheg-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM \
 -o ${ODIR}/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM \
 -o ${ODIR}/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D41

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValQCD_Pt15To7000_Flat_14TeV/CMSSW_11_0_0-110X_mcRun4_realistic_v2_2026D49noPU-v1/MINIAODSIM -p 1 \
 -o ${ODIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValQCD_Pt15To7000_Flat_14TeV/CMSSW_11_0_0-PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/MINIAODSIM -p 1 \
 -o ${ODIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValTTbar_14TeV/CMSSW_11_0_0-110X_mcRun4_realistic_v2_2026D49noPU-v2/MINIAODSIM -p 1 \
 -o ${ODIR}/RelVal1100_2026D49_TTbar_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValTTbar_14TeV/CMSSW_11_0_0-PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/MINIAODSIM -p 1 \
 -o ${ODIR}/RelVal1100_2026D49_TTbar_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValQCD_Pt15To7000_Flat_14TeV/CMSSW_11_0_0-110X_mcRun4_realistic_v2_2026D49noPU-v1/MINIAODSIM -p 1 \
 -o ${ODIR}_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 skimTracks=1

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValQCD_Pt15To7000_Flat_14TeV/CMSSW_11_0_0-PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/MINIAODSIM -p 1 \
 -o ${ODIR}_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3 skimTracks=1

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValTTbar_14TeV/CMSSW_11_0_0-110X_mcRun4_realistic_v2_2026D49noPU-v2/MINIAODSIM -p 1 \
 -o ${ODIR}_skimmedTracks/RelVal1100_2026D49_TTbar_14TeV_NoPU \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 skimTracks=1

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d /RelValTTbar_14TeV/CMSSW_11_0_0-PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/MINIAODSIM -p 1 \
 -o ${ODIR}_skimmedTracks/RelVal1100_2026D49_TTbar_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3 skimTracks=1

unset -v NEVT TRKV ODIR
