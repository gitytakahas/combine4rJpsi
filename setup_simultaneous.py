#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT
import os
import sys


shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse.root'

file = ROOT.TFile(shape_file)
hist = file.Get('sb/data_obs')

cb = ch.CombineHarvester()

sig_procs = ['bc_jpsi_tau_3p']
bkg_procs = ['bc_others', 'bc_jpsi_tau_N3p', 'bc_jpsi_dst']

categories = {
    'sr': [(1, 'sr')],
    'sb': [(2, 'sb')],
    }


channels = ['sr', 'sb']


prefix = ['rJpsi']
era = ['2018']

Nbins = hist.GetXaxis().GetNbins()
print '# of bins = ', Nbins

extraStr = ''
init_sf = 0.092

for chn in channels:

    cb.AddObservations(['*'], prefix, era, [chn], categories[chn])

    cb.AddProcesses(['*'], prefix, era, [chn], bkg_procs, categories[chn], False)
    cb.AddProcesses(['90'], prefix, era, [chn], sig_procs, categories[chn], True)

#    bg_processes = [ 'bg_bin{}'.format(i+1) for i in range(Nbins) ]
#    cb.AddProcesses(['*'], prefix, era, [chn], bg_processes, categories[chn], False)


#    if chn=='sb':
#        for i in range(1, Nbins+1):
#            
#            subtract_total = 0
#            
#            for iproc in bkg_procs:
#                hist_ = file.Get('sb/' + iproc)
#                subtract_total += hist_.GetBinContent(i)
#
#
#            init = hist.GetBinContent(i) - subtract_total
#            print 'init norm. = ', chn, ', bin=', i, ', sb data = ', hist.GetBinContent(i), ', sb sig. = ', subtract_total, ', init =>', init
##            extraStr += 'yield_bg_bin{0} rateParam * bg_bin{0} '.format(i) + str(init) + ' [-10,5000]\n'
#            extraStr += 'yield_bg_bin{0} rateParam * bg_bin{0} 1\n'.format(i)


#print '>> Adding systematic uncertainties...'
#extraStr += 'ratio_sb_sr rateParam sr bg_* ' + str(init_sf) + ' [' + str(init_sf*0.98) + ',' + str(init_sf*1.04)  + ']\n'

#cb.cp().process(sig_procs + bkg_procs).AddSyst(
#    cb, 'CMS_lumi', 'lnN', ch.SystMap()(1.025))

cb.cp().AddSyst(
    cb, 'tauReco', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst(
    cb, 'xgbsEff', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))


cb.cp().AddSyst(
    cb, 'br_BcJpsiDst', 'shape', ch.SystMap('channel', 'process')
    (channels, [ 'bc_jpsi_dst', 'dd_bkg'], 1.0))


for hammer in range(0, 10):
    cb.cp().AddSyst( 
        cb, 'hammer_ebe_e' + str(hammer), 'shape', ch.SystMap('channel', 'process')
        (channels, ['bc_jpsi_tau_3p', 'bc_jpsi_tau_N3p'], 1.0))

cb.cp().AddSyst( 
    cb, 'puweight', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'muSFID', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'muSFReco', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'weight_ctau', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'tauBr', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs, 1.0))

cb.cp().AddSyst(
    cb, 'BcPt', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))




print '>> Extracting histograms from input root files...'

for chn in channels:
    cb.cp().channel([chn]).ExtractShapes(
        '%s' % (shape_file),
        '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')


cb.SetGroup('syst', ['.*'])
cb.SetGroup('lumi', ['CMS_lumi'])
cb.RemoveGroup('syst', ['CMS_lumi'])


rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(0.3).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)
rebin.Rebin(cb, cb)


print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)
cb.PrintAll()

writer = ch.CardWriter('$TAG/$ANALYSIS_$CHANNEL_$BINID_$ERA_$MASS.txt',
                       '$TAG/common/$ANALYSIS_$CHANNEL_$BINID_$ERA_$MASS.input.root')

writer.SetVerbosity(1)

outdir = 'output/sm_cards/LIMITS'

for chn in channels:  # plus a subdir per channel
    print 'writing', chn, cb.cp().channel([chn])
    writer.WriteCards(outdir, cb.cp().channel([chn]))


print '>> Done!'

outcard = outdir + '/rJpsi_2018_90.txt'
command = 'combineCards.py sr=' + outdir + '/rJpsi_sr_1_2018_90.txt sb=' + outdir + '/rJpsi_sb_2_2018_90.txt > ' + outcard

os.system(command)

#overwrite extra rateParam
#if os.path.isfile(outcard):
#
#    f = open(outcard, 'a')
#    f.write(extraStr)
##    f.write('* autoMCStats 0 1\n')
#    f.close()

#command2 = 'text2workspace.py ' + outcard + ' -o ' + outdir + '/workspace_mu1.root -m 90'
#os.system(command2)



