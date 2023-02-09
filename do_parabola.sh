toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --autoRange 3 --rMin -3"
#option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --rMin 0 --rMax 2"

cd datacard

for year in 2016 2017 2018 all
#for year in 2018
do
    
    
    workspace="combine_${year}.root"
#    workspace="datacard_tauhad_${year}.txt"
    
    combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${option}
    combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst --freezeNuisanceGroups syst ${option} --fastScan 

    plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others  "higgsCombine.freeze.syst.${method}.mH120.root:Freeze Syst:2" --breakdown "Syst,Stat" --output parabola_comb_${year}


done

cd -


#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
