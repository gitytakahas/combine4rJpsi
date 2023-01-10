toy="-t -1 --expectSignal 0.71"
range="--rMin -3 --rMax 3"
card="combine_all.txt"

cd datacard

#combine -M FitDiagnostics --plots --robustFit 1 --saveShapes  --saveNormalizations --saveWithUncertainties --rMin -0.2 --rMax 1  rJpsi_2018_90_gamma.txt ${toy}
#combine -M FitDiagnostics --plots --robustFit 1 --saveShapes  --saveNormalizations --saveWithUncertainties --rMin -0.2 --rMax 1  rJpsi_2018_90.txt ${toy}
#combine -M FitDiagnostics --robustFit 1 --rMin -5  --rMax 5 rJpsi_2018_90.txt ${toy}
combine -M FitDiagnostics --robustFit 1 ${range} ${card} ${toy}
cd -
