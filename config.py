import numpy as np
import cv2
import itertools
import sys
import time
import datetime
import matplotlib.pyplot as plt
import subprocess as sp
import random
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
    #output_dire = "../photo/"
    fmt         = ".jpg"


    dataname           = photo_dire+name+fmt

    output_hue         = output_dire+name+"_hue.txt"
    output_gray        = output_dire+name+"_gray.txt"
    output_saturation  = output_dire+name+"_saturation.txt"

    output_blue        = output_dire+name+"_blue.txt"
    output_green       = output_dire+name+"_green.txt" 
    output_red         = output_dire+name+"_red.txt"

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



    fout = open("basename.txt","w")
    fout.write(output_dire+name+"\n")
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




def find_error(name):

    


    photo_dire  = "../photo/"
    output_dire = "../data/"
    dire = "../photo/"
    fmt         = ".jpg"
    
    dataname    = photo_dire+name+fmt
    output_hue  = "./hue.txt"

    print("---Reading image---")

    pixel = Img(dataname)




    hsv   = pixel.hsv()

    print("---Extract Hue---")


    hue    = hsv[:,:,0]

    print("---Write Out hue.txt---")

    fout = open("HuePhotoName.txt","w")
    fout.write(name+"\n")
    fout.close()

    np.savetxt(output_hue,hue,fmt = "%d")


    print("---Run find_error.c---")
    cmd1 = ["root","-q","-l","find_error.c"]
    cmd2 = ["rm","./hue.txt"]
    cmd3 = ["rm","./HuePhotoName.txt"]

    sp.run(cmd1)
    sp.run(cmd2)
    sp.run(cmd3)

    print("---Finsh---")



def marking(name):


       
    photo_dire  = "../photo/"
    fmt = ".jpg"   
    dataname = photo_dire+name+fmt
    print("---Loading--- ",dataname)

    pixel = Img(dataname)


    print("---Extract HSV data---")

    hsv = pixel.hsv()

    hue = hsv[:,:,0]


    print("---Write Out Hue data---")

    np.savetxt("./hue.txt",hue,fmt="%d")

    
    print("---Compile macro---")

    cmd = ["g++","judge.cpp","-o","judge"]

    sp.run(cmd)


    print("---Run macro---")

    cmd1 = ["./judge"]

    sp.run(cmd1)



    print("---Loading center point data---")

#    center = np.loadtxt("center.txt",dtype = "int")
    center = np.loadtxt("outvalue.txt",dtype = "int")

    print("---Marking center point---")
    count = 0
    for point in center:
        
        cv2.circle(hsv,point,50,(0,255,255),3)
        print(point)

    #print("python count",count)
    print("---Output image---")
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imwrite("../output/"+name+".jpg",bgr)



def ratio(name):



    photo_dire  = "../photo/"
    output_dire = "../data/"
    dire = "../photo/"
    fmt         = ".jpg"
    
    dataname    = photo_dire+name+fmt
    output_hue  = "./hue.txt"

    print("---Reading image---")

    pixel = Img(dataname)




    hsv   = pixel.hsv()

    print("---Extract Hue---")


    hue    = hsv[:,:,0]

    print("---Write Out hue.txt---")

    fout = open("HuePhotoName.txt","w")
    fout.write(name+"\n")
    fout.close()

    np.savetxt(output_hue,hue,fmt = "%d")

    print("Run CountBunch")

    cmd1 = ["root","-q","-l","CountBunch.C"]

    sp.run(cmd1)



    center = np.loadtxt("ratio.txt",dtype = "int")  
    pitch = np.loadtxt("pitch.txt",dtype = "int")  



    print("---Marking point---")
    
    for point in center:
        
        cv2.circle(hsv,point,35,(120,255,255),3)
    
    for point in pitch:
        
        cv2.circle(hsv,point,5,(200,255,255),1)
        

    #print("python count",count)
    print("---Output image---")
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imwrite("../output/"+name+"mark.jpg",bgr)

    print("finsh")

    cmd2 = ["rm","./hue.txt"]
    cmd3 = ["rm","./HuePhotoName.txt"]


    sp.run(cmd2)
    sp.run(cmd3)



    




def sim(name):
    

    photo_dire  = "../photo/"
    output_dire = "../data/"
    dire = "../photo/"
    fmt         = ".jpg"
    
    dataname    = photo_dire+name+fmt


    print("---Reading image---")

    pixel = Img(dataname)

    hsv   = pixel.hsv()
    row,col,calor = hsv.shape
    #print (hsv)

    ini = hsv[2000,:,:]
    ini[:,0]= np.where((ini[:,0]<50)|(ini[:,0]>120),10,90)
    #ini[:,1]= np.where((ini[:,1]<50)|(ini[:,1]>120),10,90)
    ini[:,1] = 100
    ini[:,2] = 200
    for i in range(row):
        hsv[i,:,:] = ini

    delpixel =10
    for i in range(10):

        row = random.randint(1000,5000)
        col = random.randint(500,3000)
    #cv2.circle(hsv,(col,row),20,(100,100,100),3)
        for j in range(-delpixel,delpixel):

            for k in range(-delpixel,delpixel):
        
                hsv[row+k,col+j,0] = 90  # 90 is mean of LCP distuributon Hue
                hsv[row+k,col+j,1] = 100  # 35 is mean of LCP distuributon Satu
                hsv[2000+k,1000+j,0] = 90
                hsv[2000+k,1000+j,1] = 100
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    cv2.imwrite(photo_dire+name+"_SIM.JPG",bgr)

    #cmd1 = ["python","run.py","-r"]
    #cmd2 = ["python","run.py","-s"]



    #sp.run(cmd1)
    #sp.run(cmd2)




