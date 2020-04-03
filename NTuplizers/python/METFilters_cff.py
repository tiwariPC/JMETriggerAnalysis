import FWCore.ParameterSet.Config as cms

def METFilters(process, era):
    process.METFiltersTask = cms.Task()

    ### Ref: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    if era == '2016':
       pass

    elif era in ['2017', '2018']:

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
       process.METFiltersTask.add(process.ecalBadCalibReducedMINIAODFilter)
       ## ---

    else:
       raise RuntimeError('invalid value for options["sample"]["era"]: '+era)

    process.METFiltersSeq = cms.Sequence(process.METFiltersTask)

    return process
