import FWCore.ParameterSet.Config as cms

def METFilters(process, isMC, era):

    ### read options
    triggerResults = 'TriggerResults'

    apply_metFilters = True
    ### ---

    ### MET-Filters
    ### REF https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2

    metFilters_flags = []

    metFilters_inputTags = []

    if era == '2016':

       if isMC:

          # 2016 MC
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
#            'Flag_eeBadScFilter',
          ]
          ### ----

       else:

          # 2016 Data
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
            'Flag_eeBadScFilter',
          ]
          ### ----

    elif era == '2017':

       if isMC:

          # 2017 MC
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
#            'Flag_eeBadScFilter',
          ]
          ### ----

       else:

          # 2017 Data
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
            'Flag_eeBadScFilter',
          ]
          ### ----

       ## Re-run filter 'ecalBadCalibReducedMINIAODFilter' on MINIAOD
       ##   - https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#How_to_run_ecal_BadCalibReducedM
       process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter('EcalBadCalibFilter',

         taggingMode = cms.bool(True),
         debug       = cms.bool(False),

         EcalRecHitSource = cms.InputTag('reducedEgamma:reducedEERecHits'),

         ecalMinEt = cms.double(50.),

         baddetEcal = cms.vuint32([
           872439604,872422825,872420274,872423218,
           872423215,872416066,872435036,872439336,
           872420273,872436907,872420147,872439731,
           872436657,872420397,872439732,872439339,
           872439603,872422436,872439861,872437051,
           872437052,872420649,872422436,872421950,
           872437185,872422564,872421566,872421695,
           872421955,872421567,872437184,872421951,
           872421694,872437056,872437057,872437313,
         ]),
       )
       task.add(process.ecalBadCalibReducedMINIAODFilter)

       metFilters_inputTags += ['ecalBadCalibReducedMINIAODFilter']
       ## ---

    elif era == '2018':

       if isMC:

          # 2018 MC
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
#            'Flag_eeBadScFilter',
          ]
          ### ----

       else:

          # 2018 Data
          metFilters_flags = [
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
#            'Flag_BadChargedCandidateFilter',
            'Flag_eeBadScFilter',
          ]
          ### ----

       ## Re-run filter 'ecalBadCalibReducedMINIAODFilter' on MINIAOD
       ##   - https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#How_to_run_ecal_BadCalibReducedM
       process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter('EcalBadCalibFilter',

         taggingMode = cms.bool(True),
         debug = cms.bool(False),

         EcalRecHitSource = cms.InputTag('reducedEgamma:reducedEERecHits'),

         ecalMinEt = cms.double(50.),

         baddetEcal = cms.vuint32([
           872439604,872422825,872420274,872423218,
           872423215,872416066,872435036,872439336,
           872420273,872436907,872420147,872439731,
           872436657,872420397,872439732,872439339,
           872439603,872422436,872439861,872437051,
           872437052,872420649,872422436,872421950,
           872437185,872422564,872421566,872421695,
           872421955,872421567,872437184,872421951,
           872421694,872437056,872437057,872437313,
         ]),
       )
       task.add(process.ecalBadCalibReducedMINIAODFilter)

       metFilters_inputTags += ['ecalBadCalibReducedMINIAODFilter']
       ## ---

    else:
       raise RuntimeError('invalid value for options["sample"]["era"]: '+era)

    ## MET-Filters producer
    from TopAnalysis.ZTopUtils.MetFilterCombiner_cfi import metFilterCombiner
    process.metFilters = metFilterCombiner.clone(

      src = triggerResults,
      flag = metFilters_flags,
      addsrc = metFilters_inputTags,
    )
    task.add(process.metFilters)
    ### ---

    ### MET-Filters sequence
    process.prefilterSequence = cms.Sequence()

    if apply_metFilters:

       # filters created on-the-fly
       for met_filter_mod in metFilters_inputTags:
           process.prefilterSequence *= getattr(process, met_filter_mod)

       # filters already stored as Flags in MINIAOD
       from TopAnalysis.ZTopUtils.NoiseFilter_cfi import noiseFilter

       for met_filter in metFilters_flags:

           if not (met_filter.startswith('Flag_') and met_filter != 'Flag_'):
              raise RuntimeError('METFilters -- invalid name for MET-Filter (does not start with, or has nothing after, "Flag_"): '+met_filter)

           met_filter_mod = 'METFilter' + met_filter[len('Flag_')].upper() + met_filter[len('Flag_')+1:]

           if hasattr(process, met_filter_mod):
              raise RuntimeError('METFilters -- attempting to redefine cms.Process() module: '+met_filter_mod)

           setattr(process, met_filter_mod, noiseFilter.clone(src = triggerResults, flag = met_filter))
           process.prefilterSequence *= getattr(process, met_filter_mod)
    ### ---

    return process
