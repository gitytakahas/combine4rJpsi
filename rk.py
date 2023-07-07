import os, numpy, math, copy, math
from ROOT import gStyle, TCanvas, TLegend, gROOT, TGraphAsymmErrors, Double, TH2F, kBlack, TBox, kGreen, kOrange, TFile, TH1F, TLatex, TLine, TPaveText, kGray
from common.officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetLabelSize  (0.050,"X")
gStyle.SetLabelSize  (0.070,"Y")
gStyle.SetOptTitle(0)


gStyle.SetPadLeftMargin  (0.22)
gStyle.SetPadTopMargin   (0.1)

from collections import OrderedDict
dict = OrderedDict()

#dict['rkp'] = {'val':0.86, 'up':0.14, 'down':-0.11, 'sup':0.05, 'sdown':-0.05, 'q2low':0.1, 'q2high':6.0, 'leg':'R_{pK^{-}}'}
#dict['rks0'] = {'val':0.66, 'up':0.2, 'down':-0.14, 'sup':0.02, 'sdown':-0.04, 'q2low':1.1, 'q2high':6.0, 'leg':'R_{K_{s}^{0}}'}
#dict['rks_low'] = {'val':0.66, 'up':0.11, 'down':-0.07, 'sup':0.03, 'sdown':-0.03, 'q2low':0.045, 'q2high':1.1, 'leg':'R_{K^{*0}}'}
#dict['rks_high'] = {'val':0.69, 'up':0.11, 'down':-0.07, 'sup':0.05, 'sdown':-0.05, 'q2low':1.1, 'q2high':6.0, 'leg':'R_{K^{*0}}'}
#dict['rksp'] = {'val':0.7, 'up':0.18, 'down':-0.13, 'sup':0.03, 'sdown':-0.04, 'q2low':0.045, 'q2high':6.0, 'leg':'R_{K^{*+}}'}
#dict['rk'] = {'val':0.846, 'up':0.042, 'down':-0.039, 'sup':0.013, 'sdown':-0.012, 'q2low':1.1, 'q2high':6.0, 'leg':'R_{K^{+}}'}
dict['#tau_{had} combined'] = {'val':0.71, 'up':0.0555, 'down':-0.0552, 'sup':0.1793, 'sdown':-0.1668, 'leg':'#tau_{had}, comb.'}
dict['#tau_{had} 2018'] = {'val':0.71, 'up':0.0589, 'down':-0.0586, 'sup':0.1866, 'sdown':-0.1783, 'leg':'#tau_{had}, 2018'}
dict['#tau_{had} 2017'] = {'val':0.71, 'up':0.0664, 'down':-0.0660, 'sup':0.2277, 'sdown':-0.2221, 'leg':'#tau_{had}, 2017'}
dict['#tau_{had} 2016'] = {'val':0.71, 'up':0.07, 'down':-0.0696, 'sup':0.2588, 'sdown':-0.2553, 'leg':'#tau_{had}, 2016'}
#dict['#tau_{lep} 2018'] = {'val':0.71, 'up':0.094, 'down':-0.093, 'sup':0.252, 'sdown':-0.249, 'leg':'#tau_{lep}, 2018'}
dict['LHCb'] = {'val':0.71, 'up':0.17, 'down':-0.17, 'sup':0.18, 'sdown':-0.18, 'leg':'LHCb, Run1'}

def add_CMS():
    lowX=0.22
    lowY=0.84
    lumi  = TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.055)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("#it{Private Compilation}")
    return lumi



cnt = 1

graphs = []
graphs_tot = []

frame = TH2F('frame', 'frame', 100,0.,1.4, len(dict),0,len(dict))



labels = []

for key, var in dict.items():

    print(key)

    frame.GetYaxis().SetBinLabel(cnt, '')
    frame.GetXaxis().SetTitle('R_{J/#psi}')

    graph = TGraphAsymmErrors()
    graph_tot = TGraphAsymmErrors()

#    print(var['val'], cnt - 0.5)

    graph.SetPoint(0, var['val'], cnt - 0.5, )
    graph.SetPointError(0, abs(var['down']), abs(var['up']), 0, 0)

    graph_tot.SetPoint(0, var['val'], cnt - 0.5, )
    graph_tot.SetPointError(0, math.sqrt(var['down']**2 + var['sdown']**2), math.sqrt(var['up']**2 + var['sup']**2), 0, 0)

#    graph.SetFillColor(65)
#    graph.SetLineStyle(0)

#    graph.SetLineColor(4)
#    graph.SetLineWidth(2)


    graphs.append(copy.deepcopy(graph))
    graphs_tot.append(copy.deepcopy(graph_tot))



    cnt += 1

canvas = TCanvas('can','can',800,500)

frame.Draw()

for graph in graphs_tot:

    graph.SetMarkerColor(1)
    graph.SetLineColor(1)
    graph.SetLineWidth(10)

#    graph.SetLineWidth(2)
#    graph.SetLineColor(214)
    graph.Draw('ZPSAME') # draw with graph

#    legend.AddEntry(graph,band.GetTitle(),'fl')

for graph in graphs:

    graph.SetLineColor(3)
    graph.SetLineWidth(4)
#    graph.SetLineStyle(2)

#    graph.SetLineWidth(2)
#    graph.SetLineColor(214)
    graph.Draw('ZPSAME') # draw with graph


cnt = 1
for key, var in dict.items():
    latex = TLatex()
#    latex.SetNDC(True)
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    latex.SetTextColor(kBlack)
    latex.DrawLatex(-0.3, float(cnt-0.5),var['leg'])
    cnt += 1

line = TLine(0.71, 0, 0.71, len(dict))
line.SetLineStyle(2)
line.Draw()

#line2 = TLine(0,4,1.4, 4)
#line2.SetLineColor(kGray)
#line2.Draw()


tbox = TBox(0.2544,0,0.2620,len(dict))
tbox.SetLineWidth(3)
tbox.SetLineColor(2)
tbox.SetFillStyle(3001)
tbox.SetFillColor(2)
tbox.Draw('same')

m1=add_CMS()
m1.Draw('same')


canvas.RedrawAxis()
canvas.SaveAs('Plots/rjpsi_sensitivity.pdf')
canvas.SaveAs('Plots/rjpsi_sensitivity.gif')
