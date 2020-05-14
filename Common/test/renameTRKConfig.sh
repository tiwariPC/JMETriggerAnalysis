#!/bin/bash

set -e

trkFile=""
showHelpMsg=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--file) trkFile=$2; shift; shift;;
    -h|--help) showHelpMsg=true; shift;;
    *) shift;;
  esac
done

if [ ${showHelpMsg} == true ]; then

  cat <<@EOF
Usage: renameTRKConfig.sh -f <file>

Description:
  revert renaming applied to TRK-related modules (modifies the input file by removing the prefix "hltPhase2" from all modules)
@EOF

  exit 0
fi

if [ ! -f "${trkFile}" ]; then
  printf "%s\n" "invalid path to TRK configuration file [-f]: ${trkFile}"
  exit 1
fi

trkFile=$(readlink -f ${trkFile})

for firstLet in {a..z}; do
  sed -i "s|hltPhase2${firstLet^^}|${firstLet}|g" ${trkFile}
done
unset -v firstLet

unset -v trkFile showHelpMsg
