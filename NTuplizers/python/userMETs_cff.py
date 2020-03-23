import FWCore.ParameterSet.Config as cms

def userMETs(process, isMC):

    ### MET recalculation
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#Puppi_MET

    makePuppiesFromMiniAOD( process, True );

    updatedMET_tag = 'Updated'

    if 'era' == '2016':

       runMetCorAndUncFromMiniAOD(process, isData = bool(not isMC), postfix = updatedMET_tag,
         fixEE2017 = False,
       )

       collection = 'slimmedMETs'+updatedMET_tag+'::topDileptonNtuple'

       runMetCorAndUncFromMiniAOD(process,
         isData=bool(not isMC),
         metType="Puppi",
         postfix="Puppi",
         jetFlavor="AK4PFPuppi",
       )

       process.puppiNoLep.useExistingWeights = False
       process.puppi.useExistingWeights = False

       process.METSequence *= getattr(process, 'puppiMETSequence')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+'Puppi')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+updatedMET_tag)

    elif era == '2017':

       runMetCorAndUncFromMiniAOD(process, isData = bool(not isMC), postfix = updatedMET_tag,
         fixEE2017 = True,
         fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
       )

       collection = 'slimmedMETs'+updatedMET_tag+'::topDileptonNtuple'

       runMetCorAndUncFromMiniAOD(process,
         isData=bool(not isMC),
         metType="Puppi",
         postfix="Puppi",
         jetFlavor="AK4PFPuppi",
       )

       process.puppiNoLep.useExistingWeights = False
       process.puppi.useExistingWeights = False

       process.METSequence *= getattr(process, 'puppiMETSequence')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+'Puppi')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+updatedMET_tag)

    elif era == '2018':

       runMetCorAndUncFromMiniAOD(process, isData = bool(not isMC), postfix = updatedMET_tag,
         fixEE2017 = False,
       )

       collection = 'slimmedMETs'+updatedMET_tag+'::topDileptonNtuple'

       runMetCorAndUncFromMiniAOD(process,
         isData=bool(not isMC),
         metType="Puppi",
         postfix="Puppi",
         jetFlavor="AK4PFPuppi",
       )

       process.puppiNoLep.useExistingWeights = False
       process.puppi.useExistingWeights = False

       process.METSequence *= getattr(process, 'puppiMETSequence')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+'Puppi')
       process.METSequence *= getattr(process, 'fullPatMetSequence'+updatedMET_tag)

    else:
       raise RuntimeError('userMETs_cff.py -- invalid value for "era": '+str(era))
    ### ---

    return process
