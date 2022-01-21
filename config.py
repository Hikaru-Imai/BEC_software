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

class Img():

    def __init__(self,name):

        self.name = name

    def read(self):
     
        return cv2.imread(self.name)

    def hsv(self):
      
        return cv2.cvtColor(self.read(),cv2.COLOR_BGR2HSV)

    def gray(self):

        return cv2.cvtColor(self.read(),cv2.COLOR_BGR2GRAY)


    def binary(self,thorsold):
        gray = self.gray()
        gray_bi = np.where(gray>thorsold,255,0)

#        cv2.imwrite("../result/class_binary.JPG",gray_bi)

        return gray_bi

    def rotate(self):
        '''
        photo = self.read()
        h,w,c = photo.shape
        Matrix = cv2.getRotationMatrix2D((w/2, h/2),90,1)
        bgr = cv2.warpAffine(photo, Matrix, (w, h))
        '''
        #im = Image.open(self.name)
        #pl.rotate()

        #cv2.rotate(self.read(),cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        cv2.imwrite(str(self.name),cv2.rotate(self.read(),cv2.ROTATE_90_COUNTERCLOCKWISE))

        
    def save(self):
        print("saving image data...")
        hsv = self.hsv()
        np.savetxt("gray.txt",self.gray())
        np.savetxt("hue.txt",hsv[:,:,0])
        np.savetxt("sat.txt",hsv[:,:,1])
        np.savetxt("val.txt",hsv[:,:,2])


    def write(self,dire):

        img = self.read()
        hsv = self.hsv()
        gray = self.gray()


        cv2.imwrite(dire+self.name+"_class_img.JPG",img)
        cv2.imwrite(dire+self.name+"_class_hsv.JPG",hsv)
        cv2.imwrite(dire+self.name+"_class_gray.JPG",gray)




def makeroot(name):
    
    photo_dire  = "../photo/"
    output_dire = "../data/"
    #photo_dire  = "../photo/"
    output_dire = "/Users/hikaru/Desktop/BEX/software/data/"
    fmt         = ".jpg"


    dataname           = name

    output_hue         = "./hue.txt"
    output_gray        = "./gray.txt"
    output_saturation  = "./saturation.txt"

    output_blue        = "./blue.txt"
    output_green       = "./green.txt" 
    output_red         = "./red.txt"

    #output_hue         = output_dire+name+"_hue.txt"
    #output_gray        = output_dire+name+"_gray.txt"
    #output_saturation  = output_dire+name+"_saturation.txt"

    #output_blue        = output_dire+name+"_blue.txt"
    #output_green       = output_dire+name+"_green.txt" 
    #output_red         = output_dire+name+"_red.txt"

    print("===Loading===",dataname)
    pixel = Img(dataname)
    bgr   = pixel.read()
    hsv   = pixel.hsv()



    print("====extract BGR data====")


    blue   = bgr[:,:,0]
    green  = bgr[:,:,1]
    red    = bgr[:,:,2]





    print("====extract HSV data====")

    hue          = hsv[:,:,0] 
    saturation   = hsv[:,:,1] 
    gray         = hsv[:,:,2] 

    row,col = hue.shape
    print("row number=",row,"col number=",col)
    print("====save HSV data====")



    
    print("name=",name)

    name = dataname.split('/')
    name = name[-1]
    name = name.split(".")
    fout = open("basename.txt","w")
    fout.write(output_dire+name[0]+"\n")
    fout.close()
    
    np.savetxt(output_blue,blue,fmt = "%d")
    np.savetxt(output_green,green,fmt = "%d")
    np.savetxt(output_red,red,fmt = "%d")


    np.savetxt(output_hue,hue,fmt="%d")
    np.savetxt(output_saturation,saturation,fmt="%d")
    np.savetxt(output_gray,gray,fmt="%d")



    cmd1 =["root","-q","-l","makeroot.c"]
    cmd2 =["rm",output_hue]
    cmd3 =["rm",output_saturation]
    cmd4 =["rm",output_gray]
    cmd5 =["rm",output_blue]
    cmd6 =["rm",output_green]
    cmd7 =["rm",output_red]


    print("====Run makeroot.c ====")


    sp.run(cmd1)
    sp.run(cmd2)
    sp.run(cmd3)
    sp.run(cmd4)
    sp.run(cmd5)
    sp.run(cmd6)
    sp.run(cmd7)







def Print(dataname,thr):
    
    pixel = Img(dataname)

    bgr = pixel.read()
    hsv = pixel.hsv()
    satu = hsv[:,:,1]
    gray = hsv[:,:,2]
    row,col,color = bgr.shape


    if row == 3648:
        # rotate photo
        print("Rotate photo")
        pixel.rotate()
        bgr = pixel.read()


   
 
    thr = int(thr)
    ret,satu1 = cv2.threshold(satu,thr,255,cv2.THRESH_BINARY)
    #ret,satu2 = cv2.threshold(satu,100,255,cv2.THRESH_BINARY)
    #ret,gray = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)
    
    np.savetxt("./sataBINARY.txt",satu1,fmt = "%d")

    name = dataname.split("/")
    name = name[-1]
    print(name)
    #output_dire = "Users/hikaru/Desktop/BEX/software/output/"
    output_dire = "C:Users/sphen/Desktop/BEC/output/"
    cv2.imwrite("../output/"+str(thr)+"_"+name,satu1)

    cv2.imshow("print",satu1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#    cv2.imwrite(output_dire+"Binary"+str(thr)+name,satu)


    
def Detection(dataname,thr,sigma):

    print("Read the {}".format(dataname))
    
    times = sigma

    dataname_ary = dataname.split("/")
    
    #outputname = "/Users/hikaru/Desktop/BEX/software/output/C__"+dataname_ary[-1]
    outputname = "C:/Users/sphen/Desktop/BEC/output/C__"+dataname_ary[-1]
    fout = open("setting.txt","wt")
    
    fout.write(dataname+"\n")
    fout.write(str(thr)+"\n")
    fout.write(str(times)+"\n")
    fout.write(outputname+"\n")
    
    fout.close()



# Run Macro
    #cmd1 = ["./RUN"] 
    cmd1 = ["./Detection.exe"]
    sp.run(cmd1)





def BackEndMode(thr,sigma,TargetDir):
    print("Back End mode")
    
    # write out setting file


    # Loop

    FileNumInTarDir = []
    FileNameInTarDir = os.listdir(TargetDir) # init list
    debugcount = 0

    while True:

        FileNum = len(os.listdir(TargetDir))
        #print(FileNum)
        FileNumInTarDir.append(FileNum)
        print("Waiting...")
        debugcount = debugcount + 1
        #print("debugcount=",debugcount)
        if len(FileNumInTarDir) > 2 :

            del FileNumInTarDir[0] # delete first index
            #print(FileNumInTarDir)
            #print(FileNameInTarDir)

            # input new data case
            if( FileNumInTarDir[0] != FileNumInTarDir[1]):


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
                sp.run(cmdshow,shell = True)                

                FileNameInTarDir = NowFileNameInTarDir


        time.sleep(1)
        
        if debugcount>100:
            break


def stop_backend():
    file = open("stop.txt","wt")
    file.close()


