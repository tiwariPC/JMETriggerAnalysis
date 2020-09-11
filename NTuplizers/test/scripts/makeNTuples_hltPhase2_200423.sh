#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

ODIR=$1

if [ -d ${ODIR} ]; then
  echo "output directory already exists: ${ODIR}"
  exit 1
fi

JDIR=${1}_json

if [ ! -d ${JDIR} ]; then

  mkdir -p ${JDIR}

  das_jsondump -v -m ${NEVT} \
   -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20RECOMiniAOD-NoPU_castor_all_pt_tracks_110X_mcRun4_realistic_v3-v2/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU.json

  das_jsondump -v -m ${NEVT} \
   -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20RECOMiniAOD-PU200_castor_110X_mcRun4_realistic_v3-v2/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.json

  das_jsondump -v -m ${NEVT} \
   -d /VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRWinter20RECOMiniAOD-NoPU_110X_mcRun4_realistic_v3-v2/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU.json

  das_jsondump -v -m ${NEVT} \
   -d /VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRWinter20RECOMiniAOD-PU200_110X_mcRun4_realistic_v3-v3/MINIAODSIM \
   -o ${JDIR}/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.json
fi

RECOS=(
  HLT_TRKv00
  HLT_TRKv00_TICL
#  HLT_TRKv02
#  HLT_TRKv02_TICL
  HLT_TRKv06
  HLT_TRKv06_TICL
)

SAMPLES=(
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
  Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)

for reco_i in "${RECOS[@]}"; do

  for sample_i in "${SAMPLES[@]}"; do

    htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
      -d ${JDIR}/${sample_i}.json -p 1 \
      -o ${ODIR}/${reco_i}/${sample_i} \
      -m ${NEVT} reco=${reco_i} globalTag=110X_mcRun4_realistic_v3 trkdqm=1 pfdqm=2
  done
  unset -v sample_i
done
unset -v reco_i

unset -v NEVT ODIR JDIR
unset -v RECOS SAMPLES
