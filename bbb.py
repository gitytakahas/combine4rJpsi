from ROOT import TFile
import copy, math

file=TFile('/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/tau_rhomass_unrolled_var.root')

processes = ['jpsi_tau', 'bc_others', 'jpsi_hc']

for year in ['2016', '2017', '2018']:
    for cat in ['sr', 'sb']:

        hists = []
        
        for process in processes:
            hist = file.Get('tauhad_' + cat + '_' + year + '/' + process)
            hists.append(copy.deepcopy(hist))


        
        for ibin in range(1, hists[-1].GetXaxis().GetNbins()+1):

            val = 0.
            unc = 0.

            for hist in hists:
                val += hist.GetBinContent(ibin)
                unc += hist.GetBinError(ibin)*hist.GetBinError(ibin)
            
#            val = hist.GetBinContent(ibin)
#            unc = hist.GetBinError(ibin) 

            neff = float(val*val/unc)
            
            rel = 1/math.sqrt(neff)
            if rel > 0.1:
                print ibin, year, cat, rel
        
    
