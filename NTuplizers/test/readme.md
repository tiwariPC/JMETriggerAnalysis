
#### NTuple for PF-Hadron calibrations

```
cmsRun pfHadCalibNTuple_cfg.py maxEvents=1 output=tmp.root
```

Comments:

 * currently based on ``TRK-v6.1 + TICL''
   (reconstruction choice hard-coded in the `cfg` file);

 * the output `.root` file contains two TTrees, one for
   `particleFlowTmpBarrel` (named `pfHadCalibNTuplePFBarrel/Candidates`)
   and one for `pfTICL` (named `pfHadCalibNTuplePFTICL/Candidates`);

 * the selection of PF-ChargedHadrons is currently different for `particleFlowTmpBarrel` and `pfTICL`,
   due to the fact that the latter does not use the PFBlock algorithm;
   as a temporary solution for `pfTICL`, the workflow adopts the fix introduced in
   [cmssw#32202](https://github.com/cms-sw/cmssw/pull/32202).
