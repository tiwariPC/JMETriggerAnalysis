#!/bin/bash

set -e

hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V11 --globaltag 111X_mcRun3_2021_realistic_v8 --mc --full --offline --unprescale \
 > ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V11.py

edmConfigDump \
 ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V11.py > \
 ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V11_configDump.py

rm -f ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_11_1_0_GRun_V11.py
