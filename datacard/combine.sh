toy="-t -1 --expectSignal 0.71"

for year in 2016 2017 2018 all 
#for year in 2018
do
    
    target="combine_${year}.txt"
    target_root="combine_${year}.root"
    dc_had="datacard_tauhad_${year}.txt"
    dc_lep="datacard_taulep_2018.txt"

    combineCards.py tauhad=${dc_had} taulep=${dc_lep} > ${target}
    text2workspace.py ${target} -o ${target_root} -m 125
done

#combine -M FitDiagnostics --robustFit 1 --rMin -5  combine.txt ${toy}
