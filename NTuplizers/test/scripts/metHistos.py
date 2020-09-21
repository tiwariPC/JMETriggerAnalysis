#!/usr/bin/env python
import os
import glob
import ROOT

#input_files = os.environ['CMSSW_BASE']+'/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200909_MB/ntuples/HLT_TRKv06/Phase2HLTTDR_MinBias_14TeV_PU200.root'
#output_file = 'metHistos_MB_PU200_hltWithoutTICL.root'

input_files = os.environ['CMSSW_BASE']+'/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200909_MB/ntuples/HLT_TRKv06_TICL/Phase2HLTTDR_MinBias_14TeV_PU200.root'
output_file = 'metHistos_MB_PU200_hltWithTICL.root'

ttree_key = 'JMETriggerNTuple/Events'

tchain = ROOT.TChain(ttree_key)
input_files = glob.glob(input_files)
for _tmp in input_files:
  tchain.Add(_tmp)

metTypes = [
  'l1tPFMET_pt',
  'l1tPFPuppiMET_pt',
  'hltPFMET_pt',
  'hltPFCHSMET_pt',
  'hltPFPuppiMET_pt',
  'hltPFPuppiMETv0_pt',
  'offlinePFMET_Raw_pt',
  'offlinePFPuppiMET_Raw_pt',
  'offlinePFPuppiMET_Type1_pt',
]

tchain.SetBranchStatus('*', False)
tchain.SetBranchStatus('L1T_*', True)
tchain.SetBranchStatus('HLT_*', True)
for _tmp in metTypes:
  tchain.SetBranchStatus(_tmp, True)

histos = {}
for _tmp in metTypes:
  histos[_tmp] = ROOT.TH1D(_tmp, _tmp, 500, 0, 500)
  histos[_tmp].SetDirectory(0)
  histos[_tmp].Sumw2()

for _tmp in range(len(metTypes)):
  for _tmp2 in range(_tmp+1, len(metTypes)):
    _name1 = metTypes[_tmp]
    _name2 = metTypes[_tmp2]
    _hname = _name1+'__'+_name2
    histos[_hname] = ROOT.TH2D(_hname, _hname, 500, 0, 500, 500, 0, 500)
    histos[_hname].SetDirectory(0)
    histos[_hname].Sumw2()

triggerCounts = {}
for br_i in tchain.GetListOfBranches():
  brName_i = br_i.GetName()
  if brName_i.startswith('L1T_') or brName_i.startswith('HLT_'):
    triggerCounts[brName_i] = 0

triggerCounts['l1tPFMET120'] = 0
triggerCounts['l1tPFMET120 && offlinePFMET120_Raw'] = 0
triggerCounts['l1tPFPuppiMET100'] = 0
triggerCounts['l1tPFPuppiMET120'] = 0
triggerCounts['l1tPFPuppiMET120 && offlinePFPuppiMET120_Raw'] = 0
triggerCounts['hltPFMET120'] = 0
triggerCounts['hltPFCHSMET120'] = 0
triggerCounts['hltPFPuppiMET120'] = 0
triggerCounts['hltPFPuppiMET120_v0'] = 0
triggerCounts['offlinePFMET120_Raw'] = 0
triggerCounts['offlinePFPuppiMET120_Raw'] = 0
triggerCounts['offlinePFPuppiMET120_Type1'] = 0

numEvents = 0
for evt in tchain:
    numEvents += 1

    if not (numEvents % 10000):
       print 'events processed:', numEvents

    for trigName in triggerCounts:
      if hasattr(evt, trigName) and (getattr(evt, trigName) == True):
        triggerCounts[trigName] += 1

    if evt.l1tPFMET_pt[0] > 120.:
      triggerCounts['l1tPFMET120'] += 1
      if evt.offlinePFMET_Raw_pt[0] > 120.:
        triggerCounts['l1tPFMET120 && offlinePFMET120_Raw'] += 1

    if evt.l1tPFPuppiMET_pt[0] > 100.:
      triggerCounts['l1tPFPuppiMET100'] += 1

    if evt.l1tPFPuppiMET_pt[0] > 120.:
      triggerCounts['l1tPFPuppiMET120'] += 1
      if evt.offlinePFPuppiMET_Raw_pt[0] > 120.:
        triggerCounts['l1tPFPuppiMET120 && offlinePFPuppiMET120_Raw'] += 1

    if evt.hltPFMET_pt[0] > 120.:
      triggerCounts['hltPFMET120'] += 1

    if evt.hltPFCHSMET_pt[0] > 120.:
      triggerCounts['hltPFCHSMET120'] += 1

    if evt.hltPFPuppiMET_pt[0] > 120.:
      triggerCounts['hltPFPuppiMET120'] += 1

    if evt.hltPFPuppiMETv0_pt[0] > 120.:
      triggerCounts['hltPFPuppiMET120_v0'] += 1

    if evt.offlinePFMET_Raw_pt[0] > 120.:
      triggerCounts['offlinePFMET120_Raw'] += 1

    if evt.offlinePFPuppiMET_Raw_pt[0] > 120.:
      triggerCounts['offlinePFPuppiMET120_Raw'] += 1

    if evt.offlinePFPuppiMET_Type1_pt[0] > 120.:
      triggerCounts['offlinePFPuppiMET120_Type1'] += 1

    for _tmp in metTypes:
      histos[_tmp].Fill(getattr(evt, _tmp)[0])

    for _tmp in range(len(metTypes)):
      for _tmp2 in range(_tmp+1, len(metTypes)):
        _name1 = metTypes[_tmp]
        _name2 = metTypes[_tmp2]
        _hname = _name1+'__'+_name2
        histos[_hname].Fill(getattr(evt, _name1)[0], getattr(evt, _name2)[0])

print '-'*50
print 'Events processed =', numEvents
print '-'*50

for trigName in sorted(triggerCounts.keys()):
  print '{:<60} {: >10d} {: >12.3f}'.format(trigName, triggerCounts[trigName], triggerCounts[trigName]/float(numEvents) * 2748. * 11246.)

ofile = ROOT.TFile(output_file, 'recreate')
ofile.cd()
for _tmp in sorted(histos.keys()):
  histos[_tmp].Write()
ofile.Close()
