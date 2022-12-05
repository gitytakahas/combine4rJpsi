workspace="workspace.root"
toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
range="--rMin 0. --rMax 2."

python setup.py
cd output/sm_cards/LIMITS/


combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst --freezeNuisanceGroups syst ${range} --fastScan 
#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst.bbb --freezeParameters allConstrainedNuisances ${range}

plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others  "higgsCombine.freeze.syst.${method}.mH120.root:Freeze Syst:2" --breakdown "Syst,Stat"
#plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others "higgsCombine.freeze.syst.${method}.mH120.root:Freeze Syst:2" "higgsCombine.freeze.syst.bbb.${method}.mH120.root:Freeze All:4" --breakdown "Syst,All,Stat"




cd -



#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
