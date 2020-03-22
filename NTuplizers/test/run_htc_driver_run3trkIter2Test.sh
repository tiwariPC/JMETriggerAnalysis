#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "%s\n" ">>> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

ODIR=$1

JDIR=${1}_json

if [ ! -d ${JDIR} ]; then

  mkdir -p ${JDIR}

  das_jsondump -v \
   -d /QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${JDIR}/Run3Winter20_QCD_Pt_170to300_14TeV.json
fi

recos=(
 HLT
 HLT_trkIter2RegionalPtSeed0p9
 HLT_trkIter2RegionalPtSeed2p0
 HLT_trkIter2RegionalPtSeed5p0
 HLT_trkIter2RegionalPtSeed10p0
 HLT_trkIter2GlobalPtSeed0p9
)

for reco in "${recos[@]}"; do

  ODIR=$1/${reco}

  if [ -d ${ODIR} ]; then
    printf "%s\n" ">>> output directory already exists: ${ODIR}"
    continue
  fi

  htc_driver -c jmeTriggerNTuple_cfg.py -n 200 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${JDIR}/Run3Winter20_QCD_Pt_170to300_14TeV.json -p 0 \
   -o ${ODIR}/Run3Winter20_QCD_Pt_170to300_14TeV \
   -m ${NEVT} reco=${reco}

  unset -v ODIR

done
unset -v reco

unset -v NEVT JDIR
