#!/bin/bash

if [ $# -ne 1 ]; then
  printf "%s\n" "specify if igprof shall be used [1/0]"
#  printf "%s\n" "specify if igprof shall be used [1/0] and the number of threads/streams [int]"
  exit 1
fi

IGPROF=${1}
NTHREADS=4 #${2}

EXE="cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:1E007C6B-0236-774C-AE76-16FF40129ED8.root secondaryInputFiles=None printSummaries=1 maxEvents=100 numThreads=${NTHREADS} numStreams=0 wantSummary=1"

if [ ${IGPROF} -ne 0 ]; then
  igprof -t cmsRun -pp -z -o igprof.jmeTriggerNTuple.pp.gz ${EXE}
  igprof-analyse -d -v -g igprof.jmeTriggerNTuple.pp.gz &> igprof.jmeTriggerNTuple.pp.txt
# igprof-analyse --sqlite -d -v -g igprof.jmeTriggerNTuple.pp.gz | sqlite3 igprof_analyse.jmeTriggerNTuple.pp.sql3
  rm igprof.jmeTriggerNTuple.pp.gz
else
  taskset -c 0-3 ${EXE}
fi
