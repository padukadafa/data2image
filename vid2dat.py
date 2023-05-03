import cv2 as cv
from time import process_time
import glob
import numpy as np
from tqdm import tqdm
import os
dimension = (144,256)
length = dimension[0]*dimension[1]
breakcode = "00000000111111110000000011111111000000001111111100000000111111110000000011111111"
data = ""

def check(source):
    if source[0][0] <= 144 and source[0][1] <= 144 and source[1][0] <= 144 and source[1][1] <= 144 :
        return True
    return False

def bin2arraybin(data):
    temp=[]
    tmp=''
    count=0
    for i in range(0,len(data),8):
        dat = data[i:i+8]
        tmp= tmp+dat
        tmpl = int(len(tmp)/8)
        count+=1
        if tmp[tmpl-1:(tmpl-1)*8+8] != breakcode[tmpl-1:(tmpl-1)*8+8]:
            tmp=""
            count=0
            # print(i)
        # if count > 5:
        #     print("asdasdasd ",count)
        if count ==6:
            temp = temp[:-5]
            # print("asdasdasd")
            break
        
        temp.append(dat)
    
    return temp
    

def img2bin(source):
    npdata = np.zeros((dimension[0],dimension[1],3),np.uint8)
    tmp = ""
    j=0
    for i in range(0,length*2):
        if i%(dimension[1])==0 and i != 0:
            j+=1
        # print(i)
        if j==dimension[0]:
            break
        if check([source[j*2,i*2-j*dimension[1]*2],source[j*2+1,i*2-j*dimension[1]*2+1]]):
            tmp=tmp+'1'
        else:
            tmp=tmp+'0'
            
    
    return tmp
tmp=b''
cap = cv.VideoCapture('output.mp4')
j=0
while cap.isOpened():
    
    ret,frame = cap.read()
    # print("Process")
    if not ret:
        print(ret)
        break
    bin = img2bin(frame)
    # print(len(bin))
    # cv.imshow("",frame)
    # cv.waitKey(0)
    
    arrbin = bin2arraybin(bin)
    print(len(arrbin)*8)
    
    for i in arrbin:
        
        if int(i,2) ==255:
            continue
        tmp=tmp+int(i,2).to_bytes(1,byteorder='big')
    # j+=len(tmp)
    # print(j)
with open('restesimg.png','wb') as f:
    # print(tmp)
    f.write(tmp)
