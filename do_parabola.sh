toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
#range="--rMin -5 --rMax 5."
range="--autoRange 3 --rMin -3"

cd datacard

for year in 2016 2017 2018 all
#for year in 2018
do
    
    
    workspace="combine_${year}.root"
    
    combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${range}
    combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst --freezeNuisanceGroups syst ${range} --fastScan 

    plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others  "higgsCombine.freeze.syst.${method}.mH120.root:Freeze Syst:2" --breakdown "Syst,Stat" --output parabola_comb_${year}


done

cd -


#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
