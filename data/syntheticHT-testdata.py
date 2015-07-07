# Generating synthetic data for a human trafficking decision tree model
# Y: Trafficker (binary)
# X1: Gender (0 female, 1 male)
# X2: Member of known gang (Binary)
# X3: Age
# X4: Arrest Record (Binary)
# X5: Crime Conviction Type (Personal, Property, Inchoate, Statutory)
# X9: Crime Level (Misdemeanor, Felony)
# X11: Marital Status
# X12: Education level
# X13: Employed

from scipy.stats import binom
import numpy as np
import csv

samplesize = 1000
outfile = open("humantrafficking_TEST_data.csv","w")
out = csv.writer(outfile,delimiter=",",lineterminator="\n")
header = ["Trafficker","Location", "Gender", "Age", "Marital Status", "US Citizenship", "Education","Employed","Gang Member","Arrested","Personal Crime","Property Crime","Inchoate Crime","Statutory Crime","Misdemeanor","Felony"]
out.writerow(header)
#print header

cities = ["Atlanta", "Chicago", "Dallas", "Detroit", "Las Vegas", "San Diego", "San Francisco", "St. Louis", "Tampa", "DC"]
t = binom.rvs(1,.5, size=samplesize)

for i in range(len(t)):
    arr = binom.rvs(1,.85)
    loc = cities[np.random.randint(0,len(cities))]
    if t[i] == 1:
        # gender 25/75 ratio
        gender = binom.rvs(1,.75)
        # age 18-52
        age = np.random.randint(19,54)
        # marital status
        ms =  binom.rvs(1,.7)
        # in a gang
        gang = binom.rvs(1,.72)
    else:
        # gender 40/60 ratio
        gender = binom.rvs(1,.6)
        # age 15-67
        age = np.random.randint(15,67)
        # marital status
        ms =  binom.rvs(1,.75)
        #in a gang
        gang = binom.rvs(1,.6)
    # education
    if gang:
        edu = np.random.randint(0,1)
    elif arr:
        edu = np.rint(np.random.normal(1,.5))
    else:
        edu = np.rint(np.random.normal(1.75,.25))
    # employment
    if edu > 1:
        emp = binom.rvs(1,.95)
    elif edu == 1:
        emp = binom.rvs(1,.8)
    else:
        emp = binom.rvs(1,.5)
    # criminal background
    if arr:
        sta = binom.rvs(1,.15)
    if t[i] == 1 and arr:
        per = binom.rvs(1,.3)
        if gang:
            pro = binom.rvs(1,.2)
        else:
            pro = binom.rvs(1,.1)
        inh = binom.rvs(1,.3) 
    elif arr:
        per = binom.rvs(1,.15)
        if gang:
            pro = binom.rvs(1,.6)
            inh = binom.rvs(1,.3) 
        else:
            inh = binom.rvs(1,.2) 
            pro = binom.rvs(1,.2)
    if not arr:
        per,pro,inh,sta,mis,fel = 0,0,0,0,0,0
    crimes = per + pro +sta + inh
    if crimes > 0:
        fel = binom.rvs(1,.1*crimes)
        if fel:
            mis = binom.rvs(1,.7)
        else:
            mis = 1
    else:
        mis,fel = 0,0

    usc = binom.rvs(1,.5)
    newline = [t[i],loc,gender,age,ms,usc,int(edu),emp,gang,arr,per,pro,inh,sta,mis,fel]
    #print newline
    out.writerow(newline)

outfile.close()
