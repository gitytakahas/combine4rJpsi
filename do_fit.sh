#python setup_simultaneous.py
python setup.py

toy="-t -1 --expectSignal 0.71"

cd output/sm_cards/LIMITS/

combine -M FitDiagnostics workspace.root --robustFit=1 --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND  --cminPreScan --cminDefaultMinimizerStrategy 0 --saveShapes --rMin -0.1 --rMax 2. ${toy}

cd -

#python draw.py
