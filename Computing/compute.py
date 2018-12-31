import sys

from PIL import Image
import matplotlib.pyplot as plt
from Constants import Constant_Images
import numpy as np

def convert2gray(img):
    #original image size
    width, height = img.size

    #create empty image
    new_im = Image.new('I', [width,height])
    new_px=new_im.load()

    #hesaplamalar
    sum = 0
    px = img.load()

    for i in range(0, width):
        for j in range(0, height):
            sum += (px[i, j][0]/255) * 0.2126
            sum += (px[i, j][1]/255) * 0.7152
            sum += (px[i, j][2]/255) * 0.0722
            result = round(sum*255)
            new_px[i, j] = result
            sum = 0

    return new_im

def  zoom_in(img,channel="RGB"):
    zoom_factor = 1.6
    width_original, height_original = img.size
    new_width = int(width_original*zoom_factor)
    new_height = int(height_original*zoom_factor)

    im = nearestNeighborScaling(img,new_width,new_height,channel=channel)
    return im

def  zoom_out(img,channel="RGB"):
    zoom_factor = 0.4
    width_original, height_original = img.size
    new_width = int(width_original*zoom_factor)
    new_height = int(height_original*zoom_factor)

    im = nearestNeighborScaling(img,new_width,new_height,channel=channel)
    return im

def nearestNeighborScaling(source, newWid, newHt,channel='RGB'):
    source_px = source.load()
    target = Image.new(channel, [newWid, newHt])
    target_px = target.load()
    width, height = source.size

    for x in range(0, newWid):
      for y in range(0, newHt):
        srcX = int(round(float(x) / float(newWid) * float(width)))
        srcY = int(round(float(y) / float(newHt) * float(height)))
        srcX = min(srcX, width-1)
        srcY = min(srcY, height-1)
        target_px[x, y] = source_px[srcX, srcY]

    return target

def draw_hist(img,channel='I'):
    px = img.load()
    w,h = img.size

    if (channel=='I'):

        dict={}#sayaç

        for i in range(0, w):
            for j in range(0, h):
              val = px[i, j]
              if val not in dict.keys():
                  dict[val] = 0

        for i in range(0, w):
            for j in range(0, h):
              val = px[i, j]
              if val in dict.keys():
                  dict[val] = dict[val] + 1

        print(dict)
        plt.bar(dict.keys(), dict.values(), 1, color='gray')
        plt.savefig(Constant_Images.hist_image_path+"hist.png")
        im = Image.open(Constant_Images.hist_image_path+"hist.png")
        return im
    else:
        dictR = {}
        dictG = {}
        dictB = {}
        for i in range(0, w):
            for j in range(0, h):
                valR = px[i, j][0]
                valG = px[i, j][1]
                valB = px[i, j][2]

                if valR not in dictR.keys():
                    dictR[valR] = 0
                if valG not in dictG.keys():
                    dictG[valG] = 0
                if valB not in dictB.keys():
                    dictB[valB] = 0

        for i in range(0, w):
            for j in range(0, h):
                valR = px[i, j][0]
                valG = px[i, j][1]
                valB = px[i, j][2]

                if valR in dictR.keys():
                    dictR[valR] = dictR[valR] + 1
                if valG in dictG.keys():
                    dictG[valG] = dictG[valG] + 1
                if valB in dictB.keys():
                    dictB[valB] = dictB[valB] + 1

        plt.bar(dictR.keys(), dictR.values(), 1, color='red')
        plt.savefig(Constant_Images.hist_image_path+"R_hist.png")
        imR = Image.open(Constant_Images.hist_image_path+"R_hist.png")
        plt.cla()
        plt.bar(dictG.keys(), dictG.values(), 1, color='green')
        plt.savefig(Constant_Images.hist_image_path+"G_hist.png")
        imG = Image.open(Constant_Images.hist_image_path+"G_hist.png")
        plt.cla()
        plt.bar(dictB.keys(), dictB.values(), 1, color='blue')
        plt.savefig(Constant_Images.hist_image_path+"B_hist.png")
        imB = Image.open(Constant_Images.hist_image_path+"B_hist.png")

        return imR, imG, imB

def median(img, channel="I"):
    px = img.load()
    w, h = img.size

    #yeni tesim boyutları
    w2, h2 = w - 4, h - 4
    target_im = Image.new(channel, [w2, h2])
    target_px = target_im.load()

    if(channel=="I"):#gri ise
        #resim
        for i in range(3, w2):
            for j in range(3, h2):
               list = []
               #filtre
               for k in range(5):
                   for l in range(5):
                        list.append(px[i+k, j+l])

               list.sort()
               target_px[i, j] = list[12]
               list.clear()
    else:
        for i in range(3, w2):
            for j in range(3, h2):
                listR = []
                listG = []
                listB = []
                for k in range(5):
                    for l in range(5):
                        listR.append(px[i + k, j + l][0])
                        listG.append(px[i + k, j + l][1])
                        listB.append(px[i + k, j + l][2])

                listR.sort()
                listG.sort()
                listB.sort()
                target_px[i, j] = (listR[12],listG[12],listB[12])
                listR.clear()
                listG.clear()
                listB.clear()

    return target_im

def edge_detect(img, channel="I"):
    #prewitt
    print("Kenarı bulunacak resim tip :",img.mode)

    px = img.load()
    w, h = img.size

    # yeni tesim boyutları
    w2, h2 = w - 2, h - 2
    target_im = Image.new(channel, [w2, h2])
    target_px = target_im.load()


    if channel == "I":
        for i in range(1, w2):
            for j in range(1, h2):
                sum_v = 0
                sum_v += px[i, j]*1
                sum_v += px[i, j+2]*(-1)
                sum_v += px[i+1, j]*1
                sum_v += px[i+1, j+2]*(-1)
                sum_v += px[i+2, j]*1
                sum_v += px[i+2, j+2]*(-1)
                sum_v = abs(sum_v)

                sum_h = 0
                sum_h += px[i, j]*1
                sum_h += px[i, j+1]*1
                sum_h += px[i, j+2]*1
                sum_h += px[i+2, j]*(-1)
                sum_h += px[i+2, j+1]*(-1)
                sum_h += px[i+2, j+2]*(-1)
                sum_h = abs(sum_h)

                sum_total = sum_v+sum_h
                target_px[i,j] = sum_total
    else:#for rgb
        for i in range(1, w2):
                for j in range(1, h2):
                    col=[]
                    for rgb in range(0, 3):
                        sum_v = 0
                        sum_v += px[i, j][rgb] * 1
                        sum_v += px[i, j + 2][rgb] * (-1)
                        sum_v += px[i + 1, j][rgb] * 1
                        sum_v += px[i + 1, j][rgb] * (-1)
                        sum_v += px[i + 2, j][rgb] * 1
                        sum_v += px[i + 2, j][rgb] * (-1)
                        sum_v = abs(sum_v)

                        sum_h = 0
                        sum_h += px[i, j][rgb] * 1
                        sum_h += px[i, j + 1][rgb] * 1
                        sum_h += px[i, j + 2][rgb] * 1
                        sum_h += px[i + 2, j][rgb] * (-1)
                        sum_h += px[i + 2, j + 1][rgb] * (-1)
                        sum_h += px[i + 2, j + 2][rgb] * (-1)
                        sum_h = abs(sum_h)

                        sum_total = sum_v + sum_h
                        col.append(sum_total)

                    target_px[i, j] = (col[0],col[1],col[2])
                    col.clear()


    return target_im

def conv2d(img,filter, channel="I"):

    px = img.load()
    w, h = img.size

    #yeni tesim boyutları
    w2, h2 = w - (len(filter)-1), h - (len(filter)-1)
    target_im = Image.new(channel, [w2, h2])
    target_px = target_im.load()

    print("filter:",len(filter))
    if (channel == "I"):  # gri ise
        # resim
        for i in range(len(filter)-2, w2):
            for j in range(len(filter)-2, h2):
                sum = 0
                # filtre
                for k in range(0,len(filter)):
                    for l in range(0,len(filter)):
                       sum += px[i+k,j+l] * filter[k][l]

                target_px[i, j] = abs(round(sum))
                sum=0
        return target_im
    else:
        for i in range(0, w2):
            for j in range(0, h2):
                sumR, sumG, sumB = 0, 0, 0
                for k in range(3):
                    for l in range(3):
                        sumR += px[i + k, j + l][0]*filter[k][l]
                        sumG += px[i + k, j + l][1]*filter[k][l]
                        sumB += px[i + k, j + l][2]*filter[k][l]

                target_px[i, j] = (abs(round(sumR)), abs(round(sumG)), abs(round(sumB)))
                sumR, sumG, sumB = 0, 0, 0

    return target_im

def dilation(img,se_len=3):
    px = img.load()
    w, h = img.size

    target_im = Image.new('I', [w, h])
    target = target_im.load()

    offset = int((se_len+1)/2)
    for i in range(0,w-offset):
        for j in range(0,h-offset):
            if(px[i+offset,j+offset] == 255): #yapısal elemanın ortası eşleşiyor ise
                for k in range(se_len):
                    for l in range(se_len):
                        target[i+k,j+l]=255 #doldur

    return target_im

def erosion(img,se_len=3):
    px = img.load()
    w, h = img.size

    target_im = Image.new('I', [w, h])
    target = target_im.load()

    offset = int((se_len+1)/2)
    for i in range(0,w-offset):
        for j in range(0,h-offset):
            counter = 0
            for k in range(se_len):
                    for l in range(se_len):
                        if(px[i+k,j+l] == 255):
                            counter += 1

            if (counter == se_len * se_len):
                target[i + 1, j + 1] = 255  # doldur

            counter = 0
    return target_im

def opening(img,se_len=3):

    im1 = erosion(img=img)
    im2 = dilation(img=im1)
    return  im2

def closing(img,se_len=3):

    im1 = dilation(img)
    im2 = erosion(im1)
    return im2

def Thresholding(img):
    im = img.load()
    w, h = img.size
    total = w*h

    hist = {}
    for i in range(0,256):
        hist[i]=0
    for i in range(w):
        for j in range(h):
            intensity = im[i,j]
            hist[intensity] = hist[intensity] + 1

    sum = 0
    for i in range(0,256):
        sum += i*hist[i]

    sumB = 0
    wB = 0
    wF = 0
    varMax = 0
    threshold = 0

    for i in range(0,256):
        wB += hist[i]
        if(wB==0):
            continue
        wF = total - wB
        if(wF == 0):
            break
        sumB += i*hist[i]
        mB = sumB / wB
        mF = (sum - sumB) / wF

        varBetween = wB * wF * (mB-mF) * (mB-mF)
        if(varBetween > varMax):
            varMax = varBetween
            threshold = i

    return threshold

def gray2white_and_black(img,threshold):

    px = img.load()
    w, h = img.size

    target_im = Image.new('I', [w, h])
    target = target_im.load()

    for i in range(0,w):
        for j in range(0,h):
            if(px[i,j]>threshold):
                target[i,j] = 255
            else:
                target[i,j] = 0

    return target_im

def find_object(img):
    sys.setrecursionlimit(5000)

    px = img.load()
    w, h = img.size
    print("w,h:",w,h)

    target_im = Image.new('RGB', [w, h])
    target = target_im.load()


    def conquer(i,j,color=(255,0,0)):
        print("concuer i,j :",i,j)

        if (j > 0):
            if(px[i,j-1]==255 ):
                if target[i,j-1]!=color:
                    target[i,j-1]=color
                    conquer(i=i, j=(j-1))
        else:
            return

        if  (j < h-1):
            #print("üüü:",i,j)
            if (px[i, j+1] == 255 ):
                        if target[i,j+1]!=color:
                            target[i, j+1] = color
                            conquer(i=i, j=(j + 1))
        else:
            return

        if (i > 0):
            if (px[i-1, j] == 255):
                if target[i-1,j]!=color:
                    target[i-1, j] = color
                    conquer(i=(i-1), j=j)
        else:
            return

        if (i < w-1):
            if(px[i+1,j]==255):
                if target[i+1,j]!=color:
                    target[i + 1, j] = color
                    conquer(i=(i + 1), j=j)
        else:
            return


    for i in range(1,w):
        for j in range(1,h):
            if(px[i,j]== 255 and target[i,j]!=(255,0,0)):
                print("Yeni nesnenin başlangıç pikseli=> ",i,j)
                conquer(i,j)
                #break
        #break
    return target_im



