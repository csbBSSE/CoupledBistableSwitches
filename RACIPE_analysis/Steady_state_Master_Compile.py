#MS.txt file is read, the different steady states are counted, compiled, and sorted and written into a single file i.e. fin.txt.

import glob, os
import collections
import pandas as pd
import os
from operator import itemgetter
import pathlib

cwd = pathlib.Path(__file__).parent.absolute()
os.chdir(cwd)
cwd = str(cwd)

filst = []

#MS.txt is the master file with all the msct.txt files are concatenated.
fi = open("MS.txt", "r")
fo = open("fin.txt", "w")

states = fi.readlines()


stdict = {}
st = []
freq = []

for x in range(len(states)):
    states[x] = states[x].rstrip("\n")
    states[x] = states[x].split("\t")
    sts = states[x][0]
    freq = int(states[x][1])
    #st.append(states[x][0])
    #freq.append(int(states[x][1]))
    if sts in stdict:
        stdict[sts] = stdict[sts] + freq
    else:
        stdict[sts] = freq

#sort the dictionary by the legth of the keys
od = collections.OrderedDict(sorted(stdict.items(), key = lambda t: len(t[0])))

fi.close()

#print out the values
for y,z in od.items():
    fo.write(y + "," + str(z) + "\n")
fo.close()

fz = open("fin.txt","r")
lines = fz.readlines()

msli = ["one", "two", "thr", "fou", "fiv", "six", "sev",  "eig", "nin"]
splt = []
co = 0

for l in range(len(lines)):
    lines[l] = lines[l].rstrip("\n")
    lines[l] = lines[l].split(",")

for s in range(len(lines)):
    if len(lines[s][0]) != len(lines[s-1][0]):
        splt.append(s)
        co = co + 1

splt.append(len(lines))
#print(splt)

msli = msli[0:(co)]


for t in range(len(splt)-1):
    msli[t] = lines[splt[t]:splt[t+1]]

for x in range(len(msli)):
    st = []
    fr = []
    for e in msli[x]:
        st.append(e[0])
        fr.append(int(e[1]))
    msli[x].clear()
    msli[x].append(st)
    msli[x].append(fr)


for L in msli:
    L[0] = [x for _,x in sorted(zip(L[1],L[0]), reverse=True)]
    L[1].sort(reverse=True)

Tst = []
Tfr = []
TT = []
Tf = 0
Pf = []

for lx in lines:
    Tst.append(lx[0])
    Tfr.append(int(lx[1]))
    Tf = Tf + int(lx[1])

TT.append(Tst)
TT.append(Tfr)

TT[0] = [x for _,x in sorted(zip(TT[1],TT[0]), reverse=True)]
TT[1].sort(reverse=True)

df = {"State": TT[0], "Frequency": TT[1]}
df = pd.DataFrame(df)

for ed in TT[1]:
    Pf.append(ed/Tf)

df["PerFrq"] = pd.DataFrame(Pf)


for g in range(len(msli)):
    sta = "State" + str(g+1)
    frq = "Frequency" + str(g+1)
    tot = "Total" + str(g+1)
    per = "PerFrq" + str(g+1)
    spc = " "*g
    tfr = 0
    pfr = []
    for ss in range(len(msli[g][1])):
        tfr = tfr + int(msli[g][1][ss])
    for ss in msli[g][1]:
        pfr.append((int(ss)/tfr))
    #df = {sta: msli[g][0], frq: msli[g][1]}
    df[spc] = ""
    df[sta] = pd.DataFrame(msli[g][0])
    df[frq] = pd.DataFrame(msli[g][1])
    df[per] = pd.DataFrame(pfr)
    df[tot] = pd.DataFrame([tfr, (tfr/Tf)])


#print(df)
csvfi = str(cwd).split("/")
net = "/" + csvfi[-1] + ".csv"
filnam = cwd + net
print(filnam)
df.to_csv(filnam, index=False)
