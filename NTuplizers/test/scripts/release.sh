#!/bin/bash

for ddd in {0..100}; do
  sleep 1200
  condor_release ${USER}
done
unset -v ddd
