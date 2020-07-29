#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  echo ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

ODIR=$1

if [ -d ${ODIR} ]; then
  echo "output directory already exists: ${ODIR}"
  return
fi

JDIR=${1}_json

if [ ! -d ${JDIR} ]; then

  mkdir -p ${JDIR}

  das_jsondump -v \
   -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20RECOMiniAOD-PU200_castor_110X_mcRun4_realistic_v3-v2/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_QCD_Pt_15to3000_TuneCP5_Flat_14TeV_PU200.json

  das_jsondump -v \
   -d /VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRWinter20RECOMiniAOD-PU200_110X_mcRun4_realistic_v3-v3/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_VBF_HToInvisible_M125_14TeV_PU200.json
fi

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d ${JDIR}/Phase2HLTTDR_QCD_Pt_15to3000_TuneCP5_Flat_14TeV_PU200.json -p 1 \
 -o ${ODIR}/Phase2HLTTDR_QCD_Pt_15to3000_TuneCP5_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d ${JDIR}/Phase2HLTTDR_VBF_HToInvisible_M125_14TeV_PU200.json -p 1 \
 -o ${ODIR}/Phase2HLTTDR_VBF_HToInvisible_M125_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1

unset -v NEVT ODIR JDIR
