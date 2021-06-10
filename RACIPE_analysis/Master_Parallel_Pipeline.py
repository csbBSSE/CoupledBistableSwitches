# Master script to run RACIPE processes parallelly and the other asoociated downstream scripts for analysis into a pipeline. An finally compile the results into an excel files.

import os
from os.path import isfile, join
import subprocess
import pandas as pd
import xlsxwriter

# gets the current working directory
cwd = os.getcwd()

##########################################################################################
#      Read the topo files and make directories and subdirectories
##########################################################################################
# Go to the topo directory and list all the topo files in the directory
tpdir = "/home/shadowfax/Intrnshp/Topo/"
os.chdir(tpdir)
tpFi = os.listdir() # glob.glob(".topo") might be a better choice, as it selects specifically topo files
# loop through the topo files list and create a folder in their name in the current
# working directory with 3 subfolders for the three replicates
for xi in range(len(tpFi)):
    os.chdir(cwd)
    mkpdir = "mkdir " + tpFi[xi][:-5]
    subprocess.run(mkpdir, shell=True)
    mkfol = "mkdir " + tpFi[xi][:-5] + "/1 " + tpFi[xi][:-5] + "/2 " + tpFi[xi][:-5] + "/3"
    subprocess.run(mkfol, shell=True)
    for sbdr in range(1,4):
        tpfilcp = "cp " + tpdir + tpFi[xi] + " " + cwd + "/" + tpFi[xi][:-5] + "/" + str(sbdr)  + "/"
        subprocess.call(tpfilcp, shell=True)
#
##########################################################################################
##########################################################################################
#
# reset the cwd
os.chdir(cwd)

##########################################################################################
#      Make a list of all the folders in CWD
##########################################################################################
# make a list of all the folders and files in cwd
alFi = os.listdir()
NetW = []
# append only folders to NetW list, removes all the python files in cwd from this list.
for f in range(len(alFi)):
    if "." not in alFi[f]:
        NetW.append(cwd + "/" + str(alFi[f]))

# if you just want to list the folders, you can also use:
# NetW = next(os.walk('.'))[1]
##########################################################################################
##########################################################################################
#
# sort the list not necessary
NetW.sort()
#
##########################################################################################
#    Run RACIPE - Parallel Processing
##########################################################################################
# Open the RACIPE directory
RCPdir = "/home/shadowfax/Intrnshp/RACIPE-1.0"
os.chdir(RCPdir)
# A list of all the RACIPE cpommands to be run
RnRCPli = []
# loop through the folders and subfolders to append the commands to the list
for fil in range(len(NetW)):
    for repfi in range(1,4):
        tpfil = NetW[fil] + "/" + str(repfi) + "/*.topo"
        rRCP = "./RACIPE " + tpfil #+ " -num_paras 10000 -num_ode 1000"#
        RnRCPli.append(rRCP)
        #subprocess.call(rnRCP, shell=True)

# Secify the number of cores for parallel processing
cores = 6
# devide the whole list into batches equal to the number of cores
# creates a list of lists
btchs = [RnRCPli[i:i + cores] for i in range(0, len(RnRCPli), cores)]
# join the elements of each list by " & " for the final command
# this is essential for parallel processing
for rrn in btchs:
    rnRCP = " & ".join(rrn)
    print(rnRCP)
    subprocess.run(rnRCP, shell=True)
##########################################################################################
##########################################################################################
#
os.chdir(cwd)
#
##########################################################################################
#    Copy all the necessary python files into their respective folders
##########################################################################################
#
for fil in range(len(NetW)):
    sdpst = "cp sd.py " + NetW[fil] + "/"
    subprocess.call(sdpst, shell=True)
    isdpst = "cp isd.py " + NetW[fil] + "/"
    subprocess.call(isdpst, shell=True)
    for repfi in range(1,4):
        subfol = NetW[fil] + "/" + str(repfi)
        qwpst = "cp qw.py " + subfol
        subprocess.run(qwpst, shell=True)
        fdpst = "cp fd.py " + subfol
        subprocess.run(fdpst, shell=True)
#
##########################################################################################
##########################################################################################
#
##########################################################################################
#    Run qw.py and fd.py both of which do analysis of the individual replicates
##########################################################################################
# Parallel Processing of the scripts to generate the required analysis files
# uses the steps as used in RACIPE parallel processing
btchqw = []
btchfd = []
#
for fil in range(len(NetW)):
    for repfi in range(1,4):
        os.chdir(NetW[fil] + "/" + str(repfi))
        qwRun = "python3 " + NetW[fil] + "/" + str(repfi) + "/" + "Steady_state_count.py"
        btchqw.append(qwRun)
        fdRun = "python3 " + NetW[fil] + "/" + str(repfi) + "/" + "Multistable_counter_bimodality_calc.py"
        btchfd.append(fdRun)
#
btchQ = [btchqw[o:o + cores] for o in range(0, len(btchqw), cores)]
for qrn in btchQ:
    rnQ = " & ".join(qrn)
    subprocess.run(rnQ, shell=True)
#
btchF = [btchfd[p:p + cores] for p in range(0, len(btchfd), cores)]
for frn in btchF:
    rnF = " & ".join(frn)
    subprocess.run(rnF, shell=True)
#
##########################################################################################
##########################################################################################
#Change the directory to CWD
os.chdir(cwd)
#
##########################################################################################
# Compile similar files of the replcates and then process them to create Excel Files
##########################################################################################
#
#
for fi in range(len(NetW)):
    MScmd = "cat " + NetW[fi] + "/1/msct.txt " + NetW[fi] + "/2/msct.txt "+ NetW[fi] + "/3/msct.txt " + "> " + NetW[fi] + "/MS.txt"
    Stcmd = "cat " + NetW[fi] + "/1/sts.txt " + NetW[fi] + "/2/sts.txt "+ NetW[fi] + "/3/sts.txt " + "> " + NetW[fi] + "/St.txt"
    BCcmd = "cat " + NetW[fi] + "/1/bmc.txt " + NetW[fi] + "/2/bmc.txt "+ NetW[fi] + "/3/bmc.txt " + "> " + NetW[fi] + "/BC.txt"
    subprocess.run(MScmd, shell=True)
    subprocess.run(Stcmd, shell=True)
    subprocess.run(BCcmd, shell=True)
#
# Parallel processing of the sd and fd scrips
btchsd = []
btchis = []
#
for gy in range(len(NetW)):
    sdR = "python3 " + NetW[gy] + "/Steady_state_Master_Compile.py"
    btchsd.append(sdR)
    isR = "python3 " + NetW[gy] + "/steady_state_csv_compile.py"
    btchis.append(isR)
#
btchS = [btchsd[v:v + cores] for v in range(0, len(btchsd), cores)]
for srn in btchS:
    rnS = " & ".join(srn)
    subprocess.run(rnS, shell=True)
#
btchI = [btchis[c:c + cores] for c in range(0, len(btchis), cores)]
for irn in btchI:
    rnI = " & ".join(irn)
    subprocess.run(rnI, shell=True)
#
# not parallel processing, as written in the same script, but can be converted to parallel
# by writing a seperate script and using the same logic as before
for gu in range(len(NetW)):
    os.chdir(NetW[gu])
    curnet = NetW[gu].split("/")[-1]
    stainf = pd.ExcelWriter((curnet+"S.xlsx"), engine='xlsxwriter')
    repinf = pd.ExcelWriter((curnet+"R.xlsx"), engine='xlsxwriter')
    dfi = pd.read_csv(curnet + ".csv")
    dfi.to_excel(stainf, sheet_name=(curnet+"stainf"), index=False)
    inf = pd.read_csv(curnet + "Rep.csv")
    inf.to_excel(repinf, sheet_name=(curnet+"repinf"), index=False)
    stainf.save()
    repinf.save()
#
##########################################################################################
##########################################################################################
# Change the directory to CWD
os.chdir(cwd)
#
