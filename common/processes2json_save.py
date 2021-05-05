import json
import collections as cl

processes = {} #cl.OrderedDict()

# ttbar

processes['TTLL'] = {'name':'TTLL',
                     'file':'TT/TTTo2L2Nu',
                     'cut':'1',
                     'cross-section':88.29,
                     'isSignal':0, 
                     'order':1 }

processes['TTLJ'] = {'name':'TTLJ',
                     'file':'TT/TTToSemiLeptonic',
                     'cut':'1',
                     'cross-section':365.35,
                     'isSignal':0, 
                     'order':1}

processes['TTJJ'] = {'name':'TTJJ',
                     'file':'TT/TTToHadronic',
                     'cut':'1',
                     'cross-section':377.96,
                     'isSignal':0, 
                     'order':1}

processes['TT'] = {'name':'TT',
                     'file':'TT/TT',
                     'cut':'1',
                     'cross-section':831.6,
                     'isSignal':0, 
                     'order':1}





# Z + jets

processes['ZTT'] = {'name':'ZTT',
                    'file':'DY/DYJetsToLL_M-50_reg',
                    'cross-section':1.,
                    'cut':'1',
                    'isSignal':0,
                    'order':3}

processes['ZTT1'] = {'name':'ZTT1',
                     'file':'DY/DY1JetsToLL_M-50',
                     'cross-section':1.,
                     'cut':'1',
                     'isSignal':0, 
                     'order':3}

processes['ZTT2'] = {'name':'ZTT2',
                     'file':'DY/DY2JetsToLL_M-50',
                     'cross-section':1.,
                     'cut':'1',
                     'isSignal':0, 
                     'order':3}

processes['ZTT3'] = {'name':'ZTT3',
                     'file':'DY/DY3JetsToLL_M-50',
                     'cross-section':1.,
                     'cut':'1',
                     'isSignal':0, 
                     'order':3}

#processes['ZTT4'] = {'name':'ZTT4',
#                     'file':'DY/DY4JetsToLL_M-50',
#                     'cross-section':1.,
#                     'cut':'1',
#                     'isSignal':0, 
#                     'order':3}

processes['ZTT10to50'] = {'name':'ZTT10to50',
                          'file':'DY/DYJetsToLL_M-10to50',
                          'cross-section':18610.0,
                          'cut':'1',
                          'isSignal':0, 
                          'order':3}




## ZL + jets
#
#processes['ZL'] = {'name':'ZL',
#                   'file':'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                   'cross-section':1.,
#                   'cut':'1',
#                   'isSignal':0,
#                   'order':3}
#
#processes['ZL1'] = {'name':'ZL1',
#                    'file':'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'order':3}
#
#processes['ZL2'] = {'name':'ZL2',
#                    'file':'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}
#
#processes['ZL3'] = {'name':'ZL3',
#                    'file':'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}
#
#processes['ZL4'] = {'name':'ZL4',
#                    'file':'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}
#
#
## ZJ + jets
#
#processes['ZJ'] = {'name':'ZJ',
#                   'file':'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                   'cross-section':1.,
#                   'cut':'1',
#                   'isSignal':0,
#                   'order':3}
#
#processes['ZJ1'] = {'name':'ZJ1',
#                    'file':'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'order':3}
#
#processes['ZJ2'] = {'name':'ZJ2',
#                    'file':'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}
#
#processes['ZJ3'] = {'name':'ZJ3',
#                    'file':'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}
#
#processes['ZJ4'] = {'name':'ZJ4',
#                    'file':'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
#                    'cross-section':1.,
#                    'cut':'1',
#                    'isSignal':0, 
#                    'order':3}


# W + jets

processes['W'] = {'name':'W',
                  'file':'WJ/WJetsToLNu',
                  'cross-section':1.,
                  'cut':'1',
                  'isSignal':0, 
                  'order':8}

processes['W1'] = {'name':'W1',
                   'file':'WJ/W1JetsToLNu',
                   'cross-section':1.,
                   'cut':'1',
                   'isSignal':0, 
                   'order':8}

processes['W2'] = {'name':'W2',
                   'file':'WJ/W2JetsToLNu',
                   'cross-section':1.,
                   'cut':'1',
                   'isSignal':0, 
                   'order':8}

processes['W3'] = {'name':'W3',
                   'file':'WJ/W3JetsToLNu',
                   'cross-section':1.,
                   'cut':'1',
                   'isSignal':0, 
                   'order':8}

processes['W4'] = {'name':'W4',
                   'file':'WJ/W4JetsToLNu',
                   'cross-section':1.,
                   'cut':'1',
                   'isSignal':0, 
                   'order':8}


# dibosons

#processes['WWTo1L1Nu2Q'] = {'name':'WWTo1L1Nu2Q',
#                            'file':'VV/WWTo1L1Nu2Q',
#                            'cross-section':49.997,
#                            'cut':'1',
#                            'isSignal':0, 
#                            'order':7}
#
#processes['WWTo2L2Nu'] = {'name':'WWTo2L2Nu',
#                          'file':'VV/WWTo2L2Nu',
#                          'cross-section':49.997,
#                          'cut':'1',
#                          'isSignal':0, 
#                          'order':7}
#
#processes['WZJToLLLNu'] = {'name':'WZJToLLLNu',
#                           'file':'WZ/TauTauAnalysis.WZJToLLLNu_TuneCUETP8M1_13TeV_nlo_Moriond.root',
#                           'cross-section':4.708,
#                           'cut':'1',
#                           'isSignal':0, 
#                           'order':7}
#
#processes['WZTo1L1Nu2Q'] = {'name':'WZTo1L1Nu2Q',
#                            'file':'WZ/TauTauAnalysis.WZTo1L1Nu2Q_13TeV_nlo_Moriond.root',
#                            'cross-section':10.71,
#                            'cut':'1',
#                            'isSignal':0, 
#                            'order':7}
#
#processes['WZTo1L3Nu'] = {'name':'WZTo1L3Nu',
#                            'file':'WZ/TauTauAnalysis.WZTo1L3Nu_13TeV_nlo_Moriond.root',
#                            'cross-section':3.05,
#                            'cut':'1',
#                            'isSignal':0, 
#                            'order':7}
#
#
#processes['WZTo2L2Q'] = {'name':'WZTo2L2Q',
#                         'file':'WZ/TauTauAnalysis.WZTo2L2Q_13TeV_nlo_Moriond.root',
#                         'cross-section':5.595,
#                         'cut':'1',
#                         'isSignal':0, 
#                         'order':7}
#
#
#processes['VVTo2L2Nu'] = {'name':'VVTo2L2Nu',
#                          'file':'ZZ/TauTauAnalysis.VVTo2L2Nu_13TeV_nlo_Moriond.root',
#                          'cross-section':11.95,
#                          'cut':'1',
#                          'isSignal':0, 
#                          'order':7}
#
#
#processes['ZZTo2L2Q'] = {'name':'ZZTo2L2Q',
#                          'file':'ZZ/TauTauAnalysis.ZZTo2L2Q_13TeV_nlo_Moriond.root',
#                          'cross-section':3.22,
#                          'cut':'1',
#                          'isSignal':0, 
#                          'order':7}

          
processes['WW'] = {'name':'WW',
                   'file':'VV/WW',
                   'cross-section':75.88,
                   'cut':'1',
                   'isSignal':0, 
                   'order':7}

processes['WZ'] = {'name':'WZ',
                   'file':'VV/WZ',
                   'cross-section':27.60,
                   'cut':'1',
                   'isSignal':0, 
                   'order':7}

processes['ZZ'] = {'name':'ZZ',
                   'file':'VV/ZZ',
                   'cross-section':12.14,
                   'cut':'1',
                   'isSignal':0, 
                   'order':7}


# single top
    
processes['ST_t_t'] = {'name':'ST_t_t',
                       'file':'ST/ST_t-channel_top',
                       'cross-section':136.02,
                       'cut':'1',
                       'isSignal':0, 
                       'order':9}

processes['ST_t_tbar'] = {'name':'ST_t_tbar',
                          'file':'ST/ST_t-channel_antitop',
                          'cross-section':80.95,
                          'cut':'1',
                          'isSignal':0, 
                          'order':10}

processes['ST_tw_t'] = {'name':'ST_tw_t',
                        'file':'ST/ST_tW_top',
                        'cross-section':35.85,
                        'cut':'1',
                        'isSignal':0, 
                        'order':11}

processes['ST_tw_tbar'] = {'name':'ST_tw_tbar',
                           'file':'ST/ST_tW_antitop',
                           'cross-section':35.85,
                           'cut':'1',
                           'isSignal':0, 
                           'order':12}


# signals

#processes['Signal_pair_M200'] = {'name':'Signal_pair_M200',
#                                 'file':'tba',
#                                 'cross-section':60.6,
#                                 'cut':'1',
#                                 'isSignal':1, 
#                                 'order':3000}



# data

processes['SingleMuon'] = {'name':'data_obs',
                           'file':'SingleMuon/SingleMuon_Run',
                           'cross-section':1.,
                           'cut':'1',
                           'isSignal':0, 
                           'order':2999}


processes['Tau'] = {'name':'data_obs',
                    'file':'Tau/Tau_Run',
                    'cross-section':1.,
                    'cut':'1',
                    'isSignal':0, 
                    'order':2999}



# place holder
processes['QCD'] = {'name':'QCD',
                    'file':None,
                    'cross-section':None,
                    'cut':'1',
                    'isSignal':0, 
                    'order':0}




outputjson = open('processes.json','w')
json.dump(processes, outputjson, indent=4)



# scalar LQ

#for ptype in ['pair','s-channel']:
for ptype in ['pair']:
    for mass in [500, 1000, 1500, 2000]:

        processes['SLQ_' + ptype + '_M' + str(mass)] = {'name':'SLQ_' + ptype + '_M' + str(mass),
                                                        'file':'LQ/LQ3ToTauB_' + ptype + '_M' + str(mass),
                                                        'cross-section':1.,
                                                        'cut':'1',
                                                        'isSignal':1, 
                                                        'order':3000}
        

# vector LQ
#
#for ptype in ['pair','s_channel']:
#    for mass in [500, 1000, 1500, 2000]:
#
#        processes['VLQ_' + ptype + '_M' + str(mass)] = {'name':'VLQ_' + ptype + '_M' + str(mass),
#                                                        'file':'VectorLQ3ToTauB_Fall2017_5f_Madgraph_LO_' + ptype + '_M' + str(mass) + '__nanoAOD__v1',
#                                                        'cross-section':1.,
#                                                        'cut':'1',
#                                                        'isSignal':1, 
#                                                        'order':3000}
#
#
## NonRes LQ
#
#for ptype in ['t-channel']:
#    for mass in ['500', '600', '700', '800', '900', '1000_v2', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000', '2500', '3000', '5000', '7000']:
#
#        processes['SLQ_' + ptype + '_M' + str(mass)] = {'name':'SLQ_' + ptype + '_M' + str(mass).replace('_v2',''),
#                                                        'file':'LQ3ToTauB_Fall2017_5f_Madgraph_LO_' + ptype + '-M' + str(mass) + '__nanoAOD__v1',
#                                                        'cross-section':1.,
#                                                        'cut':'1',
#                                                        'isSignal':1, 
#                                                        'order':3000}
#
#
#for ptype in ['t-channel']:
#    for mass in ['500', '800', '1000', '1200', '1500', '2000', '2500']:
#
#        processes['VLQ_' + ptype + '_M' + str(mass)] = {'name':'VLQ_' + ptype + '_M' + str(mass).replace('_v2',''),
#                                                        'file':'VectorLQ3ToTauB_Fall2017_5f_Madgraph_LO_' + ptype + '-M' + str(mass) + '__nanoAOD__v1',
#                                                        'cross-section':1.,
#                                                        'cut':'1',
#                                                        'isSignal':1, 
#                                                        'order':3000}
#
#
#for mass in ['1000', '1500', '2000', '2500', '3000', '3500', '4000']:
#    
#    processes['Zprime_M' + str(mass)] = {'name':'Zprime_M' + str(mass),
#                                         'file':'ZprimeToTauTau_M-'+ str(mass) + '_TuneCP5_13TeV-pythia8-tauola__RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1__NANOAODSIM/',
#                                         'cross-section':1.,
#                                         'cut':'1',
#                                         'isSignal':1, 
#                                         'order':3000}     



outputjson = open('processes.json','w')
json.dump(processes, outputjson, indent=4)
