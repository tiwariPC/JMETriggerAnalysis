#!/bin/bash

set -e

trkDump=""
psetName=""
showHelpMsg=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--file) trkDump=$2; shift; shift;;
    -p|--pset) psetName=$2; shift; shift;;
    -h|--help) showHelpMsg=true; shift;;
    *) shift;;
  esac
done

if [ ${showHelpMsg} == true ]; then

  cat <<@EOF
Usage: makeTRKCustomizationFunction.sh -f <config file> -l <name of cms.Path/Task/Sequence>

Description:
  create a customization function for TRK, isolating changing with respect to the Offline reconstruction (RECO step)
@EOF

  exit 0
fi

if [ ! -f "${trkDump}" ]; then
  printf "%s\n" "invalid path to TRK configuration file [-f]: ${trkDump}"
  exit 1
fi

if [ "${psetName}" == "" ]; then
  printf "%s\n" "name of cms.Path/Task/Sequence not specified [-p]"
  exit 1
fi

if [ -d tmp ]; then
  printf "%s\n" "target tmp/ directory already exists"
  exit 1
fi

printf "%s\n" "Path/Task/Sequence: \"${psetName}\""

trkDump=$(readlink -f $trkDump)

mkdir tmp
cd tmp

cmsDriver.py step3 \
  --geometry Extended2026D49 --era Phase2C9 \
  --conditions auto:phase2_realistic_T15 \
  --processName RECO2 \
  --step RAW2DIGI,RECO \
  --eventcontent RECO \
  --datatier RECO \
  --filein /store/mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/05BFAD3E-3F91-1843-ABA2-2040324C7567.root \
  --mc \
  --nThreads 4 \
  --nStreams 4 \
  --no_exec \
  -n 10 \
  --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
  --python_filename offline_cfg.py

edmConfigDump offline_cfg.py > offline_configDump.py

cp ${trkDump} trk_configDump.py

for firstLet in {a..z}; do
  sed -i "s|hltPhase2${firstLet^^}|${firstLet}|g" trk_configDump.py
done
unset -v firstLet

diffCmd="edmDiffModulesOfSequence -r offline_configDump.py -t trk_configDump.py -s ${psetName} -d -e -p process. -k TrackProducer -i GlobalTag es_hardcode mix"

${diffCmd} > diff.py
${diffCmd} -n

unset -v diffCmd trkDump psetName showHelpMsg
