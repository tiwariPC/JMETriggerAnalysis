#!/bin/bash

set -e

IDIR1=tmp/output_oldGT/QCD_Pt-15to7000_Flat2018
IDIR2=tmp/output_newGT/QCD_Pt-15to7000_Flat2018
ODIR=tmpout

python -B ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/check_hltJECs/histosFromTree_AK4PF.py ${IDIR1} 1
python -B ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/check_hltJECs/histosFromTree_AK4PF.py ${IDIR2} 1

rm -rf ${ODIR}

${CMSSW_BASE}/src/NTupleAnalysis/JMETrigger/test/compareHistos.py \
  -i ${IDIR1}.root:'Before Fix (2016 HLT-JECs)':1 \
     ${IDIR2}.root:'After Fix (2017 HLT-JECs)':2 \
  -l '[102X, 2018, Pre-Legacy] QCD_Pt15-7000_Flat' \
  -o ${ODIR} \
  -e pdf root \
  -k None

unset IDIR1 IDIR2 ODIR
