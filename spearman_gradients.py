#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:58:01 2020
@author: Bronte Mckeown
"""
from brainspace.gradient import GradientMaps
import warnings
warnings.simplefilter('ignore')
from brainspace.datasets import load_group_fc, load_parcellation, load_conte69
from brainspace.plotting import plot_hemispheres
from brainspace.utils.parcellation import map_to_labels
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os 
import subprocess 
import pandas as pd

#set number of components
NOcomp = 10

#set kernel
kernel = 'normalized_angle'

#set group variable to path of group gradient nifti
niftipathg = '/groups/labs/semwandering/BrainSpace/TempResults3/10Gradientsnormalized_angleProcrustesaligned.nii.gz'
#load group nifti
group = nib.load(niftipathg)
#get data from group nifti
group = group.get_fdata()
#reshape group nifti to 2D array
group2D = group.reshape((group.shape[0]*group.shape[1]*group.shape[2], group.shape[3]))

#set files variable to directory where individual gradient niftis are stored
files = os.listdir('/groups/labs/semwandering/BrainSpace/TempResults3/parniftis')

#create array of zeros for results below
results = np.zeros((10,10,254))

#create empty list for headers below
header = []

#loop through individual files
for i in range(len(files)):
    header.append(files[i].split('_')[0][:5])
    #set path of individuals nifti
    niftipath = '/groups/labs/semwandering/BrainSpace/TempResults3/parniftis/%s' %(files[i])
    #load individual nifti
    ind = nib.load(niftipath)
    #get data from individual nifti
    ind = ind.get_fdata()
    #reshape individual nifti to 2D array
    ind2D = ind.reshape((ind.shape[0]*ind.shape[1]*ind.shape[2], ind.shape[3]))
    
    #convert to pandas dataframe
    df = pd.DataFrame(data = ind2D)
    dfgroup = pd.DataFrame(data = group2D)
    
    #merge panda dataframes
    merged = pd.concat([df, dfgroup], axis =1)
    
    #correlate merged dataframe using spearman's rank
    allcorr = merged.corr(method = 'spearman')
    
    #index to relevant coefficients 
    corr = allcorr.iloc[0:10,10:20]
    results[:,:,i] = corr

results = results.reshape((100,254))

#z-transform correlations
z_results = np.arctanh(results)
   
header = ','.join(x for x in header)

#save out spearman's correlation coefficients
np.savetxt('/groups/labs/semwandering/BrainSpace/TempResults3/z_spearman.csv', z_results, delimiter=',', header = header)