# Reads the steady state counts of all the threee replicates, compiles them and sorts them into mono or different multistable steady states, and then finally wrtites all the information into a csv file.

import glob, os
import pathlib
import collections
import pandas as pd

cwd = pathlib.Path(__file__).parent.absolute()
os.chdir(cwd)
cwd = str(cwd)

filst = []

# MS.txt is the concatenated version of all the msct.txt files of the three replicates.
fi = open("MS.txt", "r")
fo = open("ifin.txt", "w")

states = fi.readlines()


stdict = {}
st = []
freq = []

for x in range(len(states)):
    states[x] = states[x].rstrip("\n")
    states[x] = states[x].split("\t")
    sts = states[x][0]
    freq = states[x][1]
    #st.append(states[x][0])
    #freq.append(int(states[x][1]))
    if sts in stdict:
        stdict[sts] = stdict[sts] + "," +freq
    else:
        stdict[sts] = freq

#sort the dictionary by the legth of the keys
od = collections.OrderedDict(sorted(stdict.items(), key = lambda t: len(t[0])))

#print out the values
for y,z in od.items():
    fo.write(y + "," + str(z) + "\n")
    #print(y + "\t" + str(z) + "\n")
fo.close()

fo = open("ifin.txt", "r")

dstbr = fo.readlines()

for lne in range(len(dstbr)):
    crl = dstbr[lne].rstrip("\n")
    crl = crl.split(",")
    crln = crl[1:]
    zeros = "0"
    if len(crln) < 3:
        if (3 - len(crln)) == 2:
            crln = crln + ["0", "0"]
        if (3 - len(crln)) == 1:
            crln = crln + ["0"]
    totnum = int(crln[0]) + int(crln[1]) + int(crln[2])
    crln = crln + [str(totnum)]
    crln = [crl[0]] + crln
    crln[1], crln[2], crln[3], crln[4] = int(crln[1]), int(crln[2]), int(crln[3]), int(crln[4])
    dstbr[lne] = crln
    #print(dstbr[lne])
dstbr.sort(key=lambda x: x[4], reverse=True)
#print(dstbr)
df = pd.DataFrame(dstbr)
df.columns = ["State", "Rep1", "Rep2", "Rep3", "Total"]

csvfi = cwd.split("/")
net = "/" + csvfi[-1] + "Rep.csv"
filnam = cwd + net
print(filnam)
df.to_csv(filnam, index=False)
