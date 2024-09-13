#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:42:14 2023

@author: samwebb
"""
import shutil
import math
import sys
import os
import fnmatch

from PIL import ImageTk
import numpy as np
import pyometiff

import globalfuncs


def edgezoom(fbl,**kw):
    [fbn,fb]=fbl
    if fb['zoom'][0:4]==[0,0,-1,-1]:
        globalfuncs.setList(fb['zoom'],[1,1,fb['data'].data.get(0).shape[1]-2,fb['data'].data.get(0).shape[0]-2,0,0])
    else:
        globalfuncs.setList(fb['zoom'],[fb['zoom'][0]+1,fb['zoom'][1]+1,fb['zoom'][2]-1,fb['zoom'][3]-1,0,0])
    #globalfuncs.setList(self.zmxyc,[0,0,0,0])

def saveDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']    
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
    
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            #display image
            datind=fb['data'].labels.index(chn) + 2
            pic = fb['data'].data.get(datind)[::-1,:]
            mi = fb['data'].mapindex[::-1,:]
            datlab = chn
            if len(fb['mask'].mask)!=0:
                picmsk=np.transpose(fb['mask'].mask[::-1,:])
            else:
                picmsk=[]

            ps['display'].placeData(np.transpose(pic),np.transpose(mi),None,xax=fb['data'].xvals,yax=fb['data'].yvals,domask=True,mask=picmsk,datlab=datlab)
            #save
            fn=fb['fname'] + '_MD_' + chn + '.jpg'
            ps['display'].savejpgimage(fn)
        j+=1       
    
def saveTiffDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']    
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
    
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            #display image
            datind=fb['data'].labels.index(chn) + 2
            pic = fb['data'].data.get(datind)[::-1,:]
            mi = fb['data'].mapindex[::-1,:]
            datlab = chn
            if len(fb['mask'].mask)!=0:
                picmsk=np.transpose(fb['mask'].mask[::-1,:])
            else:
                picmsk=[]

            ps['display'].placeData(np.transpose(pic),np.transpose(mi),None,xax=fb['data'].xvals,yax=fb['data'].yvals,domask=True,mask=picmsk,datlab=datlab)
            
            #save
            fn=fb['fname'] + '_MD_' + chn + '.tiff'
            ps['display'].saveHDimage(fn)
        j+=1    

def saveAnimateGIFDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']    
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()

    fbnm=fb['fname']
    imgstack=[]
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            #display image
            datind=fb['data'].labels.index(chn) + 2
            pic = fb['data'].data.get(datind)[::-1,:]
            mi = fb['data'].mapindex[::-1,:]
            datlab = chn
            if len(fb['mask'].mask)!=0:
                picmsk=np.transpose(fb['mask'].mask[::-1,:])
            else:
                picmsk=[]

            ps['display'].placeData(np.transpose(pic),np.transpose(mi),None,xax=fb['data'].xvals,yax=fb['data'].yvals,domask=True,mask=picmsk,datlab=datlab)
            #save
            imgstack.append(ImageTk.getimage(ps['display'].image))
            
        j+=1        
    fo=imgstack[0]
    fo.save(fbnm+"_animated.gif", format="GIF", append_images=imgstack,save_all=True, duration=100,loop=0)
    print("Image display animation saved in: "+fbnm+"_animated.gif")

def saveNumpyDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']    
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()

    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            fn=fb['fname']+'_'+chn+'.npy'
            datind=fb['data'].labels.index(chn) + 2
            np.save(fn,fb['data'].data.get(datind))
            print("Image display array saved in: "+fn)    
        j+=1
            

def saveOMEDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']    
        
    j=0
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()

    fbnm=fb['fname']    
    imgstack=[]
    chnused=[]
    for chn in fb['data'].labels.copy():
        if chn in oklabs:
            chnused.append(chn)
            datind=fb['data'].labels.index(chn) + 2
            imgstack.append(fb['data'].data.get(datind))
        j+=1      
    
    curXres=int(abs(fb['data'].xvals[2]-fb['data'].xvals[1])*100000)/100000.
    curYres=int(abs(fb['data'].yvals[2]-fb['data'].yvals[1])*100000)/100000.
    metadata = {
        "PhysicalSizeX":curXres,
        "PhysicalSizeXUnit":'mm',
        "PhysicalSizeY":curYres,
        "PhysicalSizeYUnit":'mm',
        "PhysicalSizeZ":1.,
        "PhysicalSizeZUnit":'mm'
        }
    
    chls={}
    for going in chnused:
        nd={"Name":going,
            "SamplesPerPixel":1,
            "ExcitationWavelength":fb['data'].energy,
            "ExcitationWavelengthUnit":"eV"}
        chls[going]=nd
    metadata["Channels"]=chls
    
    imgstack=np.array(imgstack,dtype=np.int32)
    cs = list(imgstack.shape)
    cs.insert(0,1)
    cs.insert(0,1)
    imgstack=imgstack.reshape(cs)
    
    print ('channel check:',imgstack.shape,len(chls))
    
    dimension_order='ZTCYX'
    fn=fbnm + '_OME.tiff'
    writer=pyometiff.OMETIFFWriter(
        fpath=fn,
        dimension_order=dimension_order,
        array=imgstack,
        metadata=metadata,
        explicit_tiffdata=False)

    writer.write()                
    print("Image OME data saved in: "+fn)    
    
def saveProcessed(fbl,**kw):
    [fbn,fb]=fbl
    fn = fb['fname']+'_process.dat'

    if fb['data'].hasHDF5:
        fb['data'].hdf5group.attrs.create("channels",fb['data'].channels)
        fb['data'].hdf5group.attrs.create("labels",fb['data'].labels)
        fb['data'].hdf5.flush()
        hdffn=os.path.splitext(fn)[0]+".hdf5"
        shutil.copy(fb['data'].hdf5.filename,hdffn)
        print("hdf5 saved")
    
    fb['changes']=0
    
def setMaxDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']   
    
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()

    for l in oklabs:
        ps['display'].scalemaxlist[l]=float(ps['value'])
    

def defaultMaxDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']   
    
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()

    for l in oklabs:
        if l in ps['display'].scalemaxlist: 
            del ps['display'].scalemaxlist[l]

def balanceMaxDisplay(fbl,**kw):
    [fbn,fb]=fbl
    ps=kw['kw']       
    
    if 'regex' in ps:
        oklabs = fnmatch.filter(fb['data'].labels,ps['regex'])
    else:
        oklabs = fb['data'].labels.copy()
        
    
    iters=list(ps['dataFB'].keys())
    for l in oklabs:
        cmax=0
        for nbuf in iters:
            buf=ps['dataFB'][nbuf]
            dataind=buf['data'].labels.index(l)+2
            dr=buf['data'].data.get(dataind)[::-1,:]#[::-1,:,dataind]
            if buf['zoom'][0:4]!=[0,0,-1,-1]:
                dr=dr[buf['zoom'][1]:buf['zoom'][3],buf['zoom'][0]:buf['zoom'][2]]
            pv  = np.max(dr)                
            cmax = max(pv,cmax)
            ps['display'].scalemaxlist[l]=cmax
 
