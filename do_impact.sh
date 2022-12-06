workspace="workspace.root"
#toy="-t -1 --expectSignal 0.71"
toy=""

#python setup.py

cd output/sm_cards/LIMITS/

combineTool.py -M Impacts -d ${workspace} -m 90 --doInitialFit --robustFit 1 ${toy}
combineTool.py -M Impacts -d ${workspace} -m 90 --doFits --robustFit 1 ${toy}
combineTool.py -M Impacts -d ${workspace} -m 90 -o impacts.json ${toy}
plotImpacts.py -i impacts.json -o impacts --blind

cd -
