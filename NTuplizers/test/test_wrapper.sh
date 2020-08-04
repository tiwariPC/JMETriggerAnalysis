#!/bin/bash

set -e

cd ${CMSSW_BASE}/src
git checkout from-${CMSSW_VERSION}
scram b &> /dev/null
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test
printf "%s\n" "--- REFE ---"
for nnn in {0..3}; do
  printf "%s\n" "old_${nnn}"
  ./test.sh 0 old_${nnn}.root &> old_${nnn}.txt
  grep -inr hltPFPuppi old_${nnn}.txt | grep FastReport
  rm old_${nnn}.root.txt
  printTTree -i old_${nnn}.root -o old_${nnn}.root.txt
done; unset nnn;

cd ${CMSSW_BASE}/src
#git checkout devel_puppi01_112X
#git checkout devel_puppi01_112X_float
git checkout devel_puppi01_112X_float_test2
#git checkout devel_puppi01_112X_idxs
scram b &> /dev/null
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test
printf "%s\n" "--- TARG ---"
for nnn in {0..3}; do
  printf "%s\n" "new_${nnn}"
  ./test.sh 0 new_${nnn}.root &> new_${nnn}.txt
  grep -inr hltPFPuppi new_${nnn}.txt | grep FastReport
  rm new_${nnn}.root.txt
  printTTree -i new_${nnn}.root -o new_${nnn}.root.txt
done; unset nnn;
