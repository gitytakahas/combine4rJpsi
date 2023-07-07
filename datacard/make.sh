mask="--channel-masks"

for year in 2016 2017 2018 all 
#for year in all
do
    
    target="combine_${year}.txt"
    target_root="combine_${year}.root"
    dc_had="datacard_tauhad_${year}.txt"
    dc_lep="datacard_taulep_2018.txt"
    
    echo "combinecards"
    combineCards.py tauhad=${dc_had} taulep=${dc_lep} > ${target}
    echo "text2workspace"
    text2workspace.py ${target} -o ${target_root} -m 125 ${mask}
done



for year in 2016 2017 2018 all 
do
    
    target="combine_${year}_scale.txt"
    target_root="combine_${year}_scale.root"
    dc_had="datacard_tauhad_${year}_scale.txt"
    dc_lep="datacard_taulep_2018_scale.txt"

    combineCards.py tauhad=${dc_had} taulep=${dc_lep} > ${target}
    text2workspace.py ${target} -o ${target_root} -m 125 ${mask}
done

# individual
text2workspace.py datacard_tauhad_all_scale.txt -o datacard_tauhad_all_scale.root -m 125 ${mask}
text2workspace.py datacard_taulep_2018_scale.txt -o datacard_taulep_2018_scale.root -m 125 ${mask}

text2workspace.py datacard_tauhad_all.txt -o datacard_tauhad_all.root -m 125 ${mask}
text2workspace.py datacard_taulep_2018.txt -o datacard_taulep_2018.root -m 125 ${mask}
