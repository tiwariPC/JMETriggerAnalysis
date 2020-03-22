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

JDIR=${1}_json

if [ ! -d ${JDIR} ]; then

  mkdir -p ${JDIR}

  das_jsondump -v \
   -d /RelValQCD_Pt15To7000_Flat_14TeV/CMSSW_11_0_0-PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v1/MINIAODSIM \
   -o ${JDIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.json
fi

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d ${JDIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.json -p 1 \
 -o ${ODIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3

htc_driver -c jmeTriggerNTuple_cfg.py -n 100 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
 -d ${JDIR}/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.json -p 1 \
 -o ${ODIR}_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200 \
 -m ${NEVT} \
 pfdqm=1 trkdqm=1 reco=${TRKV}_110X_D49 gt=110X_mcRun4_realistic_v3 skimTracks=1

unset -v NEVT TRKV ODIR JDIR
