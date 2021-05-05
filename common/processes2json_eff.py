import json
import collections as cl

processes = {} #cl.OrderedDict()

# ttbar

processes['TTLL'] = {'name':'TTLL',
                     'file':'TT/TTTo2L2Nu_gen',
                     'cut':'1',
                     'cross-section':88.29,
                     'isSignal':0, 
                     'order':1 }

processes['TTLJ'] = {'name':'TTLJ',
                     'file':'TT/TTToSemiLeptonic_gen',
                     'cut':'1',
                     'cross-section':365.35,
                     'isSignal':0, 
                     'order':1}

processes['TTJJ'] = {'name':'TTJJ',
                     'file':'TT/TTToHadronic_gen',
                     'cut':'1',
                     'cross-section':377.96,
                     'isSignal':0, 
                     'order':1}

processes['TT'] = {'name':'TT',
                     'file':'TT/TT_gen',
                     'cut':'1',
                     'cross-section':831.6,
                     'isSignal':0, 
                     'order':1}





# Z + jets

processes['ZTT'] = {'name':'ZTT',
                    'file':'DY/DYJetsToLL_M-50_gen',
                    'cross-section':1.,
                    'cut':'1',
                    'isSignal':0,
                    'order':3}

processes['ZTT1'] = {'name':'ZTT1',
                     'file':'DY/DY1JetsToLL_M-50_gen',
                     'cross-section':1.,
                     'cut':'1',
                     'isSignal':0, 
                     'order':3}

processes['ZTT2'] = {'name':'ZTT2',
                     'file':'DY/DY2JetsToLL_M-50_gen',
                     'cross-section':1.,
                     'cut':'1',
                     'isSignal':0, 
                     'order':3}

processes['ZTT3'] = {'name':'ZTT3',
                     'file':'DY/DY3JetsToLL_M-50_gen',
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
                          'file':'DY/DYJetsToLL_M-10to50_gen',
                          'cross-section':18610.0,
                          'cut':'1',
                          'isSignal':0, 
                          'order':3}





outputjson = open('processes_gen.json','w')
json.dump(processes, outputjson, indent=4)
