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
def image2video():
    os.system('ffmpeg -framerate 24 -i cache/%d.png -c:v copy output.mp4 -y')


def removeJunk():
    filelist = glob.glob(os.path.join('cache', "*"))
    for f in tqdm(filelist):
        os.remove(f)

def dat2bin(source):
    dump=""
    for i in tqdm(source):
        dump = dump + str(bin(i)[2:].zfill(8))
    dump = dump + breakcode
    return dump
def bin2image(source,end):
    npdata = np.zeros((dimension[0]*2,dimension[1]*2,3),np.uint8)
    j=0
    print(len(source))
    for i in range(0,end):
        if i%(dimension[1])==0 and i != 0:
            j+=1
        # print(i)
        if j==dimension[0]:
            break
        if source[i] == '0':
            npdata[j*2,i*2-j*dimension[1]*2] = (255,255,255)
            npdata[j*2+1,i*2-j*dimension[1]*2] = (255,255,255)
            npdata[j*2,i*2-j*dimension[1]*2+1] = (255,255,255)
            npdata[j*2+1,i*2-j*dimension[1]*2+1] = (255,255,255)

    return npdata
def createimages(source):
    end=length

    for i in tqdm(range(0,int(len(source)/length)+1)):
        if i == int(len(source)/length):
            end=len(source)%length
            cv.imwrite('cache/'+str(i+1)+'.png',np.zeros((dimension[0]*2,dimension[1]*2,3),np.uint8))

        img = bin2image(data[i*length:i*length+end],end)
        cv.imwrite('cache/'+str(i)+'.png',img)
    
with open('name.txt','rb') as f:
    print("Removing junk")
    removeJunk()
    source_data = f.read()
    # print(source_data)
    # print(source_data)
    print("convert data to binary")
    data = dat2bin(source_data)
    createimages(data)
    print(len(data))
    image2video()
    