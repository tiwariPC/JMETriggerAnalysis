#### Instructions to create a customization function from a standalone TRK configuration

* Open the TRK `cff` file that contains the definition of the TRK sequence (this will be referred to in the following as `MC_Tracking_vX_cff.py`);
  adjust the configuration in order to have the final track-reconstruction and vertex-reconstruction sequences inside the same `cms.Path`/`Task`/`Sequence`
  (this will be referred to in the following as `MC_Tracking_vX`).

* Create the full TRK configuration file by dumping the TRK `cfg` file via `edmConfigDump`
  (in what follows, this will be referred to as `TRKvX_configDump.py`).

* Execute
```
${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/makeTRKCustomizationFunction.sh \
-f TRKvX_configDump.py \
-p MC_Tracking_vX
```

* If this steps succeeds, its outputs can be found in a directory called `tmp`;
  this contains the input configuration files (for TRK and Offline),
  and the modules in `MC_Tracking_vX` that differ across the two files; the latter list of modules is in the file `tmp/diff.py`,
  and this constitutes the base of the final customization function.

* Edit `tmp/diff.py` to wrap the modules inside a customization function
  - add `import FWCore.ParameterSet.Config as cms` as the first line of the file;
  - add the function definition using `process` as the only function argument, e.g. `def customize_TRKvX(process):`;
  - indent all the modules;
  - add the statement `return process` at the end of the function.

* Go back to the file `MC_Tracking_vX_cff.py`, copy all the sequences relevant to track and vertex reconstruction,
  and add them at the bottom of the customization function in `tmp/diff.py` (before the `return` statement);
  if needed, revert the renaming of the modules inside said sequences;
  for the final object that combines all the (sub-)sequences relevant to track	and vertex reconstruction
  use a `cms.Sequence` named `process.globalreco_tracking`
  (i.e. the name of the TRK reconstruction sequence in the Offline reconstruction).

* **Note**: since we are currently using sequences instead of tasks,
  some modifications (usually, additions) might need to be made inside the TRK sequences
  in order to respect the modules' dependencies; for example,
  if any of the TRK sequences includes the module `process.caloTowerForTrk`,
  this must be preceeded by the sequence `process.hcalGlobalRecoSequence`
  (see [here](https://github.com/missirol/JMETriggerAnalysis/blob/0b0729437e6563838e790d37dabf4707da834ae4/Common/python/hltPhase2_TRKv06.py#L1166) for an example).

* Although not strictly necessary, inside the customization function,
  delete the object `process.globalreco_trackingTask`,
  in order to avoid inconsistencies between this `cms.Task` of the Offline reconstruction
  and the new definition of `process.globalreco_tracking`:
```
    if hasattr(process, 'globalreco_trackingTask'):
       del process.globalreco_trackingTask
```
