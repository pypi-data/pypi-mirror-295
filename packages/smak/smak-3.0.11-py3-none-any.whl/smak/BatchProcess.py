#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:52:47 2023

@author: samwebb
"""
import fnmatch
import math
import os
import sys

import numpy as np
import cv2 as cv
from skimage.transform import rescale as skrescale

from AdvancedFilteringClass import advancedfilters
import globalfuncs
import ImageGet
import MathWindowClass
from ThresholdingClass import thresholdfilters



def maskaszoom(fbl,**kw):
    [fbn,fb]=fbl
    if fb['zoom'][2]!=-1 and fb['zoom'][3]!=-1:
        fb['mask'].mask=np.zeros((fb['data'].data.shape[0],fb['data'].data.shape[1]),dtype=np.float32)
        fb['mask'].mask[fb['zoom'][1]:fb['zoom'][3],fb['zoom'][0]:fb['zoom'][2]]=np.ones(fb['data'].data.get(0)[fb['zoom'][1]:fb['zoom'][3],fb['zoom'][0]:fb['zoom'][2]].shape)

    else:
        fb['mask'].mask=np.ones((fb['data'].data.shape[0],fb['data'].data.shape[1]),dtype=np.float32)
 
def invertMask(fbl,**kw):
    [fbn,fb]=fbl
    if len(fb['mask'].mask)>0:
        md = np.where(fb['mask'].mask==0,1,0)
    else:
        md = np.ones((fb['data'].data.shape[0],fb['data'].data.shape[1]),dtype=np.float32)      

def addChanFromMask(fbl,**kw):
    [fbn,fb]=fbl 
    ps=kw['kw']
    if len(fb['mask'].mask)>0:
        md = fb['mask'].mask
    else:
        md = np.zeros((fb['data'].data.shape[0],fb['data'].data.shape[1]),dtype=np.float32)
        
    svtype='ROImask'
    i=1
    newname=svtype
    while newname in fb['data'].labels:
        newname=svtype+str(i)
        i+=1    
    ps['addchan'](md,newname,fbuffer=fbn)    
    
    
def addMaskToChan(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']

    if len(fb['mask'].mask)==0:
        print('no mask in ',fbn)
        return
    
    datind=fb['data'].labels.index(ps['destchan'])+2
    data=fb['data'].data.get(datind)
    #find power of 2...
    factor=globalfuncs.powernext(int(max(np.ravel(data))))
    fb['data'].data.put(datind,data+fb['mask'].mask*float(factor))
    fb['data'].data.put(datind,data)  

def removeMaskFromChan(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']   
    
    if len(fb['mask'].mask)==0:
        print('no mask in ',fbn)
        return
    
    datind=fb['data'].labels.index(ps['destchan'])+2
    data=fb['data'].data.get(datind)
    data=np.where(fb['mask'].mask>0,0,data)
    fbl['data'].data.put(datind,data)    
    
        
def filterGeneral(fbl,**kw):
    typd={'Mean':'-avg','Median':'-med','Min':'-min','Max':'-max','Invert':'-inv','Blur':'-blur','Unsharp':'-shrp','Denoise':'-den','Open':'-open','Close':'-close','Gradient':'-grad','TopHat':'-toph','BlackHat':'-blackh','FFT':'-fft','iFFT':'-ifft','Similarity':'-sim','SimBlur':'-sblr','MeanShift':'-ms','EDT':'-edt'}          
    [fbn,fb]=fbl
    ps=kw['kw']
    ppass={}
    for k in ps:
        if k in ['filter']: ppass[k]=ps[k]
        if k in ['size']: ppass[k]=int(ps[k])
        if k in ['sigma']: ppass[k]=float(ps[k])
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
    
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            newdata = advancedfilters(fb['data'].data.get(j+2),**ppass)
     
            svtype=typd[ps['filter']]
            i=1
            newname=chn+svtype
            while newname in fb['data'].labels:
                newname=chn+svtype+str(i)
                i+=1
            
            ps['addchan'](newdata,newname,fbuffer=fbn)
        j+=1

def threshGeneral(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']
    ppass={}
    for k in ps:
        if k in ['filter']: ppass[k]=ps[k]
        if k in ['level','value']: ppass[k]=float(ps[k])
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
    
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            newdata = thresholdfilters(fb['data'].data.get(j+2),**ppass)
     
            svtype='-thresh'
            i=1
            newname=chn+svtype
            while newname in fb['data'].labels:
                newname=chn+svtype+str(i)
                i+=1
            
            ps['addchan'](newdata,newname,fbuffer=fbn)
        j+=1    
        
        
def mathSingleChan(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']        
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
        
    if ps['oper'] in ['Horz Shift','Vert Shift','Add Scalar','Subtract Scalar','Multiply Scalar','Divide Scalar']:
        ext = float(ps['scalar'])
    else:
        ext = None
    if ps['oper'] in ['Add Scalar','Subtract Scalar','Multiply Scalar','Divide Scalar']:
        ps['oper'] = ps['oper'].split()[0]
    
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            
            newdata=MathWindowClass.MathOp(ps['oper'], fb['data'].data.get(j+2), ext)
     
            svtype=ps['oper'].lower()
            i=1
            newname=chn+'-'+svtype
            while newname in fb['data'].labels:
                newname=chn+'-'+svtype+str(i)
                i+=1
            
            ps['addchan'](newdata,newname,fbuffer=fbn)
        j+=1        

def mathTwoChan(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']        
        
    Aind=fb['data'].labels.index(ps['Adata'])+2
    Adata = fb['data'].data.get(Aind)
    if ps['Bdata'][0]=='&':  #denote for scalar
        Bdata = float(ps['Bdata'][1:])
        blab = 'scalar'
    else:
        Bind = fb['data'].labels.index(ps['Bdata'])+2
        Bdata = fb['data'].data.get(Bind)
        blab = ps['Bdata']
    option={}
    if ps['oper'] in ['Translate','Register','Transform','Align']:
        if fb['zoom'][0:4]!=[0,0,-1,-1]:  
            Adata = Adata[fb['zoom'][1]:fb['zoom'][3],fb['zoom'][0]:fb['zoom'][2]]
            Bdata = Bdata[fb['zoom'][1]:fb['zoom'][3],fb['zoom'][0]:fb['zoom'][2]]
            option['fullB']= fb['data'].data.get(Bind)
            
    newdata=MathWindowClass.MathOp(ps['oper'], Adata, Bdata, option)
     
    svtype=ps['Adata']+'.'+ps['oper'].lower()+'.'+blab
    i=1
    newname=svtype
    while newname in fb['data'].labels:
        newname=svtype+'-'+str(i)
        i+=1
            
    ps['addchan'](newdata,newname,fbuffer=fbn)



def changeColorRGBtoLAB(fbl,**kw):
    ps=kw['kw']
    doCamColorConversion(fbl,'lab',ps['addchan'])

def changeColorRGBtoHSV(fbl,**kw):
    ps=kw['kw']
    doCamColorConversion(fbl,'hsv',ps['addchan'])

def changeColorRGBtoYCC(fbl,**kw):
    ps=kw['kw']
    doCamColorConversion(fbl,'ycc',ps['addchan'])

def changeColorRGBtoXYZ(fbl,**kw):
    ps=kw['kw']
    doCamColorConversion(fbl,'xyz',ps['addchan'])

def doCamColorConversion(fbl,ct,addchan):
    [fbn,fb]=fbl
    colorspaceChange = {
        'lab':cv.COLOR_RGB2LAB,
        'hsv':cv.COLOR_RGB2HSV,
        'ycc':cv.COLOR_RGB2YCrCb,
        'xyz':cv.COLOR_RGB2XYZ}
    colorspaceBasenames= {
        'lab':['L','A','B'],
        'hsv':['H','S','V'],
        'ycc':['Y','Cr','Cb'],
        'xyz':['cX','cY','cZ']}    

    if 'RED' not in fb['data'].labels or 'GREEN' not in fb['data'].labels or 'BLUE' not in fb['data'].labels:
        print ('color channels RED GREEN BLUE not present, cancelled...')
        return

    rgbimg = np.zeros((fb['data'].data.get(0).shape[0],fb['data'].data.get(0).shape[1],3))
    rgbimg[:,:,0] = fb['data'].data.get(fb['data'].labels.index('RED')+2)
    rgbimg[:,:,1] = fb['data'].data.get(fb['data'].labels.index('GREEN')+2)
    rgbimg[:,:,2] = fb['data'].data.get(fb['data'].labels.index('BLUE')+2)

    newlab = cv.cvtColor(rgbimg.astype(dtype=np.uint8), colorspaceChange[ct])

    #save
    for basename in colorspaceBasenames[ct]:
        newname=globalfuncs.fixlabelname(basename)                
        ind=1
        ok=False            
        while not ok:    
            if newname in fb['data'].labels:
                newname=globalfuncs.fixlabelname(basename+'_'+str(ind))
                ind+=1
            else:
                ok=True
        #add the channel
        addchan(newlab[:,:,colorspaceBasenames[ct].index(basename)],newname,fbuffer=fbn)          
       
def interpolateMissingRows(fbl,**kw):
    ps=kw['kw']
    [fbn,fb]=fbl
    
    for chn in fb['data'].labels.copy():
        ind = fb['data'].labels.index(chn)
        dchan=fb['data'].data.get(ind+2)
        edit=False
        for j in range(1,dchan.shape[0]-1):
            if j%10==0: print(j)
            if sum(dchan[j,:].astype(np.int32))==0:
                edit=True
                print(j,"empty")
                dchan[j,:]=(dchan[j-1,:]+dchan[j+1,:])/2.0
        if edit:
            fb['data'].data.put(ind+2,dchan)      
    

def changeFileResolution(fbl,**kw):
    ps=kw['kw']
    [fbn,fb]=fbl
    
    #['sizeX, sizeY']
    newXR=float(ps['sizeX'])
    newYR=float(ps['sizeY'])
    curXres=int(abs(fb['data'].xvals[2]-fb['data'].xvals[1])*100000)/100000.
    curYres=int(abs(fb['data'].yvals[2]-fb['data'].yvals[1])*100000)/100000.       
    xscale=curXres/newXR
    yscale=curYres/newYR

    newfn=fb['fname']+'_res_'+str(newXR)+'_'+str(newYR)+'.hdf5'

    newfile=ImageGet.EmptyHDF5(newfn)
    pdict={}
    pdict['channels']=fb['data'].channels
    pdict['type']=fb['data'].type
    pdict['isVert']=fb['data'].isVert
    pdict['labels']=fb['data'].labels
    pdict['comments']=fb['data'].comments
    pdict['energy']=fb['data'].energy
    newfile.cleanString()

    imy=fb['data'].data.get(0)
    imx=fb['data'].data.get(1)
    if ps['display'].zmxyi[2]!=-1 and ps['display'].zmxyi[3]!=-1:
        imx=imx[::-1,:]
        imx=imx[ps['display'].zmxyi[1]:ps['display'].zmxyi[3],ps['display'].zmxyi[0]:ps['display'].zmxyi[2]]
        imx=imx[::-1,:]
        imy=imy[::-1,:]
        imy=imy[ps['display'].zmxyi[1]:ps['display'].zmxyi[3],ps['display'].zmxyi[0]:ps['display'].zmxyi[2]]
        imy=imy[::-1,:]
    if xscale<1 or yscale<1:
        aa=True
    else:
        aa=False
    newdatay=skrescale(imy,(xscale,yscale),mode='edge')
    newdatax=skrescale(imx,(xscale,yscale),mode='edge')

    xv=newdatay[0,:]
    yv=newdatax[:,0]
 
    print (newdatay[0,:])   
    print (newdatay[-1,:])   
    print (newdatax[:0])   
    print (newdatax[:-1])   
 
    newfile.addParams(xv,yv,pdict)
    newfile.data.put(0,newdatay)
    newfile.data.put(1,newdatax)
    for j in range(fb['data'].channels):
        im=fb['data'].data.get(j+2)
        if ps['display'].zmxyi[2]!=-1 and ps['display'].zmxyi[3]!=-1:
            im=im[::-1,:]
            im=im[ps['display'].zmxyi[1]:ps['display'].zmxyi[3],ps['display'].zmxyi[0]:ps['display'].zmxyi[2]]
            im=im[::-1,:]
        if xscale<1 or yscale<1:
            aa=True
        else:
            aa=False
        newdata=skrescale(im,(xscale,yscale),mode='edge')
        newfile.data.put(j+2,newdata)
    newfile.close()
    
def changeFileVertFlip(fbl,**kw):
    ps=kw['kw']
    doFileTransformationGen(fbl,'vert',ps['display'])

def changeFileHorzFlip(fbl,**kw):
    ps=kw['kw']
    doFileTransformationGen(fbl,'horz',ps['display'])  

def changeFileRotate(fbl,**kw):
    ps=kw['kw']
    doFileTransformationGen(fbl,'rot',ps['display'])
    
def doFileTransformationGen(fbl,op,display):
    [fbn,fb]=fbl    
    #get new filename       
    newfn=fb['fname']+'_tf_'+op+'.hdf5'
    
    if op == 'vert':
        f = MathWindowClass.VFlipOp
    elif op == 'horz':
        f = MathWindowClass.HFlipOp
    else:
        f = np.transpose

    newfile=ImageGet.EmptyHDF5(newfn)
    pdict={}
    pdict['channels']=fb['data'].channels
    pdict['type']=fb['data'].type
    pdict['isVert']=fb['data'].isVert
    pdict['labels']=fb['data'].labels
    pdict['comments']=fb['data'].comments
    pdict['energy']=fb['data'].energy
    newfile.cleanString()

    imy=fb['data'].data.get(0)
    imx=fb['data'].data.get(1)
    if display.zmxyi[2]!=-1 and display.zmxyi[3]!=-1:
        imx=imx[::-1,:]
        imx=imx[display.zmxyi[1]:display.zmxyi[3],display.zmxyi[0]:display.zmxyi[2]]
        imx=imx[::-1,:]
        imy=imy[::-1,:]
        imy=imy[display.zmxyi[1]:display.zmxyi[3],display.zmxyi[0]:display.zmxyi[2]]
        imy=imy[::-1,:]

    xv=imy[0,:]
    yv=imx[:,0]
 
    newdatay=f(imy)
    newdatax=f(imx)

    fxv=newdatay[0,:]
    fyv=newdatax[:,0]

    if op == 'Rotate':
        newfile.addParams(fxv,fyv,pdict)#(yv,xv,pdict)
    else:
        newfile.addParams(fxv,fyv,pdict)

    newfile.data.put(0,newdatay)
    newfile.data.put(1,newdatax)
    for j in range(fb['data'].channels):
        im=fb['data'].data.get(j+2)
        if display.zmxyi[2]!=-1 and display.zmxyi[3]!=-1:
            im=im[::-1,:]
            im=im[display.zmxyi[1]:display.zmxyi[3],display.zmxyi[0]:display.zmxyi[2]]
            im=im[::-1,:]

        newdata=f(im)
        newfile.data.put(j+2,newdata)
    newfile.close()            
    
    
    
    
    
    
    
    
    