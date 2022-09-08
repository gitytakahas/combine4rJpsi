workspace="workspace.root"
toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
range="--rMin 0.1 --rMax 2."

python setup.py
cd output/sm_cards/LIMITS/


combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi.syst --freezeNuisanceGroups lumi,syst ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi.syst.bbb --freezeNuisanceGroups lumi,syst,bbb ${range}

plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others "higgsCombine.freeze.lumi.${method}.mH120.root:Freeze Lumi:2" "higgsCombine.freeze.lumi.syst.${method}.mH120.root:Freeze Lumi-Syst:4" "higgsCombine.freeze.lumi.syst.bbb.${method}.mH120.root:Freeze Lumi-Syst-bbb:6" --breakdown "Lumi,Syst,bbb,Stat"

cd -


