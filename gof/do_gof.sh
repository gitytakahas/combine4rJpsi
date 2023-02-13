workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
signal_for_gof="--fixedSignalStrength=0.71"
#signal_for_gof="--fixedSignalStrength=0."
ntoys="250"
#option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1"

#method="KS"
#method="saturated"

#for method in "KS" "saturated"
#cd datacard 

for method in "KS" "saturated"
#for method in "KS"
do
#    combine -M GoodnessOfFit ${workspace} --algo=${method} -n _${method} --rMin -3 --rMax 3 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
    
    hadd -f higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.*.root

    combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root -o combine_${method}.json
    
    plotGof.py combine_${method}.json --statistic ${method} --mass 125.0 -o gof_plot --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="combined"
done

#cd -

