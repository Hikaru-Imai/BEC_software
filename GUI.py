import numpy as np
import cv2
import itertools
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import time
import datetime
import matplotlib.pyplot as plt
import subprocess as sp
import random

from config import makeroot
from config import Detection
from config import Print
from config import BackEndMode
from config import stop_backend
def dirdialog_clicked():
    iDir = "/Users/hikaru/Desktop/BEX/software"
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    DirStr.set(iDirPath)


def filedialog_clicked():
    iDir = "/Users/hikaru/Desktop/BEX/software"
    iFilePath = filedialog.askopenfilename(initialdir = iDir)
    NameStr.set(iFilePath)


def Detection_clicked():
    Detection(NameStr.get(),ThrStr.get(),SigmaStr.get())



def  BackEndMode_clicked():
    
    #BackEndMode(ThrStr.get(),SigmaStr.get(),DirStr.get())
    startcmd = ["start"]
    cmd = ["start","cmd","/k","python","BackEnd.py",ThrStr.get(),SigmaStr.get(),DirStr.get()]
    #sp.run(startcmd,shell=True)
    sp.run(cmd,shell=True)
    #print(DirStr.get())

def stop_backend_clicked():
    stop_backend()

def makeroot_clicked():
    makeroot(NameStr.get())

def Print_clicked():
    Print(NameStr.get(),ThrStr.get())

def Exit():

    exit()
    





# main window

root  = tk.Tk()

root.title("BEC_software")
root.geometry("800x500")


#label

DirNameLa = tk.Label(text = 'Target Dir')
NameLa = tk.Label(text = 'photoname')
ThrLa  = tk.Label(text = 'threshold')
SigmaLa  = tk.Label(text = 'sigma')



DirNameLa.place(x=20,y=40)
NameLa.place(x=20,y=70)
ThrLa.place(x=20,y=130)
SigmaLa.place(x=20,y=170)




# Entry

DirStr    = tk.StringVar()
NameStr   = tk.StringVar()
ThrStr    = tk.StringVar()
SigmaStr  = tk.StringVar()


# set initial parameter.defult parameter

NameStr.set("")
ThrStr.set("70")
SigmaStr.set("5")

DirEn      = tk.Entry(width = 65,textvariable= DirStr)
NameEn     = tk.Entry(width = 65,textvariable = NameStr)
SetThrEn   = tk.Entry(textvariable = ThrStr,width = 5)
SetSigmaEn = tk.Entry(textvariable = SigmaStr,width = 5)

DirEn.place(x =110,y = 40)
NameEn.place(x =110,y = 70)
SetThrEn.place(x=110,y=130)
SetSigmaEn.place(x=110,y=170)



# Button


RunBu  = tk.Button(text = "RUN",height = 5,width = 10,command = Detection_clicked,fg='black',bg = 'gray')
BackEndBu  = tk.Button(text = "Backend mode",height = 5,width = 10,command = BackEndMode_clicked,fg='black',bg = 'spring green')
stopBackEndBu  = tk.Button(text = "stop Backend \n mode",height = 5,width = 10,command = stop_backend_clicked,fg='white',bg = 'red')

BrowsedirBu = tk.Button(text = "Browse",command = dirdialog_clicked )
BrowseBu = tk.Button(text = "Browse",command = filedialog_clicked )
ROOTBu = tk.Button(text = "ROOT",height = 5,width = 10,command = makeroot_clicked)
PrintBu = tk.Button(text = "BINARY",height = 5,width = 10,command = Print_clicked)

ExitBu = tk.Button(text = "exit",command = Exit,width = 6) 

ExitBu.place(x=620,y = 10)
BrowsedirBu.place(x =600,y =40 )
BrowseBu.place(x =600,y =70 )
RunBu.place( x= 550,y = 130 )
BackEndBu.place( x= 400,y = 230 )
stopBackEndBu.place( x= 550,y = 230 )
ROOTBu.place( x= 250,y = 130 )
PrintBu.place( x= 400,y = 130 )# todo change name to binary



root.mainloop()







