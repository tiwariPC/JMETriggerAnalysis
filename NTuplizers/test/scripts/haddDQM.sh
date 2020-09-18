
merge_dqm(){
  hadd -ff tmp_${1}.root output_hltPhase2_200909/HLT_TRKv06_TICL/Phase2HLTTDR_MinBias_14TeV_PU200/job_${1}*/DQM.root
  rm -f                  output_hltPhase2_200909/HLT_TRKv06_TICL/Phase2HLTTDR_MinBias_14TeV_PU200/job_${1}*/DQM.root
}

merge_dqm 11
merge_dqm 10
merge_dqm 09
merge_dqm 08
merge_dqm 07
merge_dqm 06
merge_dqm 05
merge_dqm 04
merge_dqm 03
merge_dqm 02
merge_dqm 01
