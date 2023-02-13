#!/bin/bash
# 
#SBATCH -p short
#SBATCH --account=t3
#SBATCH --time 01:00:00
#SBATCH -e cn-test.err  # replace default slurm-SLURM_JOB_ID.err
#SBATCH -o cn-test.out  # replace default slurm-SLURM_JOB_ID.out

workspace="/work/ytakahas/work/Combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
signal_for_gof="--fixedSignalStrength=0.71"
ntoys="20"
#option="--setRobustFitAlgo=Minuit2 --setRobustFitStrategy=0 --setRobustFitTolerance=0.2 --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:0.5 --cminFallbackAlgo Minuit2,0:1.0 --cminPreScan --cminPreFit 1 --rMin 0 --rMax 2"


echo HOME: $HOME 
echo USER: $USER 
echo SLURM_JOB_ID: $SLURM_JOB_ID
echo HOSTNAME: $HOSTNAME

# each worker node has local /scratch space to be used during job run
mkdir -p /scratch/$USER/${SLURM_JOB_ID}
export TMPDIR=/scratch/$USER/${SLURM_JOB_ID}


for method in "KS" "saturated"
do
#    combine -M GoodnessOfFit ${workspace} --algo=${method} -n _${method} --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
    
    combine -M GoodnessOfFit ${workspace} --algo=${method} -t ${ntoys} -n _${method}_unblindToys -s -1 --toysFrequentist --cminDefaultMinimizerStrategy 0 ${signal_for_gof} -m 125
done

#combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${method}.GoodnessOfFit.mH125.root higgsCombine_${method}_unblindToys.GoodnessOfFit.mH125.1234.root -o combine_${method}.json

#plotGof.py combine_${method}.json --statistic ${method} --mass 125.0 -o gof_plot --title-right="138 fb^{-1} (Run-3, 13 TeV)" --title-left="combined"




#python draw.py --year YEARTOBEFILLED --min --sys SYSTEMATIC --outdir $TMPDIR/

#ls -lart $TMPDIR

#xrdcp -f $TMPDIR root://t3dcachedb03.psi.ch/OUTDIRECTORY

# cleaning of temporal working dir when job was completed:
#rm -rf ${TMPDIR}

date
