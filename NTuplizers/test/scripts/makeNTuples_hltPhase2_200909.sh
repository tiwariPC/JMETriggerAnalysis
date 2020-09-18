#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=-1

ODIR=$1

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

if [ $(ls .tmp_*_cfg.py 2> /dev/null | wc -l) -gt 0 ]; then
  printf "%s\n%s\n" "target configuration files already exist:" "$(ls .tmp_*_cfg.py)"
  exit 1
fi

declare -A samplesMap
samplesMap["Phase2HLTTDR_MinBias_14TeV_PU200"]="/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"
##samplesMap["Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_castor_all_pt_tracks_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
##samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"

recoKeys=(
#  HLT_TRKv00
#  HLT_TRKv00_TICL
#  HLT_TRKv02
#  HLT_TRKv02_TICL
  HLT_TRKv06
#  HLT_TRKv06_TICL
#  HLT_TRKv06_skimmedTracks
#  HLT_TRKv06_TICL_skimmedTracks
)

JDIR=${1}_json

mkdir -p ${JDIR}

for sample_key in ${!samplesMap[@]}; do
  sample_name=${samplesMap[${sample_key}]}

  [ -f ${JDIR}/${sample_key}.json ] || (das_jsondump -v -m ${NEVT} -d ${sample_name} -o ${JDIR}/${sample_key}.json -p 0)

  # lxplus: specify JobFlavour and AccountingGroup
  [[ ${HOSTNAME} != lxplus* ]] || opts="--JobFlavour longlunch --AccountingGroup group_u_CMS.CAF.PHYS --no-export-LD-LIBRARY-PATH"

  for reco_key in "${recoKeys[@]}"; do
    [ -f .tmp_${reco_key}_cfg.py ] || (python jmeTriggerNTuple_cfg.py dumpPython=.tmp_${reco_key}_cfg.py numThreads=1 reco=${reco_key} trkdqm=0 pfdqm=0 globalTag=111X_mcRun4_realistic_T15_v2)

    htc_driver -c .tmp_${reco_key}_cfg.py --customize-cfg -m ${NEVT} -n 100 --cpus 1 --memory 2000 --runtime 10800 ${opts} \
      -d ${JDIR}/${sample_key}.json -p 0 -o ${ODIR}/${reco_key}/${sample_key}
  done
  unset reco_key sample_name
done
unset sample_key NEVT ODIR JDIR recoKeys samplesMap

rm -f .tmp_*_cfg.py
