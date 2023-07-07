workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
signal_for_gof="--fixedSignalStrength=0.71"
#signal_for_gof="--fixedSignalStrength=0."
#option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1"


for method in "KS" "saturated"
do   

    echo $method
    
    hadd -f higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.*.root

    combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.root -o combine_${method}.json
    
    plotGof.py combine_${method}.json --statistic ${method} --mass 125.0 -o gof_plot --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="combined"
done



for method in "saturated"
do
    for year in 2016 2017 2018
    do   
	
	echo $method

	hadd -f higgsCombine_${method}_unblindToys_${year}only.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys_${year}only.GoodnessOfFit.mH125.*.root
	
	combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys_${year}only.GoodnessOfFit.mH125.root -o combine_${method}_${year}only.json
	
	plotGof.py combine_${method}_${year}only.json --statistic ${method} --mass 125.0 -o gof_plot_${year} --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="${method}, ${year}"
    done
done



