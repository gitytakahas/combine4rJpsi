workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all_scale.root"
#workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/datacard_tauhad_all_scale.root"
#workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/datacard_taulep_2018_scale.root"
#toy="-t -1 --expectSignal 0.71"
toy=""
option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --rMin -1 --rMax 3"

#rm -rf impact
#mkdir -p impact
#cp ../datacard/${workspace} .

#cd impact 

combineTool.py -M Impacts -d ${workspace} -m 125 --doInitialFit --robustFit 1 ${toy} ${option}

combineTool.py -M Impacts -d ${workspace} -m 125 --doFits --robustFit 1 ${toy} ${option} --job-mode slurm --task-name rjpsi --job-dir jobs --merge 1 --sub-opts '--partition standard --time 12:00:00'

#combineTool.py -M Impacts -d ${workspace} -m 125 -o impacts.json ${toy}
#plotImpacts.py -i impacts.json -o impacts --blind
#convert -density 160 -trim impacts.pdf[0] -quality 100 impacts.png


#cd -
