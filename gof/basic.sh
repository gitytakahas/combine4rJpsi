workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"

for method in "KS" "saturated"
do
    combine -M GoodnessOfFit ${workspace} --algo=${method} -n _${method} --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
done
