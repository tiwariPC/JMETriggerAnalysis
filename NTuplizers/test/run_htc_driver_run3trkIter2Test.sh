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
   -d /QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${JDIR}/Run3Winter20_QCD_Pt_170to300_14TeV.json
fi

recos=(
 HLT
 HLT_iter2RegionalPtSeed0p9
 HLT_iter2RegionalPtSeed2p0
 HLT_iter2RegionalPtSeed5p0
 HLT_iter2GlobalPtSeed0p9
)

for reco in "${recos[@]}"; do

  htc_driver -c jmeTriggerNTuple_cfg.py -n 200 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${JDIR}/Run3Winter20_QCD_Pt_170to300_14TeV.json -p 0 \
   -o ${ODIR}/${reco}/Run3Winter20_QCD_Pt_170to300_14TeV \
   -m ${NEVT} reco=${reco}

done
unset -v reco

unset -v NEVT ODIR JDIR
