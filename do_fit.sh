#toy="-t -1 --expectSignal 0.71"
toy=""
workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
#option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --rMin 0 --rMax 2"
option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --rMin -1 --rMax 3"
save="--plots --saveShapes  --saveNormalizations --saveWithUncertainties"

cd datacard

#combine -M FitDiagnostics --plots --robustFit 1 --saveShapes  --saveNormalizations --saveWithUncertainties --rMin -0.2 --rMax 1  rJpsi_2018_90_gamma.txt ${toy}
combine -M FitDiagnostics --robustFit 1  --saveShapes --saveWithUncertainties ${option} ${workspace} ${toy}
#combine -M FitDiagnostics --robustFit 1 --rMin -5  --rMax 5 rJpsi_2018_90.txt ${toy}
#combine -M FitDiagnostics --robustFit 1 ${range} ${card} ${toy}
cd -
