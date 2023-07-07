# 1. create ROOstats ...

> root -l examplews.C


# 2. setup cards 

> python makeDatacard.py

> cd datacard

> sh make.sh

> cd - 


# 3. run fit 

!!!BE CAREFUL NOT TO UNBLIND!!!

> sh do_fit.sh 

> python draw.py 

# 4. run bias test

inspect job_template.sh and modify expectSignal as you wish

> cd bias
> python getDataset.py
> python draw_bias.py


# 5. make likelihood paraborah 

> sh do_parabola.sh 


# 6. make impact plot

> cd impact 

> sh do_impact.sh

> sh draw.sh


# 7. channel compatibility 

> sh do_channelCompatibility.sh


# 8. gof

> cd gof

> sh basic.sh

> python getDataset.py

> sh draw.sh 


# 9. sensitivity plot 

> python rk.py 