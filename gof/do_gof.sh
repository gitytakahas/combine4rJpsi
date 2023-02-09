workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
signal_for_gof="--fixedSignalStrength=0.71"
#signal_for_gof="--fixedSignalStrength=0."
ntoys="250"

#method="KS"
#method="saturated"

#for method in "KS" "saturated"
#cd datacard 

for method in "KS" "saturated"
do
#    combine -M GoodnessOfFit ${workspace} --algo=${method} -n _${method} --rMin -3 --rMax 3 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
    
    hadd -f higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.*.root

    combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root -o combine_${method}.json
    
    plotGof.py combine_${method}.json --statistic ${method} --mass 125.0 -o gof_plot --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="combined"
done

#cd -

