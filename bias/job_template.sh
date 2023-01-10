#!/bin/bash
# 
#SBATCH -p short
#SBATCH --account=t3
#SBATCH --time 01:00:00
#SBATCH -e cn-test.err  # replace default slurm-SLURM_JOB_ID.err
#SBATCH -o cn-test.out  # replace default slurm-SLURM_JOB_ID.out

workspace="/t3home/ytakahas/work/combination/CMSSW_10_2_13/src/CombineHarvester/combine4rJpsi_comb/datacard/combine_all.root"
trial="30"
toy="-t ${trial} --expectSignal 0.71"


echo HOME: $HOME 
echo USER: $USER 
echo SLURM_JOB_ID: $SLURM_JOB_ID
echo HOSTNAME: $HOSTNAME

# each worker node has local /scratch space to be used during job run
mkdir -p /scratch/$USER/${SLURM_JOB_ID}
export TMPDIR=/scratch/$USER/${SLURM_JOB_ID}


combine ${workspace} -M GenerateOnly --bypassFrequentistFit --toysFrequentist ${toy} --saveToys -m 125 -s SEED --setParameters bc=1,bkg=1 --freezeParameters bc,bkg


combine ${workspace} -M FitDiagnostics --toysFrequentist --toysFile higgsCombineTest.GenerateOnly.mH125.SEED.root -t ${trial} --cminDefaultMinimizerStrategy=0 -n SEED




#python draw.py --year YEARTOBEFILLED --min --sys SYSTEMATIC --outdir $TMPDIR/

#ls -lart $TMPDIR

#xrdcp -f $TMPDIR root://t3dcachedb03.psi.ch/OUTDIRECTORY

# cleaning of temporal working dir when job was completed:
#rm -rf ${TMPDIR}

date