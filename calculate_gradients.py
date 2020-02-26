# -*- coding: utf-8 -*-

"""
Created on Fri Dec 13 10:29:44 2019
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

#set number of components
NOcomp = 10

#set kernel
kernel = 'normalized_angle'

#set interactive plotting
plt.ion()

#set files variable to directory where individual connectivity matrices are stored
files = os.listdir('/groups/labs/semwandering/BrainSpace/TempResults/par2')

#Load 400 Schaefer parcellation
labeling = load_parcellation('schaefer', scale=400, join=True)
#and load the conte69 hemisphere surfaces
surf_lh, surf_rh = load_conte69()
mask = labeling != 0

#load HCP data from BrainSpace and calculate group level gradients
conn_matrix = load_group_fc('schaefer', scale=400)
conn_gradient = GradientMaps(n_components=NOcomp, kernel= kernel)
conn_gradient.fit(conn_matrix)

#load our group matrix and calculate group level gradients
m = np.loadtxt('/groups/labs/semwandering/BrainSpace/TempResults/Schaefer400_meandataforGradients.csv', delimiter=',')
group_gradient = GradientMaps(n_components=NOcomp, kernel= kernel, alignment='procrustes')
#align our group level gradients to the HCP gradients
group = group_gradient.fit([m], reference = conn_gradient.gradients_)

#plot lambdas
plt.title("Scree plot of the scaled eigenvalues of the group-averaged gradients\n")
plt.xlabel("Gradients")
plt.ylabel("Lambdas scaled to a sum of 1")
plt.xticks(np.arange(10), ('1','2','3','4','5','6', '7', '8', '9', '10'))
plt.scatter(range(group.lambdas_[0].size), group.lambdas_[0])

#Get gradient maps in nifti format
niftisave = group_gradient.aligned_[0] 
ics = nib.load('/groups/labs/semwandering/Cohort/masks/Schaefer400/IndividualParcels/Schaefer2018_400Parcels_7Networks_order_FSLMNI152_2mm_400_volumes.nii.gz')
icsdata = ics.get_data()
icsdatars = icsdata.reshape((icsdata.shape[0]*icsdata.shape[1]*icsdata.shape[2], icsdata.shape[3]))
icvox = np.dot(icsdatars, niftisave)
icnidat = icvox.reshape((icsdata.shape[0], icsdata.shape[1], icsdata.shape[2], niftisave.shape[1]))
saveic_header = ics.header
saveic_header['dim'][4] = niftisave.shape[1]
saveimg =  nib.Nifti1Image(icnidat, ics.affine, header=saveic_header)
nib.save(saveimg,'/groups/labs/semwandering/BrainSpace/TempResults3/%sGradients%sProcrustesaligned.nii.gz' %(NOcomp,kernel))

#change directory to where individual connectivity matrices are stored
os.chdir('/groups/labs/semwandering/BrainSpace/TempResults/par2')

#create empty participant list
par= []
#iterate through individual files to calculate individual gradients
for i in range(len(files)):
    
    niftipath = '/groups/labs/semwandering/BrainSpace/TempResults3/parniftis/%saligned_%scomp.nii.gz' %(files[i].split('_')[2].strip('.csv'), NOcomp)
    par.append(files[i].split('_')[2].strip('.csv'))
    
    #Load the correlation matrix for that individual and calculate individual gradients, aligned to group
    ind_matrix = np.loadtxt(files[i],delimiter=',')
    ind_gradient = GradientMaps(n_components=10, kernel= kernel, alignment='procrustes')
    ind_gradient.fit([ind_matrix],reference = group_gradient.aligned_[0])
   
    #save individual niftis
    niftisave = ind_gradient.aligned_[0]
   
    ics = nib.load('/groups/labs/semwandering/Cohort/masks/Schaefer400/IndividualParcels/Schaefer2018_400Parcels_7Networks_order_FSLMNI152_2mm_400_volumes.nii.gz')
    icsdata = ics.get_data()

    icsdatars = icsdata.reshape((icsdata.shape[0]*icsdata.shape[1]*icsdata.shape[2], icsdata.shape[3]))
    icvox = np.dot(icsdatars, niftisave)
    icnidat = icvox.reshape((icsdata.shape[0], icsdata.shape[1], icsdata.shape[2], niftisave.shape[1]))
    #saveic_header = ics.header
    saveic_header['dim'][4] = niftisave.shape[1]
    saveimg =  nib.Nifti1Image(icnidat, ics.affine, header=saveic_header)

    nib.save(saveimg, niftipath)