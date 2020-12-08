#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=20000

ODIR=$1

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

declare -A samplesMap
#samplesMap["Phase2HLTTDR_MinBias_14TeV_PU200"]="/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"
samplesMap["Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_NoPU"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_castor_all_pt_tracks_111X_mcRun4_realistic_T15_v1-v1/FEVT"
samplesMap["Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
samplesMap["Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_QCD_Pt020to030_14TeV_PU200"]="/QCD_Pt_20to30_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1-v2/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt030to050_14TeV_PU200"]="/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt050to080_14TeV_PU200"]="/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt080to120_14TeV_PU200"]="/QCD_Pt_80to120_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt120to170_14TeV_PU200"]="/QCD_Pt_120to170_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt170to300_14TeV_PU200"]="/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt300to470_14TeV_PU200"]="/QCD_Pt_300to470_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt470to600_14TeV_PU200"]="/QCD_Pt_470to600_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_QCD_Pt600toInf_14TeV_PU200"]="/QCD_Pt_600oInf_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_WJetsToLNu_14TeV_PU200"]="/WJetsToLNu_TuneCP5_14TeV-amcatnloFXFX-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_DYJetsToLL_M010to050_14TeV_PU200"]="/DYJetsToLL_M-10to50_TuneCP5_14TeV-madgraphMLM-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"
#samplesMap["Phase2HLTTDR_DYJetsToLL_M050toInf_14TeV_PU200"]="/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT"

recoKeys=(
#  HLT_TRKv00
#  HLT_TRKv00_TICL
#  HLT_TRKv02
#  HLT_TRKv02_TICL
#  HLT_TRKv06
#  HLT_TRKv06_TICL
#  HLT_TRKv06p1
  HLT_TRKv06p1_TICL
#  HLT_TRKv06p3
#  HLT_TRKv06p3_TICL
#  HLT_TRKv07p2
#  HLT_TRKv07p2_TICL
)

for sampleKey in ${!samplesMap[@]}; do
  sampleName=${samplesMap[${sampleKey}]}

  # options (JobFlavour and AccountingGroup)
  opts=""
  if [[ ${HOSTNAME} == lxplus* ]]; then
    opts+="--JobFlavour longlunch"
    if [[ ${USER} == missirol ]]; then
      opts+=" --AccountingGroup group_u_CMS.CAF.PHYS"
    fi
  fi

  for recoKey in "${recoKeys[@]}"; do
    python jmeTriggerNTuple_cfg.py dumpPython=/tmp/${USER}/${recoKey}_cfg.py numThreads=1 reco=${recoKey} trkdqm=1 pvdqm=1 pfdqm=1 globalTag=111X_mcRun4_realistic_T15_v2

    htc_driver -c /tmp/${USER}/${recoKey}_cfg.py --customize-cfg -m ${NEVT} -n 200 --cpus 1 --memory 2000 --runtime 10800 ${opts} \
      -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/${sampleKey}
  done
  unset recoKey sampleName opts
done
unset sampleKey NEVT ODIR recoKeys samplesMap
