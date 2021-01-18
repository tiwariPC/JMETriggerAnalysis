#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=1000000

ODIR=$1

if [ $# -eq 1 ]; then
  ODIR=${1}
  ODIR_cmsRun=${1}
else
  ODIR=${1}
  ODIR_cmsRun=${2}
fi

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

declare -A samplesMap
samplesMap["Phase2HLTTDR_QCD_PtFlat15to7000_14TeV_NoPU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20DIGI-NoPU_castor_110X_mcRun4_realistic_v3_ext1-v1/GEN-SIM-DIGI-RAW"
samplesMap["Phase2HLTTDR_QCD_PtFlat15to7000_14TeV_PU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRWinter20DIGI-FlatPU0To200_castor_110X_mcRun4_realistic_v3_ext1-v1/GEN-SIM-DIGI-RAW"
#samplesMap["Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"

recoKeys=(
#  HLT_TRKv00
#  HLT_TRKv00_TICL
#  HLT_TRKv02
#  HLT_TRKv02_TICL
#  HLT_TRKv06
#  HLT_TRKv06_TICL
  HLT_TRKv06p1
#  HLT_TRKv06p1_TICL
#  HLT_TRKv06p3
#  HLT_TRKv06p3_TICL
#  HLT_TRKv07p2
#  HLT_TRKv07p2_TICL
)

# options (JobFlavour and AccountingGroup)
opts=""
if [[ ${HOSTNAME} == lxplus* ]]; then
  opts+="--JobFlavour longlunch"
  if [[ ${USER} == missirol ]]; then
    opts+=" --AccountingGroup group_u_CMS.CAF.PHYS"
  fi
fi

for recoKey in "${recoKeys[@]}"; do
  python hltJRA_mcRun4_cfg.py dumpPython=/tmp/${USER}/${recoKey}_cfg.py numThreads=1 reco=${recoKey} #globalTag=111X_mcRun4_realistic_T15_v2

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}

    htc_driver -c /tmp/${USER}/${recoKey}_cfg.py --customize-cfg -m ${NEVT} -n 500 --cpus 1 --memory 2000 --runtime 10800 ${opts} \
      -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/${sampleKey} --cmsRun-output-dir ${ODIR_cmsRun}/${recoKey}/${sampleKey}

    unset sampleName
  done
  unset sampleKey
done
unset recoKey opts NEVT ODIR ODIR_cmsRun recoKeys samplesMap
