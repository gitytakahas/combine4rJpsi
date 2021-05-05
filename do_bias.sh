#python setup.py

cd output/sm_cards/LIMITS/

combine workspace_mu1.root -M GenerateOnly --toysFrequentist -t 400 --expectSignal 0.71 --saveToys -m 90
combine workspace_mu1.root -M FitDiagnostics --toysFile higgsCombineTest.GenerateOnly.mH90.123456.root -t 400 --rMin -0.1 --rMax 2 --cminDefaultMinimizerStrategy=0

cd -

