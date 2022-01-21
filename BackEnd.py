import numpy as np
import cv2
import itertools
import sys
import time
import datetime
import matplotlib.pyplot as plt
import subprocess as sp
import random
import os
from  PIL  import Image







def BackEndMode(thr,sigma,TargetDir):
    print("Back End mode")
    
    # write out setting file


    # Loop

    FileNumInTarDir = []
    FileNameInTarDir = os.listdir(TargetDir) # init list
    debugcount = 0
    popupNum = 0
    while True:

        FileNum = len(os.listdir(TargetDir))
        #print(FileNum)
        FileNumInTarDir.append(FileNum)
        time_now = datetime.datetime.now()
        if(time_now.second % 2 == 0):
            print("Waiting...")
        debugcount = debugcount + 1
        #print("debugcount=",debugcount)
        if len(FileNumInTarDir) > 2 :

            del FileNumInTarDir[0] # delete first index
            #print(FileNumInTarDir)
            #print(FileNameInTarDir)

            # input new data case
            if( FileNumInTarDir[0] != FileNumInTarDir[1]):

                # task kill
                if(popupNum>0):
                    killcmd = ["taskkill","/f","/im","Microsoft.Photos.exe"]
                    sp.run(killcmd,shell = True)


                NowFileNameInTarDir = os.listdir(TargetDir)
                difflist = list(set(NowFileNameInTarDir)^set(FileNameInTarDir) )
                dataname = str(difflist[0])
                
                # write out setting file    
                fout = open("setting.txt","wt")
                #outputname = "/Users/hikaru/Desktop/BEX/software/output/C__"+dataname # Mac
                outputname = "C:/Users/sphen/Desktop/BEC/output/C__"+dataname # win10 ver

                times = sigma
                fout.write(TargetDir+"/"+dataname+"\n")
                fout.write(str(thr)+"\n")
                fout.write(str(times)+"\n")
                fout.write(outputname+"\n")
    
                fout.close()

                print("Run Macro")
                #cmd = ["./RUN"] # for mac
                cmd = ["Detection"] # for win10
                cmdshow = [outputname]
                time.sleep(1)
                sp.run(cmd)
                sp.run(cmdshow,shell = True) # pop up photo               
                popupNum = popupNum + 1
                FileNameInTarDir = NowFileNameInTarDir


        time.sleep(1)
        
        #if debugcount>100:
            #break

        if(os.path.isfile("stop.txt")): # if stop.txt file exist, stop back end mode.
            rmcmd = ["del","stop.txt"]
            sp.run(rmcmd,shell= True)
            print("Stop Back End mode")
            break




# main function

#                   thr       sigma  Target Dir
print(sys.argv[1],sys.argv[2],sys.argv[3])
BackEndMode(sys.argv[1],sys.argv[2],sys.argv[3])


