toy="-t -1 --expectSignal 0.71"
#combine -M FitDiagnostics --plots --robustFit 1 --saveShapes  --saveNormalizations --saveWithUncertainties --rMin -0.2 --rMax 1  rJpsi_2018_90_gamma.txt ${toy}
combine -M FitDiagnostics --plots --robustFit 1 --saveShapes  --saveNormalizations --saveWithUncertainties --rMin -0.2 --rMax 1  rJpsi_2018_90.txt ${toy}
