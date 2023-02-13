
for year in 2016 2017 2018 all
do
    python makeDatacard.py --year ${year}
    python makeDatacard.py --year ${year} --scale
done
