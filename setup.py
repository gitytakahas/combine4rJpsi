#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT
import os
import sys

args = sys.argv

shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/dev/datacard/combine/q2_simple.root'

mu = ROOT.Double(1)

if len(args)==2:
    mu = ROOT.Double(args[1])



file = ROOT.TFile(shape_file)


data_sb = file.Get('sr/data_obs')
#sig_sb = file.Get('sb/signal')
#bgbc_sb = file.Get('sb/bg_bc')
#bkg_sr = file.Get('sr/bg_ul')
#bkg_sb = file.Get('sb/bg_ul')
#sf = file.Get('sr/sf').GetBinContent(1)
#ratio = file.Get('sr/ratio')

cb = ch.CombineHarvester()

sig_procs = ['signal']
bkg_procs = ['bg_bc']

categories = {
    'sr': [(1, 'sr')],
    'sb': [(2, 'sb')],
    'cr1': [(3, 'cr1')],
    'cr2': [(4, 'cr2')],
    }


channels = ['sr', 'sb', 'cr1', 'cr2']


prefix = ['rJpsi']
era = ['2018']
Nbins = data_sb.GetXaxis().GetNbins()

print 'mu-value = ', mu
print '# of bins = ', Nbins
#print 'sf = ', sf

extraStr = ''

for chn in channels:

    cb.AddObservations(['*'], prefix, era, [chn], categories[chn])

    cb.AddProcesses(['*'], prefix, era, [chn], bkg_procs, categories[chn], False)
    cb.AddProcesses(['90'], prefix, era, [chn], sig_procs, categories[chn], True)

    bg_processes = [ 'bg_bin{}'.format(i+1) for i in range(Nbins) ]
    cb.AddProcesses(['*'], prefix, era, [chn], bg_processes, categories[chn], False)
    
    for i in range(1, Nbins+1):
        if chn in ['sb', 'cr1', 'cr2']:

            init = file.Get(chn + '/data_obs').GetBinContent(i) - mu*(file.Get(chn + '/signal').GetBinContent(i)) - file.Get(chn + '/bg_bc').GetBinContent(i)
            
            print i, init
#            extraStr += 'yield_bg_sb_bin{0} rateParam sb bg_bin{0} '.format(i) + str(init) + ' [' + str(init*1.2) +  ',' + str(init*1.2) + ']\n'
#            extraStr += 'yield_bg_sb_bin{0} rateParam sb bg_bin{0} '.format(i) + str(init) + ' [-50,' + str(init*2) + ']\n'
            extraStr += 'yield_bg_' + chn + '_bin{0}'.format(i) + ' rateParam ' + chn + ' bg_bin{0}'.format(i) + ' '+ str(init) + ' [-50,100000]\n'
#            extraStr += 'yield_bg_' + chn + '_bin{0} rateParam '.format(i) + chn + ' bg_bin{0} '.format(i) + str(init) + ' [-50,1000]\n'
#            extraStr += 'yield_bg_sb_bin{0} rateParam sb bg_bin{0} '.format(i) + str(init) + '\n'
#            extraStr += 'yield_bg_' + chn + '_bin{0} rateParam '.format(i) + chn + ' bg_bin{0} 1.\n'.format(i)


        elif chn=='sr':
#            extraStr += 'correction_sr_bin{0} rateParam sr bg_bin{0} '.format(i) + str(ratio.GetBinContent(i)) + ' [' + str(ratio.GetBinContent(i)) + ']\n'
            extraStr += 'yield_bg_' + chn + '_bin' + str(i) + ' rateParam ' + chn + ' bg_bin{0} (@0*@1/@2) yield_bg_sb_bin{0},yield_bg_cr1_bin{0},yield_bg_cr2_bin{0}'.format(i) + '\n'

print '>> Adding systematic uncertainties...'


#cb.cp().bin_id([1]).process(procs['sig'] + ['ZJ', 'ZL', 'TTJ', 'VV', 'STT', 'STJ', 'TTT', 'ZTT']).AddSyst(

cb.cp().process(['signal', 'bg_bc']).AddSyst(
    cb, 'CMS_lumi', 'lnN', ch.SystMap()(1.025))

cb.cp().process(bkg_procs).AddSyst(
    cb, 'CMS_bkg', 'lnN', ch.SystMap()(1.05))


# mu->tau fakes and QCD norm should be added


print '>> Extracting histograms from input root files...'
#file = aux_shapes + 'datacard_combine_1p.root'

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
command = 'combineCards.py'

for cat, clist in categories.items():
    command += " " + clist[0][1] + '=' + outdir + '/rJpsi_' + clist[0][1] + '_' + str(clist[0][0]) + '_2018_90.txt'

command += " > " + outcard

print command 

os.system(command)

# overwrite extra rateParam
if os.path.isfile(outcard):

    f = open(outcard, 'a')
    f.write(extraStr)
    f.write('* autoMCStats 0 1\n')
    f.close()

command2 = 'text2workspace.py ' + outcard + ' -o ' + outdir + '/workspace_mu' + str(mu).replace('.0','') + '.root -m 90'
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


