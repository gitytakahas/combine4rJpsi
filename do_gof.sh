workspace="workspace.root"
#signal_for_gof="--fixedSignalStrength=0.71"
signal_for_gof="--fixedSignalStrength=0."
ntoys="500"

#python setup.py

cd output/sm_cards/LIMITS/

combine -M GoodnessOfFit ${workspace} --algo=saturated -n _saturated --rMin -2 --rMax 2 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 90

combine -M GoodnessOfFit ${workspace} --algo=saturated -t ${ntoys} -n _saturated_unblindToys -s 1234 --rMin -2 --rMax 2 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 90

combineTool.py -M CollectGoodnessOfFit --input higgsCombine_saturated.GoodnessOfFit.mH90.root higgsCombine_saturated_unblindToys.GoodnessOfFit.mH90.1234.root -o rjpsi_saturated.json

plotGof.py rjpsi_saturated.json --statistic saturated --mass 90.0 -o gof_plot --title-right="59.5 fb^{-1} (2018, 13 TeV)" --title-left="combined"


cd -

