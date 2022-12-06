#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT
import os
import sys

#args = sys.argv

shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4/tau_rhomass_unrolled_var.root'

file = ROOT.TFile(shape_file)

cb = ch.CombineHarvester()

sig_procs = ['bc_jpsi_tau']
bkg_procs = ['bc_others', 'bc_jpsi_dst', 'dd_bkg']

name = 'tauhad'

channels = [name]

#eras = ['2018']
eras = ['2016', '2017', '2018']

categories = {}

for era in eras:
    categories[name + '_' + era] = [(1, name + '_' + era)]

prefix = ['rJpsi']


#extraStr = ''

for era in eras:
    for chn in channels:
        cb.AddObservations(['*'], prefix, [era], [chn], categories[chn + '_' + era])
        cb.AddProcesses(['*'], prefix, [era], [chn], bkg_procs, categories[chn + '_' + era], False)
        cb.AddProcesses(['90'], prefix, [era], [chn], sig_procs, categories[chn + '_' + era], True)


print '>> Adding systematic uncertainties...'

#cb.cp().process(['qqH', 'ggH', 'WH', 'ZH', 'Dibosons', 'WJets']).AddSyst(
#    cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')  
#    (['7TeV'], 1.022) 
#    (['8TeV'], 1.026))


#cb.cp().channel(['ee']).process_rgx([higgs_rgx, 'ZTT', 'TTJ', 'Dibosons']).AddSyst(
#    cb, 'CMS_scale_e_$ERA', 'shape', ch.SystMap()(0.50))




cb.cp().AddSyst(
    cb, 'tauReco', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

#cb.cp().AddSyst(
#    cb, 'xgbsEff', 'shape', ch.SystMap('channel', 'process')
#    (channels, sig_procs + bkg_procs, 1.0))

# This is from Stefano's number: https://sleontsi.web.cern.ch/sleontsi/Bc+/Yuta/

cb.cp().process(['dd_bkg']).AddSyst(
    cb, 'CMS_bkg_$ERA', 'lnN', ch.SystMap()(1.3))



cb.cp().AddSyst(
    cb, 'br_BcJpsiDst', 'shape', ch.SystMap('channel', 'process')
    (channels, [ 'bc_jpsi_dst', 'dd_bkg'], 1.0))

for hammer in range(0, 10):
    cb.cp().AddSyst( 
        cb, 'hammer_ebe_e' + str(hammer), 'shape', ch.SystMap('channel', 'process')
        (channels, ['bc_jpsi_tau', 'dd_bkg'], 1.0))

cb.cp().AddSyst( 
    cb, 'puweight', 'shape', ch.SystMap('channel', 'process')
    (channels, sig_procs + bkg_procs, 1.0))

cb.cp().AddSyst( 
    cb, 'shape', 'shape', ch.SystMap('channel', 'process')
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



#bbb = ch.BinByBinFactory()
#bbb.SetAddThreshold(0.15).SetFixNorm(False)

#bbb.AddBinByBin(cb.cp().process(sig_procs + ['bc_others', 'bc_jpsi_dst']), cb)


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

outcard = outdir + '/rJpsi_combine.txt'
command = 'combineCards.py'

for era in eras:
    command += " " + name + "_" + era + '=' + outdir + '/rJpsi_' + name + '_1_' + era + '_90.txt'

command += " > " + outcard

print command 

os.system(command)

# overwrite extra rateParam

if os.path.isfile(outcard):

    f = open(outcard, 'a')
#    f.write(extraStr)
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





#cb.cp().process(sig_procs + ['bc_others', 'bc_jpsi_tau_N3p', 'bc_jpsi_dst']).AddSyst(
#    cb, 'CMS_lumi', 'lnN', ch.SystMap()(1.025))

#    cb, 'CMS_bkg', 'lnN', ch.SystMap()((0.98, 1.04)))

#cb.cp().process(['dd_bkg']).AddSyst(
#    cb, 'CMS_bkg', 'rateParam', ch.SystMap()(1.0))

#cb.cp().AddSyst(
#    cb, 'CMS_bkg', 'rateParam', ch.SystMap('channel', 'process')
#    (['dd_bkg'], 1.0))


#cb.cp().AddSyst(
#    cb, 'bkgExtra', 'shape', ch.SystMap('channel', 'process')
#    (channels, ['dd_bkg'], 1.0))
