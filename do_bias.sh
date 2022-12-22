workspace="combine_all.root"
trial="10"
toy="-t ${trial} --expectSignal 0.71"

#python setup.py --year all

#cd output/sm_cards/LIMITS/
cd datacard

combine ${workspace} -M GenerateOnly --bypassFrequentistFit --toysFrequentist ${toy} --saveToys -m 125 -s 123456 --setParameters bc=1,bkg=1 --freezeParameters bc,bkg


combine ${workspace} -M FitDiagnostics --toysFrequentist --toysFile higgsCombineTest.GenerateOnly.mH125.123456.root -t ${trial} --rMin -10. --rMax 10. --cminDefaultMinimizerStrategy=0

cd -

#python draw_bias.py
