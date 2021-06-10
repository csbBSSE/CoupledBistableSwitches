# Reads the solution files, counts the number of monostable and other multistable states, reports the counts in the sts.txt file. Reads the davvk.txt file to find out bimodality coefficients of the individual nodes according to thier steady state values and reports it in bmc.txt file.

import glob, os
import pathlib
import collections
import scipy.stats as scpy

cwd = pathlib.Path(__file__).parent.absolute()
os.chdir(cwd)

fo = open("sts.txt", "w")

filst = []

# Create a List of .dat files
for file in glob.glob("*.dat"):
    filst.append(file)

# Sort the file list do that the TS_solution_*.dat files come at last
filst.sort()

# Read through the files one by one, -2 because the first 2 files are not TS_solution_*.dat files
for n in range(int(len(filst))-2):
    fh = open(filst[n+2])
#    print(filst[n+2])
    lines = fh.readlines()
    # sln ==> gives the number of the solution file
    sln = (filst[n+2][-5])
    fo.write(sln + "\t" + str(len(lines)) + "\n")

fo.close()

#Reading davvk files to acces the steady g/k normalised state values of the nodes.
bcf = open("davvk.txt", "r")
vali = bcf.readlines()

A = []
B = []
C = []
D = []

#Storing the values of nodes in thier individual arrays.
for s in range(len(vali)):
    vali[s] = vali[s].rstrip("\n")
    vali[s] = vali[s].split("\t")
    A.append(float(vali[s][0]))
    B.append(float(vali[s][1]))
    C.append(float(vali[s][2]))
    D.append(float(vali[s][3]))

n = len(A)
num = (pow((n-1),2))/((n-2)*(n-3))

#Calculating the bimodality coefficients
gA = scpy.skew(A)
kA = scpy.kurtosis(A, fisher=True)
bcA = (pow(gA,2) + 1)/(kA + 3*num)

gB = scpy.skew(B)
kB = scpy.kurtosis(B, fisher=True)
bcB = (pow(gB,2) + 1)/(kB + 3*num)

gC = scpy.skew(C)
kC = scpy.kurtosis(C, fisher=True)
bcC = (pow(gC,2) + 1)/(kC + 3*num)

gD = scpy.skew(D)
kD = scpy.kurtosis(D, fisher=True)
bcD = (pow(gD,2) + 1)/(kD + 3*num)

bcf.close()

bmc = open("bmc.txt", "w")

repno = int(str(cwd).split("/")[-1])

# Writing the bimodality coefficients into the bmc.txt file
if repno == 1:
    bmc.write("A,B,C,D\n")
    bmc.write(str(bcA)+","+str(bcB)+","+str(bcC)+","+str(bcD)+"\n")
else:
    bmc.write(str(bcA)+","+str(bcB)+","+str(bcC)+","+str(bcD)+"\n")



