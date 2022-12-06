import os, copy
from ROOT import gStyle, TCanvas, TLegend, TH1F, gROOT, TFile
from officialStyle import officialStyle
#from common.DisplayManager_postfit import DisplayManager
#from common.DataMCPlot import *


gROOT.SetBatch(True)
#gROOT.SetBatch(False)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(1111)
gStyle.SetOptFit(1111)



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



filename = 'output/sm_cards/LIMITS/fitDiagnosticsTest.root'

file = TFile(filename)
tree = file.Get('tree_fit_sb')

bias = TH1F('bias', 'bias', 100,-5,5)
bias.GetXaxis().SetTitle('Pull')
bias.GetYaxis().SetTitle('a.u.')

tree.Draw("(r-0.71)/(0.5*(rHiErr+rLoErr))>>bias")

canvas = TCanvas('canvas')
bias.Draw()
bias.Fit('gaus')

canvas.RedrawAxis()                
canvas.SaveAs('bias.pdf')
