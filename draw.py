import os, copy
from ROOT import gStyle, TCanvas, TLegend, TH1F, gROOT, TFile
from officialStyle import officialStyle
from common.DataMCPlot import *
from common.DisplayManager_postfit import DisplayManager
from common.helper import *
from common.H2TauStyle import *

#lumi=140

lumis = {
    '2016':36.5,
    '2017':41.5,
    '2018':59.5
}



gROOT.SetBatch(True)
#gROOT.SetBatch(False)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)




def comparisonPlots(hist, lumi, pname='sync.pdf', isLog=False, isRatio=True, clabel=''):

    display = DisplayManager(pname, isRatio, isLog, lumi, clabel, 0.42, 0.65)
    display.Draw(hist)

#def comparisonPlots(hist, pname='sync.pdf', clabel=labeldir['tautau'], isRatio=False):

#    display = DisplayManager(pname, isRatio, lumi, clabel, 0.42, 0.65)
#    display.Draw(hist)




filename = 'datacard/fitDiagnosticsTest.root'

file = TFile(filename)

print(file)

#process = {
#    'data':{'name':'data'},
#    'total_signal':{'name':'total_signal'},
#    'total_background':{'name':'total_background'}
#}

#for ibin in range(1, nbin+1):
#    process['bg_bin' + str(ibin)] = {'name':'bg_bin' + str(ibin)}


process = {
    'bc_others':{'name':'tt', 'isSignal':0, 'order':4},
    'fakes':{'name':'Diboson', 'isSignal':0, 'order':5},
    'jpsi_hc':{'name':'W', 'isSignal':0, 'order':6},
#    'DY':{'name':'DY', 'isSignal':0, 'order':1},
#    'QCD':{'name':'QCD', 'isSignal':0, 'order':10},
    'data':{'name':'data', 'isSignal':0, 'order':2999},
    'jpsi_tau':{'name':'SingleTop', 'isSignal':1, 'order':3001},
#    'Signal_M800':{'name':'Signal_M800', 'isSignal':0, 'order':3001},
}



ensureDir('Plots/')


for ftype in ['fit_s', 'fit_b', 'prefit']:
#for ftype in ['prefit']:

#    for cr in ['tauhad_2016', 'tauhad_2017', 'tauhad_2018']:
    for year in ['2016', '2017', '2018']:

        for cat in ['sr', 'sb']:
#        for cat in ['sr']:

            catname = ftype + '_' + cat + '_' + year

            hists = []
        
            ymax = -1
            
        
            for ii, var in process.iteritems():
    
                hist_ = file.Get('shapes_' + ftype + '/tauhad_tauhad_' + cat + '_' + year + '/' + ii)

                ### in case of data ... #############
                if ii.find('data')!=-1: 
                    hist_tmp = TH1F('data_' + catname, 'data_' + catname, hists[-1].GetXaxis().GetNbins(), hists[-1].GetXaxis().GetXmin(), hists[-1].GetXaxis().GetXmax())
                    hist_tmp.SetName('data_obs')
                    hist_tmp.SetTitle('data_obs')
#                    import pdb; pdb.set_trace()

                    for jj in range(0, hist_.GetN()):
                        
                        x = Double(0.)
                        y = Double(0.)
                        hist_.GetPoint(jj, x, y)
#                        print jj, y
                        hist_tmp.SetBinContent(jj+1, y)

                    hist_ = hist_tmp 

                ### in case of data ... #############
                
                hist_.SetFillStyle(0)
                
                nbin = hist_.GetXaxis().GetNbins()
                print nbin
                
                if var['isSignal']==1:
                    hist_.SetLineColor(2)
                    hist_.SetLineStyle(2)
                if ii.find('data')!=-1:
                    hist_.Sumw2(False)
                    hist_.SetBinErrorOption(1)
                    hist_.SetMarkerStyle(20)
                    hist_.SetMarkerSize(1)

                hist_.SetLineWidth(3)
                hist_.GetXaxis().SetLabelSize(0.0)
        
                hists.append(copy.deepcopy(hist_))
                
#                if ymax < hist.GetMaximum(): ymax = hist.GetMaximum()

            


 #           hists2draw = copy.deepcopy(hists2write)
#            print ( "Calling    Histo = DataMCPlot(vkey)    for  vkey ", vkey )
            Histo = DataMCPlot(catname)

            for _hist in hists:

                _name = _hist.GetName()

                if _name.find('data')!=-1:
                    _hist.SetFillStyle(0)
#                    _hist.Sumw2(False)
                    _hist.SetBinErrorOption(1)
            

                _hist.SetName(_name)
                _hist.SetTitle(_name)
                _hist.GetXaxis().SetLabelColor(1)
                #            _hist.GetXaxis().SetLabelSize(0.0)

                Histo.AddHistogram(_hist.GetName(), _hist)
#            print ( " Histo = DataMCPlot(vkey) with _hist ", _hist.GetName() ," bins ", _hist.GetNbinsX() )
                if _name.find('data')!=-1:
                    Histo.Hist(_hist.GetName()).stack = False



            Histo._ApplyPrefs()
            print(Histo)
#            comparisonPlots(Histo, lumis[year], 'Plots/' + catname +'.gif')
            comparisonPlots(Histo, lumis[year], 'Plots/' + catname +'.pdf')
            comparisonPlots(Histo, lumis[year], 'Plots/' + catname +'.C')
#            comparisonPlots(Histo, lumis[year], 'Plots/' + catname +'.gif')



#
#            cname = ftype + '_' + cat + '_' + year
#            canvas = TCanvas('canvas_' + cname)
#
#            frame = TH1F('frame_' + cname, 'fname_' + cname, nbin, 0, nbin)
#            frame.GetXaxis().SetTitle('Tau rhomasses unrolled bin ID')
#            frame.GetYaxis().SetTitle('Events')
#            
#            frame.SetMaximum(ymax*2.)
#            frame.SetMinimum(0.)
#            
#            frame.Draw()
#            
#            hs = copy.deepcopy(hists['total_background'])
#            hs.Add(copy.deepcopy(hists['total_signal']))
#            hs.SetFillStyle(1)
#            hs.SetFillColor(2)
#            hs.SetLineColor(2)
#            hs.Draw('hsame')
#            
#            hists['total_background'].SetFillStyle(1)
#            hists['total_background'].SetFillColor(10)
#            hists['total_background'].Draw('hsame')
#            
#            hists['total_signal'].Draw('hsame')
#            hists['data'].Draw('epzsame')
#            
#            canvas.RedrawAxis()                
#            canvas.SaveAs('Plots/' + cname + '.gif')
            
