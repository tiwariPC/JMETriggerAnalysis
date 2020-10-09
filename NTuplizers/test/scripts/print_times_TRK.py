#!/usr/bin/env python
import argparse
import os
import fnmatch
import math
import ROOT

def updateDictionary(dictionary, TDirectory, prefix='', matches=[], skip=[], verbose=False):

    key_prefix = prefix+'/' if (len(prefix) > 0) else ''

    for j_key in TDirectory.GetListOfKeys():
        print j_key
        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        try:
          aaa = j_obj.InheritsFrom('TDirectory')
        except:
          continue

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, matches=matches, skip=skip, verbose=verbose)

        elif j_obj.InheritsFrom('TH1') or j_obj.InheritsFrom('TGraph'):

           out_key = key_prefix+j_key_name

           if skip:
              skip_key = False
              for _keyw in skip:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = True
                     break
              if skip_key:
                 continue

           if matches:
              skip_key = True
              for _keyw in matches:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = False
                     break
              if skip_key:
                 continue

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           if hasattr(dictionary[out_key], 'SetDirectory'):
              dictionary[out_key].SetDirectory(0)

           if verbose:
              print colored_text('[input]', ['1','92']), out_key

    return dictionary

def getTH1sFromTFile(path, matches=[], skip=[], verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', matches=matches, skip=skip, verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict




#histos = getTH1sFromTFile('DQM_V0001_R000000001__HLT__FastTimerService__All.root', matches=['*/module_time_real_total'], verbose=False)
import sys
i_inptfile = ROOT.TFile.Open(sys.argv[1])
#histo_nominal = i_inptfile.Get('DQMData/Run 1/HLT/Run summary/TimerService/process RECO2 paths/path HLT_AK4PuppiJet100_v1/module_time_real_running')
histo_nominal = i_inptfile.Get('DQMData/Run 1/HLT/Run summary/TimerService/process RECO2 paths/path HLT_PFPuppiMET250_v1/module_time_real_running')
print histo_nominal

tracking_modules = [
'siPhase2Clusters',
'siPixelClusters',
'siPixelClusterShapeCache',
'siPixelRecHits',
'MeasurementTrackerEvent',
'pixelTrackFilterByKinematics',
'pixelFitterByHelixProjections',
'pixelTracksTrackingRegions',
'pixelTracksSeedLayers',
'pixelTracksHitDoublets',
'pixelTracksHitSeeds',
'pixelTracks',
'pixelVertices',
'trimmedPixelVertices',
'initialStepSeeds',
'initialStepTrackCandidates',
'initialStepTracks',
'initialStepTrackCutClassifier',
'initialStepTrackSelectionHighPurity',
'highPtTripletStepClusters',
'highPtTripletStepSeedLayers',
'highPtTripletStepTrackingRegions',
'highPtTripletStepHitDoublets',
'highPtTripletStepHitTriplets',
'highPtTripletStepSeeds',
'highPtTripletStepTrackCandidates',
'highPtTripletStepTracks',
'highPtTripletStepTrackCutClassifier',
'highPtTripletStepTrackSelectionHighPurity',
'unsortedOfflinePrimaryVertices',
'caloTowerForTrk',
'ak4CaloJetsForTrk',
'trackWithVertexRefSelectorBeforeSorting',
'trackRefsForJetsBeforeSorting',
'offlinePrimaryVertices',
'offlinePrimaryVerticesWithBS',
'inclusiveVertexFinder',
'vertexMerger',
'trackVertexArbitrator',
'inclusiveSecondaryVertices',
'offlineBeamSpot',
'trackerClusterCheck',
'generalTracks',
]

#for hkey in histos:
if True:
#    if hkey.endswith('/module_time_real_total'):

       names =[]
       times=[]
       totalSize=0.
       for bin_i in range(1, histo_nominal.GetXaxis().GetNbins()):
           value = histo_nominal.GetBinContent(bin_i)
           name = histo_nominal.GetXaxis().GetBinLabel(bin_i)
           if name not in tracking_modules:
              continue
           times.append(value)
           names.append(name)
           totalSize+=value

       print '-'*100
       print histo_nominal.GetName()
       print '-'*100

       zipped_lists = zip(names, times)
       sorted_pairs = sorted(zipped_lists,reverse=True, key=lambda x: x[1])
       maxWidthEntry = max(sorted_pairs, key=lambda x: len(x[0])+len(str(x[1]))+1)
       width = len(maxWidthEntry[0]) + len(str(maxWidthEntry[1]))
       
       fractions = [float(b)/float(totalSize)*100. for a,b in sorted_pairs]
       
       i=0
       for a,b in sorted_pairs:
#           print a, " "*(width-len(a)-len(str(b))), b, fractions[i],"%"
           print '{:>5d}. {:<50} {:9.3f} {:5.2f}%'.format(i, a, b, fractions[i])
           i=i+1
       print "-"*(width+len(str(totalSize)))
       print "Total", " "*(width-len("Total")-len(str(totalSize))),totalSize
