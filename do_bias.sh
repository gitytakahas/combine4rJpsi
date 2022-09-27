workspace="workspace_lnN.root"
toy="-t 100 --expectSignal 0.71"

#python setup.py

#cd output/sm_cards/LIMITS/
cd workspace

#combine ${workspace} -M GenerateOnly --toysFrequentist --run blind ${toy} --saveToys -m 90
combine ${workspace} -M GenerateOnly --bypassFrequentistFit --toysFrequentist ${toy} --saveToys -m 90

combine ${workspace} -M FitDiagnostics --toysFrequentist --toysFile higgsCombineTest.GenerateOnly.mH90.123456.root -t 100 --rMin -2. --rMax 2. --cminDefaultMinimizerStrategy=0

cd -

