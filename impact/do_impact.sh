workspace="/t3home/ytakahas/work/combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
#toy="-t -1 --expectSignal 0.71"
toy=""

#rm -rf impact
#mkdir -p impact
#cp ../datacard/${workspace} .

#cd impact 

combineTool.py -M Impacts -d ${workspace} -m 125 --doInitialFit --robustFit 1 ${toy} --rMin -10

combineTool.py -M Impacts -d ${workspace} -m 125 --doFits --robustFit 1 ${toy} --rMin -10 --job-mode slurm --task-name rjpsi --job-dir jobs --merge 1 --sub-opts '--partition standard --time 12:00:00'

#combineTool.py -M Impacts -d ${workspace} -m 125 -o impacts.json ${toy}
#plotImpacts.py -i impacts.json -o impacts --blind
#convert -density 160 -trim impacts.pdf[0] -quality 100 impacts.png


#cd -
