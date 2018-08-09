# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:43:21 2018

@author: shamnaz
"""

#Pull a signal from a file given filename, start sample, and sample count
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc, font_manager
import os
import time
import json
import Tkinter as tk
import tkMessageBox
import tkFileDialog as fd
from IPython.core.debugger import Tracer
import scipy.io as spio
root = tk.Tk()
root.wm_title("DON'T CLOSE - HELPS TK RUN")
tkMessageBox.showinfo("Choose file to import","Choose a sigMF file")
fn = fd.askopenfilename()#  filename
fnMeta = fn[:-4]+'meta' #Trim last 4 and add 'meta' to get meta filename
fnData = fn[:-4]+'data' #Trim last 4 and add 'data' to get data filename
root.destroy() 
def PullBinarySample(filename, startSample, sampCount):
    # account for no buffer possible because signal starts at beginning of record
    if startSample<0:
        startSample=0
    
    with open(filename, "rb") as f:
        #Seek to startSample
        f.seek(startSample*4) #4bytes per sample (2x16 bit ints)
       # from IPython.core.debugger import Tracer
       # Tracer()() #this one triggers the debugger
        #Read in as ints
        raw = np.fromfile(f,dtype='int16',count=2*sampCount)
        #Convert interleaved ints into complex
        array=raw.reshape([sampCount,2])
        print array.shape
        #from IPython.core.debugger import Tracer
        #Tracer()()
        cmp = array[:,0]+array[:,1]*1j
        return cmp


#Initialize counter to limit number of plots
count=0

#Buffer before and after signal
buffer = 0


allSignals = json.load(open(fnMeta))

#Determine if the recording is wifi
wifi = allSignals['annotations'][0]['rfml:label'][0]=='wifi'

#find time step based on sample rate
Fs = allSignals['global']['core:sample_rate']
Fc = allSignals['capture'][0]['core:frequency']
dt = 1/Fs
hwmany = 1

#for each signal
for signal in allSignals['annotations']:

    #Read parameters for signal pulling
    startSamps = signal['core:sample_start']
    countSamps = signal['core:sample_count']
    sig_ref_no = signal['capture_details:signal_reference_number'].encode('ascii')
    dev_type = signal['rfml:label'][0].encode('ascii')
    dev_mid = signal['rfml:label'][1].encode('ascii')
    dev_id = signal['rfml:label'][2].encode('ascii')
    

    
    #Pull channel info if wifi or set if ADSB
    if wifi:
        lowFreq = signal['core:freq_lower_edge']
        upFreq = signal['core:freq_upper_edge']
    else:
        lowFreq = 1.085e9
        upFreq =  1.095e9

    #Pull Binary signal
    complexSignal = PullBinarySample(fnData,startSamps-buffer,countSamps+(2*buffer))
    mid = dev_type+"/"+dev_mid 
    filename = dev_type+"/"+dev_mid+"/"+dev_type+"_"+dev_mid+"_"+dev_id+".mat"
   # print complexSignal.shape
    if not os.path.exists(dev_type):
        os.makedirs(dev_type)
        if not os.path.exists(mid):
            os.makedirs(mid)
            if not os.path.exists(filename):
                with open(filename, 'ab'):
                    spio.savemat(filename, {'complexSignal':complexSignal})
    else:
        if not os.path.exists(mid):
            os.makedirs(mid)
            if not os.path.exists(filename):
                with open(filename, 'ab'):
                    spio.savemat(filename, {'complexSignal':complexSignal})

        else:
            if not os.path.exists(filename):
                with open(filename, 'ab'):
                    spio.savemat(filename, {'complexSignal':complexSignal})
            else:
                matfile = spio.loadmat(filename, appendmat=True)
                appendedfile = np.append(matfile['complexSignal'], complexSignal)
                spio.savemat(filename, {'complexSignal':appendedfile})
            
    
