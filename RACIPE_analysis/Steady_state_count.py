# Compiles the solution files (""). Normalised the steady state value of the nodes in different parameter sets through g/k normalisation and writes the values into davvk.txt file. Converts the steady states reported into into Boolean notation and then writes their counts into a file (msct.txt) in the following format:
# "Steady State" + "\t" + "Count"

import numpy as np
import seaborn as sb; sb.set(color_codes=True)
import matplotlib.pyplot as plt
import glob, os
import pandas as pd
from collections import Counter
import math
import pathlib

cwd = pathlib.Path(__file__).parent.absolute()
os.chdir(cwd)
print(os.getcwd())
parameterfil = glob.glob("*_parameters.dat")
#print(parameterfil[0])

filst = []

# Create a List of .dat files
for file in glob.glob("*.dat"):
    filst.append(file)
# Sort the file list do that the TS_solution_*.dat files come at last
filst.sort()
#print(filst)

# Create a combined file with all the TS_solution_*.dat
# ADCD are the nodes ==> Change needed for other networks
fi = open("davvk.txt","w+")

lnwtt = []

#print(filst)

linco = 0
sttlis = [1]

#lsi of all the lines in parameters file
pr = open(parameterfil[0], "r")
prlin = pr.readlines()

bt = []

# Read through the files one by one, -2 because the first 2 files are not TS_solution_*.dat files
for n in range(int(len(filst))-2):
    fh = open(filst[n+2])
#    print(filst[n+2])
    lines = fh.readlines()
    # sln ==> gives the number of the solution file
    sln = int(filst[n+2][-5])
    if sln == 0:
        sln = 10
    bt.append(int(sln))
    for r in range(len(lines)):
        #strips the \n at the end of the line
        lines[r] = lines[r].rstrip("\n")
        #strips the \t in the line, outputs a list
        lines[r] = lines[r].split("\t")
        # index of the corresponding line in the parameters.dat file
        l = int(lines[r][0]) - 1
        #prepare the list of the the diferent parameters
        prlin[l] = prlin[l].rstrip("\n")
        prlin[l] = prlin[l].split("\t")
        #this loop writes in data.txt
        #it divides the line into chunks of 4 values (i.e. 4 nodes)
        for v in range(sln):
            #print(v)
            #find the g/k values of the corresponding nodes
            gvkA = float(prlin[l][2])/float(prlin[l][6])
            gvkB = float(prlin[l][3])/float(prlin[l][7])
            gvkC = float(prlin[l][4])/float(prlin[l][8])
            gvkD = float(prlin[l][5])/float(prlin[l][9])
            #nomalise the final values in solution.dat with the g/k values if the corresponding node
            nodA = pow(2,float(lines[r][(2 + 4*v)]))/gvkA
            nodB = pow(2,float(lines[r][(3 + 4*v)]))/gvkB
            nodC = pow(2,float(lines[r][(4 + 4*v)]))/gvkC
            nodD = pow(2,float(lines[r][(5 + 4*v)]))/gvkD
            #Take log base2 again
            nodA = math.log(nodA,2)
            nodB = math.log(nodB,2)
            nodC = math.log(nodC,2)
            nodD = math.log(nodD,2)
            #write them down in the dagvk.txt
            fi.write(str(nodA) + "\t" + str(nodB) + "\t" + str(nodC) + "\t" + str(nodD) + "\n")
            #fi.write(lines[r][(2 + 4*v)] + "\t" + lines[r][(3 + 4*v)] + "\t" + lines[r][(4 + 4*v)] + "\t" + lines[r][(5 + 4*v)] + "\n")
            linco = linco + 1
    # this list gives the line numbers where the different multistable steady states start in the data.txt file
    #useful later on when we again bring them together for final plotting
    sttlis.append(linco)

#print(sttlis)
fi.close()

fi = open("davvk.txt", "r")

ro = 0
ex = 0
SStli = []
SSt = ""

frer = fi.readlines()

A = []
B = []
C = []
D = []


for x in frer:
    x = x.rstrip("\n")
    x = x.split("\t")
    A.append(float(x[0]))
    B.append(float(x[1]))
    C.append(float(x[2]))
    D.append(float(x[3]))

stdA = np.std(A)
meanA = np.mean(A)

stdB = np.std(B)
meanB = np.mean(B)

stdC = np.std(C)
meanC = np.mean(C)

stdD = np.std(D)
meanD = np.mean(D)

for ro in frer:
    #read data.txt to convert the lines from float to H/L notation
    ro = ro.rstrip("\n")
    ro = ro.split("\t")
    one = float(ro[0])
    two = float(ro[1])
    thr = float(ro[2])
    fou = float(ro[3])
    # take the mean of the values
    # As we have to classify as only H/L here, no need to calculate the complete Z-score
    if (one -  meanA)/stdA > -0 :
        SSt = SSt + "H"
    else:
        SSt = SSt + "L"

    if (two -  meanB)/stdB > -0 :
        SSt = SSt + "H"
    else:
        SSt = SSt + "L"

    if (thr -  meanC)/stdC > -0 :
        SSt = SSt + "H"
    else:
        SSt = SSt + "L"

    if (fou -  meanD)/stdD > -0 :
        SSt = SSt + "H"
    else:
        SSt = SSt + "L"
    # append the values to a list
    # here the order in the lines is preserved and so we can still use sttlis to acces the different
    # multistable states
    SStli.append(SSt)
    SSt = ""

#print(SStli)

#bt = 1

mistli = []
templi = []
v = 0
fg = 0
lll = 0
# this loops goes through sttlis to accces the coordinates where the
# different multi stable steady states start
# -1 because the last value corresponds to the last line/element of the list
# and we are looking at w and w+1, so avoid the out of range error
#print(bt)
#print(sttlis)
for w in range(len(sttlis)-1):
    #print(bt[w])
    for v in range(sttlis[w],sttlis[w+1], bt[w]):
        #print(sttlis[w+1])
    # bt gives the multi-stable state value and also the number of elements v should jump
    # to get to the next set of multistable state values
    #    print(v)
        for fg in range(bt[w]):
            # the steady states are added to a temp list
            #print(v+fg)
            templi.append(SStli[v + fg])
        # the list is then sorted
        # this is done to remove duplicates which differ only by their order in which they are seen
        templi.sort()
        #print(templi)
        # the sorted list in added to anoter list whcich has all the multi stable states information
        mistli.append(templi)
        # clear the temp list for the next loop
        #print(templi)
        templi = []
    # while this loop exits, update the value of bt, to the next multi stable state value
    #bt = bt+1


#print(len(mistli))

# convert the mstli list to a tuple list to count the multistable states
nmistli = map(tuple, mistli)
# count the occuranced of the tuples which represent the multistable
count = Counter(nmistli)

#print(count)

# the count function values can then be acced by creating list for the keys(multistable states) and
# their counts (values)
key = list(count.keys())
val = list(count.values())
#print(val)
#print(key)

cou = open("msct.txt", "w")


# plotting parameters
#plt.xlabel("Bi/Multi-Stable States")
#plt.xticks(rotation=90, fontsize=8)
#plt.ylabel("Frequency")

total = 0

# preparing the data for plotting
for e in range(len(val)):
#    lenkey = len(key[e])
    key[e] = " ".join(key[e])
#    total = total + val[e]
    # frequency of the multistable states is found out by
    # dividing the count of that pariculr frequency state by
    # the total number multistable states which is,
    # 100(inital parameters) - no. of monostable states
    #val[e] = round(val[e]/(100-sttlis[0]), 2)
    # upade the count  with its frequency and round it off
    # total is to check wether everything is right (sould add up to 1)
    # but because of round off, it will come to be lesser than that
    #total = total + val[e]
    cou.write(key[e] + "\t" + str(val[e]) + "\n")
#print(total)
#print((100-sttlis[0]))

#plott the graph, use tight layout
#plt.bar(key, val)

#for i in range(len(val)):
    #plt.text(x = key[i], y = val[i], s = val[i], ha='center', va='bottom')

#plt.show()
