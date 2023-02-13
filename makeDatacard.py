from ROOT import TFile
from optparse import OptionParser, OptionValueError

usage = "usage: python compare.py" 
parser = OptionParser(usage) 
parser.add_option('-b', '--bbb', action="store_true", default=True, dest='bbb')
parser.add_option('-s', '--scale', action="store_true", default=False, dest='scale')
parser.add_option("-y", "--year", default="all", type="string", dest="year")
(options, args) = parser.parse_args() 

eras = ['2016', '2017', '2018']
if options.year!='all':
    eras = [options.year]


filename = "/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/tau_rhomass_unrolled_var.root"

if options.scale:
    filename = "/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/combine_sb3p5_sr4_simultaneous/tau_rhomass_unrolled_var_scaled.root"

input_file = TFile(filename)

bins = []

for year in eras:
#for year in ['2018']:
    for cat in ['sr', 'sb']:
        bins.append('tauhad_' + cat + '_' + year)


processes = ['jpsi_tau', 'bc_others', 'jpsi_hc', 'fakes']


#with open('rJpsi_2018_90_template.txt') as f:
#    data_lines = f.read()
    

#for bin in bins:
#    for process in processes:

#        print(bin.lower() + '/' + process)

#        hist = input_file.Get(bin.lower() + '/' + process)
#        print hist

#        data_lines = data_lines.replace('REP_' + process + '_' + bin, '{0:.2f}'.format(hist.Integral()))

from collections import OrderedDict

sysdict = OrderedDict()

for year in eras:
    sysdict['fakeNorm_' + year] = {'type':'lnN', 'proc':['fakes'], 'size':1.3}
    sysdict['trigger_' + year] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.03}
    sysdict['sfIdJpsi_' + year] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.03}

    if year!='2018':
        sysdict['bcnorm_' + year] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.3}


    if year=='2018':
        sysdict['sfReco'] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.03}
    else:
        sysdict['sfReco_' + year] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.03}


sysdict['bccorr'] = {'type':'shape', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.0}
sysdict['bglvar_e0'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e1'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e2'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e3'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e4'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e5'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e6'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e7'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e8'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['bglvar_e9'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['br_jpsi_hc_over_mu'] = {'type':'lnN', 'proc':['jpsi_hc'], 'size':1.38}
sysdict['br_others'] = {'type':'lnN', 'proc':['bc_others'], 'size':1.5}
sysdict['ctau'] = {'type':'shape', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.0}
sysdict['puWeight'] = {'type':'shape', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.0}
sysdict['tauBr'] = {'type':'shape', 'proc':['jpsi_tau'], 'size':1.0}
sysdict['tauReco'] = {'type':'lnN', 'proc':['jpsi_tau', 'bc_others', 'jpsi_hc'], 'size':1.05}


nbins = None

output='datacard/datacard_tauhad_' + options.year + '.txt'

if options.scale:
    output='datacard/datacard_tauhad_' + options.year + '_scale.txt'

with open(output, mode="w") as f:
    f.write('imax ' + str(len(bins)) + '\n')
    f.write('jmax ' + str(len(processes)-1) + '\n')

    hist_ = input_file.Get(bins[-1].lower() + '/data_obs')
    nbins = hist_.GetXaxis().GetNbins()
    print 'nbin=', nbins

    if options.bbb:
        total = len(sysdict) + len(bins)*(len(processes)-1)*nbins
        print 'total=', total
        f.write('kmax ' + str(total) + '\n')
    else:
        f.write('kmax ' + str(len(sysdict)) + '\n')

    f.write('-'*80 + '\n')

    for bin in bins:
        if options.scale:
            f.write('shapes \t * \t ' + bin + ' \t param_tauhad_ws_scale.root wspace:$PROCESS_' + bin + ' wspace:$PROCESS_$SYSTEMATIC_' + bin + '\n')
        else:
            f.write('shapes \t * \t ' + bin + ' \t param_tauhad_ws.root wspace:$PROCESS_' + bin + ' wspace:$PROCESS_$SYSTEMATIC_' + bin + '\n')

    if options.scale:
        f.write('shapes \t data_obs \t tauhad_* \t param_tauhad_ws_scale.root wspace:$PROCESS wspace:$PROCESS_$SYSTEMATIC \n')
    else:
        f.write('shapes \t data_obs \t tauhad_* \t param_tauhad_ws.root wspace:$PROCESS wspace:$PROCESS_$SYSTEMATIC \n')

    f.write('-'*80 + '\n')

    f.write('bin \t')
    for bin in bins:    
        f.write(bin + '\t')
    f.write('\n')

    f.write('observation \t')
    for bin in bins:    
        hist = input_file.Get(bin.lower() + '/data_obs')
#        nbins = hist.GetXaxis().GetNbins()
        f.write(str(int(hist.Integral())) + '\t')
    f.write('\n')

    f.write('-'*80 + '\n')

    f.write('bin \t')
    for bin in bins:    
        for process in processes:
            f.write(bin + '\t')
    f.write('\n')

    f.write('process \t')
    for bin in bins:    
        for process in processes:
            f.write(process + '\t')
    f.write('\n')

    f.write('process \t')
    for bin in bins:    
        for ip, process in enumerate(processes):
            f.write(str(ip) + '\t')
    f.write('\n')

    f.write('rate \t')
    for bin in bins:    
        for ip, process in enumerate(processes):
            if process=='fakes':
                f.write('1\t')
            else:
                hist = input_file.Get(bin.lower() + '/' + process)
                f.write('{0:.2f}'.format(hist.Integral()) + '\t')
    f.write('\n')

    f.write('-'*80 + '\n')

    for nuisance, var in sysdict.items():
        f.write(nuisance + ' \t' + var['type'] + '\t')

        for bin in bins:    
            for process in processes:
            
                wstr = '-'
                if process in var['proc']:
                    wstr = str(var['size'])

                if nuisance.find('fakeNorm')!=-1 and process == 'fakes':
                    if bin.find('sb')!=-1: wstr = '-'
                    if bin.find('sr')!=-1:
                        _year = bin.split('_')[2]
                        _year2 = nuisance.split('_')[1]
                        if _year != _year2: wstr = '-'

                if nuisance.find('bcnorm')!=-1 and process in var['proc']:
                    _year = bin.split('_')[2]
                    _year2 = nuisance.split('_')[1]
                    if _year != _year2: wstr = '-'

                f.write(wstr + '\t')
        f.write('\n')



    if options.bbb:

        for bin_bbb in bins:
            for process_bbb in processes:

                if process_bbb=='fakes': continue
                for ii in range(nbins):
                
                    dstr = process_bbb + '_bbb' + str(ii+1) + bin_bbb + '\t shape'
                
                    for bin in bins:                
                        for process in processes:
                            if process==process_bbb and bin_bbb==bin:
                                dstr += '\t 1.0'
                            else:
                                dstr += '\t -'
                    f.write(dstr + '\n')


    for bin in bins:    
        for process in processes:
            if process=='fakes': continue
            f.write('bc \t rateParam \t ' + bin + '\t' + process + '\t 1 \n')


    for bin in bins:    
        if bin.find('sb')==-1: continue
        for ii in range(nbins):
            f.write('bg_bin' + str(ii+1) + '_' + bin + ' \t flatParam\n')


    f.write('syst group = ')

    for nuisance, var in sysdict.items():        
        f.write(nuisance + ' ')

    f.write('\n')




#        for ii in range(144):
#            f.write('jpsi_tau_bbb' + str(ii+1) + '\t  shape \t 1.0 \t - \t - \t - \t - \t - \t - \t -\n')
#        for ii in range(144):
#            f.write('bc_others_bbb' + str(ii+1) + '\t  shape \t - \t 1.0 \t - \t - \t - \t - \t - \t -\n')
#        for ii in range(144):
#            f.write('jpsi_hc_bbb' + str(ii+1) + '\t  shape \t - \t - \t 1.0 \t - \t - \t - \t - \t -\n')
#        for ii in range(144):
#            f.write('jpsi_tau_bbb' + str(ii+1) + '\t  shape \t - \t - \t - \t - \t 1.0 \t - \t - \t -\n')
#        for ii in range(144):
#            f.write('bc_others_bbb' + str(ii+1) + '\t  shape \t - \t - \t - \t - \t - \t 1.0 \t - \t -\n')
#        for ii in range(144):
#            f.write('jpsi_hc_bbb' + str(ii+1) + '\t  shape \t - \t - \t - \t - \t - \t - \t 1.0 \t -\n')















#bin                                sr               sr               sr               sr               sr               sb               sb               sb               sb             sb
#process                            bc_jpsi_tau_3p   bc_others        bc_jpsi_tau_N3p  bc_jpsi_dst      fakes            bc_jpsi_tau_3p   bc_others        bc_jpsi_tau_N3p  bc_jpsi_dst    fakes
#process                            0                1                2                3                4                0                1                2                3              4
#rate                               501.57           169.845          76.0048          760.739          1                478.768          468.33           126.007          1028.05        1
#----------------------------------------------------------------------------------------------------------------------------------
#fakeNorm                lnN         -               -                -                -                1.03	        -                -                -                -              -
#bbb			shape	    -		    -		     -		      -		       1.0		-		 -		  -		   -		  -
#BcPt                    shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#br_BcJpsiDst            shape      -                -                -                1.0              -                -                -                -                1.0            -
#hammer_ebe_e0           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e1           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e2           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e3           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e4           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e5           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e6           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e7           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e8           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#hammer_ebe_e9           shape      1.0              -                1.0              -                -                1.0              -                1.0              -              -
#muSFID                  shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#muSFReco                shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#puweight                shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#tauBr                   shape      1.0              -                -                -                -                1.0              -                -                -              -
#tauReco                 shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#weight_ctau             shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#xgbsEff                 shape      1.0              1.0              1.0              1.0              -                1.0              1.0              1.0              1.0            -
#bc_jpsi_tau_3p_bbb1	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb2	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb3	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb4	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb5	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb6	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb7	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb8	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb9	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb10	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb11	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb12	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb13	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb14	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb15	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb16	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb17	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb18	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb19	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb20	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb21	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb22	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb23	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb24	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb25	shape	   1.0		    -		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb1		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb2		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb3		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb4		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb5		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb6		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb7		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb8		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb9		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb10		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb11		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb12		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb13		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb14		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb15		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb16		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb17		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb18		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb19		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb20		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb21		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb22		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb23		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb24		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_others_bbb25		shape	   -  		    1.0		     -		      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb1	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb2	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb3	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb4	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb5	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb6	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb7	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb8	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb9	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb10	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb11	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb12	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb13	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb14	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb15	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb16	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb17	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb18	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb19	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb20	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb21	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb22	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb23	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb24	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_tau_N3p_bbb25	shape	   -  		    -		     1.0	      -		       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb1	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb2	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb3	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb4	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb5	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb6	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb7	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb8	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb9	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb10	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb11	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb12	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb13	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb14	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb15	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb16	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb17	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb18	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb19	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb20	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb21	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb22	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb23	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb24	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_dst_bbb25	shape	   -  		    -		     -  	      1.0	       -		-		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb1	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb2	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb3	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb4	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb5	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb6	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb7	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb8	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb9	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb10	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb11	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb12	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb13	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb14	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb15	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb16	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb17	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb18	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb19	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb20	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb21	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb22	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb23	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb24	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_jpsi_tau_3p_bbb25	shape	   -  		    -		     -		      -		       -		1.0		 -		  -		   -		  -
#bc_others_bbb1		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb2		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb3		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb4		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb5		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb6		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb7		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb8		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb9		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb10		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb11		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb12		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb13		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb14		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb15		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb16		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb17		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb18		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb19		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb20		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb21		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb22		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb23		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb24		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_others_bbb25		shape	   -  		    -  		     -		      -		       -		-		 1.0		  -		   -		  -
#bc_jpsi_tau_N3p_bbb1	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb2	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb3	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb4	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb5	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb6	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb7	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb8	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb9	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb10	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb11	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb12	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb13	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb14	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb15	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb16	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb17	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb18	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb19	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb20	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb21	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb22	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb23	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb24	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_tau_N3p_bbb25	shape	   -  		    -		     -  	      -		       -		-		 -		  1.0		   -		  -
#bc_jpsi_dst_bbb1	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb2	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb3	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb4	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb5	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb6	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb7	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb8	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb9	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb10	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb11	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb12	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb13	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb14	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb15	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb16	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb17	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb18	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb19	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb20	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb21	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb22	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb23	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb24	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#bc_jpsi_dst_bbb25	shape	   -  		    -		     -  	      -  	       -		-		 -		  -		   1.0		  -
#syst group = hammer_ebe_e2 hammer_ebe_e3 hammer_ebe_e0 hammer_ebe_e1 hammer_ebe_e6 hammer_ebe_e7 hammer_ebe_e4 hammer_ebe_e5 hammer_ebe_e8 hammer_ebe_e9 BcPt tauReco br_BcJpsiDst weight_ctau xgbsEff muSFReco puweight muSFID tauBr
#bg_bin1_sb  flatParam
#bg_bin2_sb  flatParam
#bg_bin3_sb  flatParam
#bg_bin4_sb  flatParam
#bg_bin5_sb  flatParam
#bg_bin6_sb  flatParam
#bg_bin7_sb  flatParam
#bg_bin8_sb  flatParam
#bg_bin9_sb  flatParam
#bg_bin10_sb  flatParam
#bg_bin11_sb  flatParam
#bg_bin12_sb  flatParam
#bg_bin13_sb  flatParam
#bg_bin14_sb  flatParam
#bg_bin15_sb  flatParam
#bg_bin16_sb  flatParam
#bg_bin17_sb  flatParam
#bg_bin18_sb  flatParam
#bg_bin19_sb  flatParam
#bg_bin20_sb  flatParam
#bg_bin21_sb  flatParam
#bg_bin22_sb  flatParam
#bg_bin23_sb  flatParam
#bg_bin24_sb  flatParam
#bg_bin25_sb  flatParam

