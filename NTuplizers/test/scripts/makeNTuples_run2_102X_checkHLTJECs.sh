#!/bin/bash

ODIR=tmp

if [ ! -d ${ODIR} ]; then

  mkdir ${ODIR}
  pushd ${ODIR}

  das_jsondump -p 0 -v -m 60000 \
   -d /QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v1/GEN-SIM-RAW \
   -o  QCD_Pt-15to7000_Flat2018.json

  htc_driver -c ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py -m 60000 -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d QCD_Pt-15to7000_Flat2018.json -p 0 \
   -o output_oldGT/QCD_Pt-15to7000_Flat2018 \
   reco=HLT_102X globalTag=102X_upgrade2018_realistic_v21

  htc_driver -c ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py -m 60000 -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d QCD_Pt-15to7000_Flat2018.json -p 0 \
   -o output_newGT/QCD_Pt-15to7000_Flat2018 \
   reco=HLT_102X globalTag=102X_upgrade2018_realistic_fixHltJec_v1

  popd
fi

unset ODIR
