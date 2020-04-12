#!/bin/bash

renametrk(){
  sed -i "s|hltPhase2$1|$2|" ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/hltPhase2_TRKv06.py
}

renametrk A a
renametrk P p
renametrk N n
renametrk I i
renametrk F f
renametrk G g
renametrk U u
renametrk T t
renametrk O o
renametrk V v
renametrk H h

unset -v renametrk
