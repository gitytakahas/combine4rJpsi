#!/bin/bash
# 
#SBATCH -p standard
#SBATCH --account=t3
#SBATCH --time 05:00:00
#SBATCH -e cn-test.err  # replace default slurm-SLURM_JOB_ID.err
#SBATCH -o cn-test.out  # replace default slurm-SLURM_JOB_ID.out


workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
signal_for_gof="--fixedSignalStrength=0.71"
ntoys="20"


echo HOME: $HOME 
echo USER: $USER 
echo SLURM_JOB_ID: $SLURM_JOB_ID
echo HOSTNAME: $HOSTNAME

# each worker node has local /scratch space to be used during job run
mkdir -p /scratch/$USER/${SLURM_JOB_ID}
export TMPDIR=/scratch/$USER/${SLURM_JOB_ID}





for method in "KS"
do
    echo $method
    
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
done


for method in "saturated"
do

    echo $method
    
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys_2016only -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125 --setParametersForEval mask_tauhad_tauhad_sr_2016=0,mask_tauhad_tauhad_sb_2016=0,mask_tauhad_tauhad_sr_2017=1,mask_tauhad_tauhad_sb_2017=1,mask_tauhad_tauhad_sr_2018=1,mask_tauhad_tauhad_sb_2018=1
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys_2017only -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125 --setParametersForEval mask_tauhad_tauhad_sr_2016=1,mask_tauhad_tauhad_sb_2016=1,mask_tauhad_tauhad_sr_2017=0,mask_tauhad_tauhad_sb_2017=0,mask_tauhad_tauhad_sr_2018=1,mask_tauhad_tauhad_sb_2018=1
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys_2018only -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125 --setParametersForEval mask_tauhad_tauhad_sr_2016=1,mask_tauhad_tauhad_sb_2016=1,mask_tauhad_tauhad_sr_2017=1,mask_tauhad_tauhad_sb_2017=1,mask_tauhad_tauhad_sr_2018=0,mask_tauhad_tauhad_sb_2018=0

done


date
