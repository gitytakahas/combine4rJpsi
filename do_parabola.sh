workspace="workspace.root"
toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
range="--rMin 0.1 --rMax 2."

python setup.py
cd output/sm_cards/LIMITS/


combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${range}

#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst --freezeNuisanceGroups syst ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.syst.bbb --freezeNuisanceGroups syst,bbb ${range}

plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others  "higgsCombine.freeze.lumi.syst.${method}.mH120.root:Freeze Syst:2" "higgsCombine.freeze.lumi.syst.${method}.mH120.root:Freeze Syst-bbb:4" --breakdown "Syst,bbb,Stat"


cd -


