#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "specify path to output directory"
  exit 1
fi

IDIR=out_das_jsondumps
ODIR=$1

DATASETS=(
 QCD_Pt_15to3000_Flat_14TeV_NoPU
 QCD_Pt_15to3000_Flat_14TeV_PU140
 QCD_Pt_15to3000_Flat_14TeV_PU200

 TT_14TeV_NoPU
 TT_14TeV_PU140
 TT_14TeV_PU200

 VBF_HToInvisible_M125_14TeV_NoPU
 VBF_HToInvisible_M125_14TeV_PU140
 VBF_HToInvisible_M125_14TeV_PU200
)

EXE="htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 2000 --runtime 1800"

for dset in "${DATASETS[@]}"; do

  if [ ! -f ${IDIR}/${dset}.json ]; then
    echo "input file does not exist: ${IDIR}/${dset}.json"
    exit 1
  fi

  if [ -d ${ODIR}/${dset} ]; then
    echo "output directory already exists: ${ODIR}/${dset}"
    exit 1

  elif [ ! -d ${ODIR} ]; then
    mkdir -p ${ODIR}
  fi

  ${EXE} -d ${IDIR}/${dset}.json -o ${ODIR}/${dset}

done
unset -v dset

unset -v IDIR ODIR DATASETS EXE
