import subprocess, os, sys


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


cdir = os.getcwd()

import datetime

d_today = datetime.datetime.now()

d_today = str(d_today).split('.')[0]
d_today = d_today.replace(' ', '-').replace(':','')

print d_today



jobdir = cdir + '/job_' + d_today
#outdir = '/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/RJpsi/combine/'
#ensureDir(outdir)

if os.path.isdir(jobdir):
    ans = raw_input("Directory " + jobdir + " already exists. Delete?\n")
    
    if ans in ['Y', 'yes', 'Yes', 'y']:
        print 'deleted'
        os.system('rm -rf ' + jobdir)
    else:
        print 'quit...'
        sys.exit(1)

ensureDir(jobdir)

njobs = 200

for ijob in range(njobs):

    jobscript = jobdir + '/job_' + str(ijob) + '.sh'
        
    os.system("cp job_template.sh " + jobscript)
            
    with open(jobscript) as f:
        data_lines = f.read()
        
        data_lines = data_lines.replace('SEED', str(100+ijob))
        
        with open(jobscript, mode="w") as f:
            f.write(data_lines)

        command = 'sbatch -p short --account=t3 --error=' + jobdir + '/err_' + str(ijob) + ' --output=' + jobdir + '/out_' + str(ijob) + ' ' + jobscript

        print(command)
        os.system(command)
