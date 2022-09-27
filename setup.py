#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT
import os
import sys

args = sys.argv

shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/2018/tau_rhomass_unrolled_coarse.root'
#shape_file = '/work/cgalloni/Rjpsi_analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4p3/2018/tau_rhomass_unrolled_coarse.root'
#shape_file = '/work/cgalloni/Rjpsi_analysis/CMSSW_10_2_10/src/rJpsi/anal/datacard_fromYuta20220317_sr4p3_sb2p5-3p5_lp2-2p5_fixed_Federica_0p078_weightLuigi_systBkg/sr/tau_rhomass_unrolled_coarse_new.root'


file = ROOT.TFile(shape_file)


#data_sb = file.Get('inclusive_hp/data_obs')

cb = ch.CombineHarvester()

sig_procs = ['bc_jpsi_tau_3p']
bkg_procs = ['bc_others', 'bc_jpsi_tau_N3p', 'bc_jpsi_dst', 'dd_bkg']

categories = {
    'sr': [(1, 'sr')],
    }


channels = ['sr']


prefix = ['rJpsi']
era = ['2018']
#Nbins = data_sb.GetXaxis().GetNbins()

#print '# of bins = ', Nbins
#print 'sf = ', sf

extraStr = ''

for chn in channels:

    cb.AddObservations(['*'], prefix, era, [chn], categories[chn])

    cb.AddProcesses(['*'], prefix, era, [chn], bkg_procs, categories[chn], False)
    cb.AddProcesses(['90'], prefix, era, [chn], sig_procs, categories[chn], True)


print '>> Adding systematic uncertainties...'




#cb.cp().process(sig_procs + ['bc_others', 'bc_jpsi_tau_N3p', 'bc_jpsi_dst']).AddSyst(
#    cb, 'CMS_lumi', 'lnN', ch.SystMap()(1.025))

cb.cp().AddSyst(
    cb, 'tauReco', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst(
    cb, 'xgbsEff', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

# This is from Stefano's number: https://sleontsi.web.cern.ch/sleontsi/Bc+/Yuta/

cb.cp().process(['dd_bkg']).AddSyst(

    cb, 'CMS_bkg', 'lnN', ch.SystMap()((0.98, 1.04)))

cb.cp().AddSyst(
    cb, 'br_BcJpsiDst', 'shape', ch.SystMap('channel', 'process')
    (channels, [ 'bc_jpsi_dst', 'dd_bkg'], 1.0))

for hammer in range(0, 10):
    cb.cp().AddSyst( 
        cb, 'hammer_ebe_e' + str(hammer), 'shape', ch.SystMap('channel', 'process')
        (channels, ['bc_jpsi_tau_3p', 'bc_jpsi_tau_N3p', 'dd_bkg'], 1.0))

cb.cp().AddSyst( 
    cb, 'puweight', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'shape', 'shape', ch.SystMap('channel', 'process')
    (channels, ['dd_bkg'], 1.0))

cb.cp().AddSyst(
    cb, 'bkgExtra', 'shape', ch.SystMap('channel', 'process')
    (channels, ['dd_bkg'], 1.0))

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
#file = aux_shapes + 'datacard_combine_1p.root'

for chn in channels:
    cb.cp().channel([chn]).ExtractShapes(
        '%s' % (shape_file),
        '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')



#rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(0.3).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

# to be robust for the bias!!
rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(0.2).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)
rebin.Rebin(cb, cb)



bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.15).SetFixNorm(False)

bbb.AddBinByBin(cb.cp().process(sig_procs + ['bc_others', 'bc_jpsi_tau_N3p', 'bc_jpsi_dst']), cb)


cb.SetGroup('syst', ['.*'])
cb.SetGroup('bbb', ['CMS_rJpsi_.*_bin_.*'])
cb.RemoveGroup('syst', [ 'CMS_rJpsi_.*_bin_.*'])



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

outcard = outdir + '/rJpsi_sr_1_2018_90.txt'
#command = 'combineCards.py'
#
#for cat, clist in categories.items():
#    command += " " + clist[0][1] + '=' + outdir + '/rJpsi_' + clist[0][1] + '_' + str(clist[0][0]) + '_2018_90.txt'
#
#command += " > " + outcard
#
#print command 
#
#os.system(command)

# overwrite extra rateParam

if os.path.isfile(outcard):

    f = open(outcard, 'a')
    f.write(extraStr)
    f.write('* autoMCStats 0 1\n')
    f.close()

command2 = 'text2workspace.py ' + outcard + ' -o ' + outdir + '/workspace.root -m 90'
os.system(command2)




#outcard = outdir + '/rJpsi_2018_90.txt'
#command = 'combineCards.py sb=' + outdir + '/rJpsi_sb_1_2018_90.txt sr=' + outdir + '/rJpsi_sr_2_2018_90.txt > ' + outcard
#os.system(command)
#
## overwrite extra rateParam
#if os.path.isfile(outcard):
#
#    f = open(outcard, 'a')
#    f.write(extraStr)
#    f.write('* autoMCStats 0 0 1\n')
#    f.close()
#
#command2 = 'text2workspace.py ' + outcard + ' -o ' + outdir + '/workspace.root -m 90'
#os.system(command2)


