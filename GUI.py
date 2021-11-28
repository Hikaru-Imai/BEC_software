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

def dirdialog_clicked():
    iDir = "/Users/hikaru/Desktop/BEX/software"
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    DirEn.set(iDirPath)


def filedialog_clicked():
    iDir = "/Users/hikaru/Desktop/BEX/software"
    iFilePath = filedialog.askopenfilename(initialdir = iDir)
    NameStr.set(iFilePath)


def Detection_clicked():
    Detection(NameStr.get(),ThrStr.get(),SigmaStr.get())


def makeroot_clicked():
    makeroot(NameStr.get())

def Print_clicked():
    Print(NameStr.get(),ThrStr.get())

def Exit():

    exit()
    





# main window

root  = tk.Tk()

root.title("BEC_software")
root.geometry("700x300")


#label

NameLa = tk.Label(text = 'photoname')
ThrLa  = tk.Label(text = 'threshold')
SigmaLa  = tk.Label(text = 'sigma')



NameLa.place(x=20,y=70)
ThrLa.place(x=20,y=130)
SigmaLa.place(x=20,y=170)




# Entry

NameStr = tk.StringVar()
ThrStr = tk.StringVar()
SigmaStr = tk.StringVar()


# set initial parameter.defult parameter

NameStr.set("/Users/hikaru/Desktop/BEX/software/photo/20211102110525.jpg")
ThrStr.set("70")
SigmaStr.set("5")

DirEn = tk.Entry(width = 45)
NameEn = tk.Entry(width = 45,textvariable = NameStr)
SetThrEn = tk.Entry(textvariable = ThrStr,width = 5)
SetSigmaEn = tk.Entry(textvariable = SigmaStr,width = 5)

#DirEn.place(x =110,y = 40)
NameEn.place(x =110,y = 70)
SetThrEn.place(x=110,y=130);
SetSigmaEn.place(x=110,y=170);



# Button


RunBu  = tk.Button(text = "RUN",height = 5,width = 10,command = Detection_clicked,fg='red')
BrowseBu = tk.Button(text = "Browse",command = filedialog_clicked )
ROOTBu = tk.Button(text = "ROOT",height = 5,width = 10,command = makeroot_clicked)
PrintBu = tk.Button(text = "BINARY",height = 5,width = 10,command = Print_clicked)

ExitBu = tk.Button(text = "exit",command = Exit,width = 6) 

ExitBu.place(x=480,y = 10)
BrowseBu.place(x =600,y =70 )
RunBu.place( x= 550,y = 130 )
ROOTBu.place( x= 250,y = 130 )
PrintBu.place( x= 400,y = 130 )



root.mainloop()







