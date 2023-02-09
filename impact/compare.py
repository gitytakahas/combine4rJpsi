import json, copy, sys
from ROOT import TGraphAsymmErrors, TFile, TH2F, gStyle, gROOT, TCanvas, TLegend
from officialStyle import officialStyle
#from TreeProducerBcJpsiTauNu import *

#out = TreeProducerBcJpsiTauNu('compare.root', 'data')

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

#from TreeProducerBcJpsiTauNu import *


def applyLegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)


#outf = open('idlist.txt', 'w')




n_params = 2000
#n_params = 30

from collections import OrderedDict
dicts = OrderedDict()


dicts['0b_only'] = {'file':'impacts_had.json', 'poi':'r', 'mstyle':21, 'col':2, 'lwidth':3, 'offset':0}
dicts['0b_allcat'] = {'file':'impacts_lep.json', 'poi':'r', 'mstyle':22, 'col':4, 'lwidth':3, 'offset':-0.1}
dicts['allcat'] = {'file':'impacts_comb.json', 'poi':'r', 'mstyle':20, 'col':1, 'lwidth':3, 'offset':0.1}

base='allcat'
#base='0b_only'

#f = open('nuisdict.json')
#namedict = json.load(f)


#bonlydict = {}
#
#for line in open('../pulls/combine_pull.txt', 'r'):
#    line = line.rstrip().split()
#    nuisance = line[0]
#    val = line[1]
#    unc = line[2]
#
#    bonlydict[nuisance] = {'val':val, 'unc':unc}



datas = {}

graphs = OrderedDict()

for key, var in dicts.items():

    f = open(var['file'])
  
    data = json.load(f)

    POIs = [ele['name'] for ele in data['POIs']]
    POI = POIs[0]
    var['poi'] = POI

    data['params'].sort(key=lambda x: abs(x['impact_%s' % POI]), reverse=True)

    datas[key] = copy.deepcopy(data)
    
    f.close()


    graph = TGraphAsymmErrors()
    graph.SetName(key)
    graph.SetTitle(key)
    graph.SetMarkerStyle(var['mstyle'])
    graph.SetMarkerSize(1)
    graph.SetMarkerColor(var['col'])
    graph.SetLineColor(var['col'])
    graph.SetLineWidth(var['lwidth'])

    graphs[key] = copy.deepcopy(graph)


    
#bname = 'b_only'
#graph_bonly = TGraphAsymmErrors()
#graph_bonly.SetName(bname)
#graph_bonly.SetTitle(bname)
#graph_bonly.SetMarkerStyle(23)
#graph_bonly.SetMarkerSize(1)
#graph_bonly.SetMarkerColor(6)
#graph_bonly.SetLineColor(6)
#graph_bonly.SetLineWidth(3)
#
#
#graphs[bname] = graph_bonly



frame = TH2F('frame', 'frame', n_params, 0.5, n_params+0.5, 100,-3,3)
frame.GetYaxis().SetTitleOffset(0.4)
frame.GetYaxis().SetTitle('pull')


idx = 0
counter = 0
bcounter = 0

impact_vals = []
impact_names = []

for vals in datas[base]['params']:

#    if idx >= n_params: 
#        break

    name = vals['name']

    err_hi = vals['fit'][2] - vals['fit'][1] 
    err_lo = vals['fit'][1] - vals['fit'][0] 

    graphs[base].SetPoint(idx, idx+1, vals['fit'][1])
    graphs[base].SetPointError(idx, 0., 0., err_lo, err_hi)

    frame.GetXaxis().SetBinLabel(idx+1, name.replace('CMS_',''))


    for key, var in dicts.items():

        if key == base: continue

        valLocated = None

        idx_find = None
        for idx_, vals_ in enumerate(datas[key]['params']):
        
            name_ = vals_['name']

            if name_ == name:

                valLocated = copy.deepcopy(vals_)
                idx_find = idx_


        if valLocated!=None:

##            diff = float(vals['fit'][1]) -  float(valLocated['fit'][1])
##
##            poiname = dicts[base]['poi']
##            impact_hi = float(vals[poiname][2]) - float(vals[poiname][1])
##            impact_lo = float(vals[poiname][1]) - float(vals[poiname][0])
##            average = (abs(impact_hi) + abs(impact_lo))/2.
##            average_postfit = (abs(err_hi) + abs(err_lo))/2.
##            sign = 1
##
##            total = average_postfit*diff*average*sign
##            impact_vals.append(abs(total))
##            impact_names.append(name)


#            print key, var['offset'], 'check=', idx+1+var['offset']

            graphs[key].SetPoint(counter, idx+1+var['offset'], valLocated['fit'][1])

            err_hi = valLocated['fit'][2] - valLocated['fit'][1] 
            err_lo = valLocated['fit'][1] - valLocated['fit'][0] 
            
            graphs[key].SetPointError(counter, 0., 0., err_lo, err_hi)
            counter += 1

#            print('-'*20, name, 'is not existing for', key)

    if bonlydict.has_key(name):
        graphs[bname].SetPoint(bcounter, idx+1, float(bonlydict[name]['val']))
        graphs[bname].SetPointError(bcounter, 0., 0., float(bonlydict[name]['unc']), float(bonlydict[name]['unc']))
        
        bcounter += 1 

    idx += 1


canvas = TCanvas('can', 'can', 2000,600)
legend = TLegend(0.07, 0.75, 0.15, 0.85)
applyLegendSettings(legend)

frame.Draw()

#print graphs

for key, graph in graphs.items():
    print graph.GetName()
    graph.Draw('pz0same')
    legend.AddEntry(graph, key, "lep")

legend.Draw()
canvas.SaveAs('impact_compare.png')




#foo, bar = zip(*sorted(zip(impact_vals, impact_names)))
#for f,b in zip(foo, bar):
#    print f, b



#file = TFile('out.root', 'recreate')
#g_pulls_1poi.Write()
#g_pulls_3poi.Write()
#frame.Write()
#file.Write()
#file.Close()

#out.endJob()
#outf.close()
