#### Instructions to create a customization function from a standalone TRK configuration

* Open the TRK `cff` file that contains the definition of the TRK sequence
  (this will be referred to in the following as `MC_Tracking_vX_cff.py`);
  adjust the configuration in order to have the final
  track-reconstruction and vertex-reconstruction sequences inside the same `cms.Path`/`Task`/`Sequence`
  (this will be referred to in the following as `MC_Tracking_vX`).

* Create the full TRK configuration file by dumping the TRK `cfg` file via `edmConfigDump`
  (in what follows, this will be referred to as `TRKvX_configDump.py`).

* Execute
```
${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/makeTRKCustomizationFunction.sh \
-f TRKvX_configDump.py \
-p MC_Tracking_vX
```

* **Note**: since the modules in TRK configuration are sometimes renamed to include a prefix (currently, `hltPhase2`),
  the previous script only compares modules with the same exact name in the two configurations;
  several modules in the TRK configuration are currently renamed to include a prefix (`hltPhase2`, in recent versions),
  and these modules will thus not be compared to any in the Offline configuration
  (if a module included in the specified `cms.Path`/`Task`/`Sequence`
  has no homonym in the Offline configuration file,
  it will be included in the output of the previous step).
  Therefore, due to this renaming, one might find more differences
  (with respect to the Offline configuration) than there actually are.
  Ultimately, at the end of the previous step,
  the renaming of the TRK modules is reverted
  in order to use the names of the Offline collections,
  and maintain full compatibility with the downstream modules.
  This is necessary for a better integration of modules
  for which we largely rely on developments done for
  the Offline reconstruction (e.g. PF, HGCal, MTD);
  those modules will work without further modifications
  only if the TRK modules are named as in the Offline reconstruction.

* If this steps succeeds, its outputs can be found in a directory called `tmp`;
  this contains the input configuration files (for TRK and Offline),
  and the modules in `MC_Tracking_vX` that differ across the two files; the latter list of modules is in the file `tmp/diff.py`,
  which includes the base of the final customization function.

* Modify the name of customization function in the file `tmp/diff.py`, if necessary.

* Go back to the file `MC_Tracking_vX_cff.py`,
  copy all the sequences relevant to track and vertex reconstruction,
  and add them at the bottom of the customization function in `tmp/diff.py` (before the `return` statement);
  if needed, revert the renaming of the modules inside said sequences,
  to be consistent with the modules already included in the function;
  for the final object that combines all the (sub-)sequences relevant to track	and vertex reconstruction
  use a `cms.Sequence` named `process.globalreco_tracking`
  (i.e. the name of the TRK reconstruction sequence in the Offline reconstruction).

* **Note**: since we are currently using sequences instead of tasks,
  some modifications (usually, additions) might need to be made inside the TRK sequences
  in order to respect the modules' dependencies; for example,
  if any of the TRK sequences includes the module `process.caloTowerForTrk`,
  this must be preceeded by the sequence `process.hcalGlobalRecoSequence`
  (see [here](https://github.com/missirol/JMETriggerAnalysis/blob/0b0729437e6563838e790d37dabf4707da834ae4/Common/python/hltPhase2_TRKv06.py#L1166) for an example).

* Although not strictly necessary,
  add to the customization function
  the deletion of the object `process.globalreco_trackingTask`,
  in order to avoid inconsistencies between this `cms.Task` of the Offline reconstruction
  and the new definition of `process.globalreco_tracking`:
```
    if hasattr(process, 'globalreco_trackingTask'):
       del process.globalreco_trackingTask
```

* **Note**: the above is not an exact procedure; unfortunately,
  there is no guarantee that the end-result will work,
  and give the exact same outputs as the starting TRK configuration.
  Attention needs to be paid in every step,
  and sometimes manual adjustments are necessary.
  Once the customization function technically works,
  it remains necessary to cross-check that the output tracks and vertices
  are the same as those obtained with the original TRK configuration.
