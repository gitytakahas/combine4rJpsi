#! /bin/bash
# Author: Izaak Neutelings (January 2022)
# ./resubmit_Impacts.sh `grep -L Done impacts/jobs/job_impacts*.log`
# ./resubmit_Impacts.sh `grep -le ':[^/]*[+-]0\.000/' -e '/[+-]0\.000[> ]' impacts/jobs/*.log`
# ./resubmit_Impacts.sh `grep -le ':[^/]*[+-]0\.000/' -e '/[+-]0\.000[> ]' impacts/jobs/*resub*.log`
function peval { echo ">>> $@"; eval "$@"; }

LOGS="$@"
echo ">>> \$LOGS=$LOGS"
#QUEUE="--partition standard --time 03:00:00"
QUEUE="--partition standard --time 08:00:00"
#QUEUE="--partition short" # --time 00:45:00"
NEWLOG="jobs/job_%x_%A.log"
EXTRAOPT="--X-rtd MINIMIZER_analytic --robustFit=1"
RMIN=0
RMAX="" #1.9

cd impacts
for log in $LOGS; do
  
  # SETTINGS
  echo ">>> Resubmitting $log..."
  FILE=`echo ${log/_resub/} | sed 's/_[0-9]*.log//g'`
  FILE=${FILE/impacts\//}
  SCRIPT="${FILE}.sh"
  NEWSCRIPT="$SCRIPT"
  JOBNAME=`basename ${FILE/job_/}`
  NEWJOBNAME="${JOBNAME}_resub"
  [ ! -e $SCRIPT ] && echo ">>> Did not find $SCRIPT..." && continue
  if [ "$EXTRAOPT" ]; then
    NEWSCRIPT="${NEWSCRIPT/.sh/_resub.sh}"
    eval "cp $SCRIPT $NEWSCRIPT"
    eval "sed 's/--algo impact/--algo impact $EXTRAOPT/g' -i $NEWSCRIPT"
    [ "$RMIN" ] && eval "sed 's/--rMin [0-9.-]\+/--rMin $RMIN/g' -i $NEWSCRIPT"
    [ "$RMAX" ] && eval "sed 's/--rMax [0-9.-]\+/--rMax $RMAX/g' -i $NEWSCRIPT"
  fi
  #echo ">>>   \$SCRIPT=$SCRIPT"
  #echo ">>>   \$NEWSCRIPT=$NEWSCRIPT"
  #echo ">>>   \$NEWLOG=$NEWLOG"
  #echo ">>>   \$JOBNAME=$JOBNAME"
  #echo ">>>   \$EXTRAOPT=$EXTRAOPT"
  
  # RESUBMIT
  peval "sbatch -J $NEWJOBNAME -o $NEWLOG $QUEUE $NEWSCRIPT"
  echo ">>> "
  
done