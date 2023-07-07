import os, copy
from ROOT import gStyle, TCanvas, TLegend, TH1F, gROOT, TFile, TChain, TGraphErrors
from officialStyle import officialStyle
#from common.DisplayManager_postfit import DisplayManager
#from common.DataMCPlot import *


#gROOT.SetBatch(True)
gROOT.SetBatch(False)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat("emr")
gStyle.SetOptFit(111)


graph = TGraphErrors()
graph_fit = TGraphErrors()

#for idx, mu in enumerate([0.1, 0.25, 0.5, 0.71, 1]):
for idx, mu in enumerate([0.71]):
    
    folder = str(mu).replace('.', 'p')

    ch = TChain('tree_fit_sb')
#    ch.Add(folder + '/fitDiagnostics*.root')
    ch.Add('./fitDiagnostics*.root')

    #file = TFile(filename)
    #tree = file.Get('tree_fit_sb')
    
    #bias = TH1F('bias', 'bias', 120,-6,6)
    bias = TH1F('bias', 'bias', 50,-7,7)
    bias.GetXaxis().SetTitle('Pull')
    bias.GetYaxis().SetTitle('a.u.')
    
    ch.Draw("(r-" + str(mu) + ")/(0.5*(rHiErr+rLoErr))>>bias", "fit_status==0 && rLoErr > 0.1 && rHiErr > 0.1")
    
    canvas = TCanvas('canvas_' + folder)
    bias.Draw()
    bias.Fit('gaus')
    
    canvas.RedrawAxis()
    canvas.SaveAs('bias_' + folder + '.pdf')
    canvas.SaveAs('bias_' + folder + '.gif')

    print idx 

    graph.SetPoint(idx, mu, bias.GetMean())
    graph.SetPointError(idx, 0, bias.GetRMS())

#    graph_fit.SetPoint(idx, mu, bias.GetMean())
#    graph_fit.SetPointError(idx, 0, bias.GetRMS())
canvas_fit = TCanvas('fit')
graph.GetXaxis().SetTitle('injected signal strength')
graph.GetYaxis().SetTitle('pull')
graph.Draw('apl')
canvas_fit.SaveAs('sig_injection.pdf')
canvas_fit.SaveAs('sig_injection.gif')




#shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/dev/datacard_MUSF_blind/tau_rhomass_unrolled_coarse_new.root'
#<<<<<<< HEAD
#shape_file = '/work/cgalloni/Rjpsi_analysis/CMSSW_10_2_10/src/rJpsi/anal/datacard_fromYuta20220317_sr4p3_sb2p5-3p5_lp2-2p5_fixed_Federica/sr/tau_rhomass_unrolled_new.root'
#file_shape = TFile(shape_file)
#data_sb = file_shape.Get('sb/data_obs')
#nbin = data_sb.GetXaxis().GetNbins()
#=======
##shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/dev/datacard_MUSF_blind/tau_rhomass_unrolled_new.root'
##file_shape = TFile(shape_file)
##data_sb = file_shape.Get('sb/data_obs')
##nbin = data_sb.GetXaxis().GetNbins()
#>>>>>>> origin/main

#os.system('rm -f fitDiagnostics.root')
#os.system('hadd -f fitDiagnostics.root fitDiagnostics*.root')


