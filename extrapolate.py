#from https://gist.github.com/ajgilbert/2085fd740e96ac1f6c60a906754289c2

# Note: requires the CombineHarvester plotting module
# If you don't have CombineHarvester in your local area
# can get just the plotting module with:
#
#  cd $CMSSW_BASE/src
#  git clone via ssh:
#  bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-plotting-ssh.sh)
#  OR
#  git clone via https:
#  bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-plotting-https.sh)

import CombineHarvester.CombineTools.plotting as plot
import ROOT, os



file = ROOT.TFile('/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/plots/ratio.root')

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

upper_boundary = 3.5
lower_boundary = 0.


for year in ['2016', '2017', '2018']:
#for year in ['2016']:

    if year=='2016':
        upper_boundary = 3.

    hist = file.Get('ratio_'+ year)

    # Set pT range for the plot
#    min_pt = -1 #hist.GetXaxis().GetXmin()
    max_pt = hist.GetXaxis().GetXmax()
    vals = [] 

    for ii in range(1, hist.GetXaxis().GetNbins()+1):

        if hist.GetBinCenter(ii) < lower_boundary: continue
        if hist.GetBinError(ii)==0: continue

        vals.append((hist.GetBinCenter(ii), hist.GetBinContent(ii), hist.GetBinError(ii)))

        print ii, hist.GetBinCenter(ii), hist.GetBinContent(ii), hist.GetBinError(ii)


    pt_var = ROOT.RooRealVar('pt', 'pt', lower_boundary, lower_boundary, max_pt)
    eff_var = ROOT.RooRealVar('eff', 'eff', 0.5, -5, 15)
    arg_set = ROOT.RooArgSet(pt_var, eff_var)

    # Create the dataset, telling RooFit to store the errors on the scale factors
    dat = ROOT.RooDataSet('data', '', arg_set, ROOT.RooFit.StoreError(ROOT.RooArgSet(eff_var)))
    # Fill the values in the dataset
    for pt, eff, err in vals:
        pt_var.setVal(pt)
        eff_var.setVal(eff)
        eff_var.setError(err)
        dat.add(arg_set)

        # Create the fitting function, can adjust initial parameter values and
        # ranges here if necessary
    m = ROOT.RooRealVar('m', 'm', 0, -0.2, 0.2)
    c = ROOT.RooRealVar('c', 'c', 1, -5, 10)
    d = ROOT.RooRealVar('d', 'd', 1, -5, 10)
    # Formula is m*(x-x0) + c, where x0 is the first x-value in the vals list
    func = ROOT.RooFormulaVar('pdf', '', '@1*@0*@0 + @2*@0 + @3', ROOT.RooArgList(pt_var, m, c, d))

    # Do a chi2 fit, save the RooFitResult which contains the correlation matrix
    res = func.chi2FitTo(dat, ROOT.RooFit.YVar(eff_var), ROOT.RooFit.Save(True))

    # Set up the plotting
    canv = ROOT.TCanvas("tauid_sf_fit", "tauid_sf_fit")
    pads = plot.OnePad()

    xframe = pt_var.frame(ROOT.RooFit.Title("Tau ID SF Fits"))

    # VisualizeErrors using the covariance matrix sampling method
    func.plotOn(xframe, ROOT.RooFit.VisualizeError(res, 1, False))
    func.plotOn(xframe)
    dat.plotOnXY(xframe, ROOT.RooFit.YVar(eff_var))
    xframe.Draw()

    # Cosmetics
    plot.Set(pads[0], Tickx=1, Ticky=1)
    pads[0].SetGrid(1, 1)
    axis = plot.GetAxisHist(pads[0])
    plot.Set(axis.GetXaxis(), Title='BDT score')
    plot.Set(axis.GetYaxis(), Title='Ratio')
    pads[0].RedrawAxis("g")
    plot.DrawCMSLogo(pads[0], 'CMS', 'Internal', 0, 0.17, 0.05, 1.0, '', 1.0)
    plot.DrawTitle(pads[0], year, 3)

    # save the output
    canv.SaveAs('extrapolate_' + year + '.png')
    canv.SaveAs('extrapolate_' + year + '.pdf')

file.Close()
