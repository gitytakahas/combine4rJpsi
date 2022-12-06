workspace="workspace.root"
signal_for_gof="--fixedSignalStrength=0.71"
#signal_for_gof="--fixedSignalStrength=0."
ntoys="250"

python setup.py

#method="KS"
#method="saturated"

cd output/sm_cards/LIMITS/

for method in "KS" "saturated"
do
    combine -M GoodnessOfFit ${workspace} --algo=${method} -n _${method} --rMin -2 --rMax 2 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 90
    
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys -s 1234 --rMin -2 --rMax 2 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 90
    
    combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH90.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH90.1234.root -o rjpsi_${method}.json
    
    plotGof.py rjpsi_${method}.json --statistic ${method} --mass 90.0 -o gof_plot --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="combined"
done

cd -

