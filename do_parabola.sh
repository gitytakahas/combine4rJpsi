workspace="workspace_mu1.root"
toy="-t -1 --expectSignal 0.71"
method="MultiDimFit"
range="--rMin 0.1 --rMax 2."
cd output/sm_cards/LIMITS/


combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .nominal ${range}
#combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi --freezeNuisanceGroups lumi ${range}
combine -M ${method} ${workspace} --robustFit=1 ${toy} --algo grid -n .freeze.lumi.syst --freezeNuisanceGroups syst ${range}

plot1DScan.py higgsCombine.nominal.${method}.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others  "higgsCombine.freeze.lumi.syst.${method}.mH120.root:Freeze Lumi-Syst:4" --breakdown "Syst,Stat"

#combine -M MultiDimFit workspace_mu1.root  -t -1 --expectSignal 1 --robustFit=1 -n .nominal --rMin 0 --rMax 2

#plot1DScan.py output/sm_cards/LIMITS/higgsCombine.nominal.MultiDimFit.mH120.root --POI "r" -o nominal.es --logo 'CMS' --logo-sub 'Internal' --others "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.MultiDimFit.mH120.root:Freeze Lumi:2" "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.syst.MultiDimFit.mH120.root:Freeze Lumi-Syst:4" --breakdown "Lumi,Syst,Stat"

cd -


