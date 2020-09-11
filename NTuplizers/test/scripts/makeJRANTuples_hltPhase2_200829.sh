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

declare -A samplesMap
samplesMap["Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20DIGI-PU200_castor_110X_mcRun4_realistic_v3-v2/GEN-SIM-DIGI-RAW"

recoKeys=(
# HLT_TRKv06
  HLT_TRKv06_TICL
)

JDIR=${1}_json

mkdir -p ${JDIR}

for sample_key in ${!samplesMap[@]}; do
  sample_name=${samplesMap[${sample_key}]}

  if [ ! -f ${JDIR}/${sample_key}.json ]; then
    das_jsondump -v -m ${NEVT} -d ${sample_name} -o ${JDIR}/${sample_key}.json -p 0
  fi

  for reco_key in "${recoKeys[@]}"; do
    htc_driver -c hltJRA_mcRun4_cfg.py -n 100 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
      -d ${JDIR}/${sample_key}.json -p 0 \
      -o ${ODIR}/${reco_key}/${sample_key} \
      -m ${NEVT} reco=${reco_key} trkdqm=1 pfdqm=1
  done
  unset -v reco_key
  unset -v sample_name
done
unset -v sample_key

unset NEVT ODIR JDIR
unset recoKeys samplesMap
