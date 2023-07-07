workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all_scale.root"
#workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/datacard_taulep_2018.root"
#workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/datacard_tauhad_all_scale.root"
#workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/datacard_taulep_2018_scale.root"
#toy="-t -1 --expectSignal 0.71"
toy=""

#rm -rf impact
#mkdir -p impact
#cp ../datacard/${workspace} .

#cd impact 

#combineTool.py -M Impacts -d ${workspace} -m 125 --doInitialFit --robustFit 1 ${toy} --rMin -10

#combineTool.py -M Impacts -d ${workspace} -m 125 --doFits --robustFit 1 ${toy} --rMin -10 --job-mode slurm --task-name rjpsi --job-dir jobs --merge 1 --sub-opts '--partition standard --time 12:00:00'

#file="impacts_lep_scale.json"
file="impacts_comb_scale.json"

combineTool.py -M Impacts -d ${workspace} -m 125 -o ${file} ${toy}
plotImpacts.py -i ${file} -o impacts --blind
#plotImpacts.py -i ${file} -o impacts

for ii in 0 1 2 3 4
do
    convert -density 160 -trim impacts.pdf[${ii}] -quality 100 impacts_${ii}.png
done

#cd -
