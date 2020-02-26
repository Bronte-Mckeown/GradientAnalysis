#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:46:29 2020

@author: Bronte Mckeown
"""
import os
import shutil as sh 
import numpy as np
import pandas as pd

#create sorted list of participant numbers
parlist = sorted(os.listdir('/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis'))

#create list of 10 numbers, remove 1 from list
#this list used to remove all but gradient two nifti files below
Clist = list(range(10))
Clist.remove(1)

#for every participant in participant list
for i in range(len(parlist)):
    #copy 10 gradient nifti file to appropriate participant directory
    sh.copy('/groups/labs/semwandering/BrainSpace/TempResults3/parniftis/%saligned_10comp.nii.gz' %parlist[i], '/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis/%s' %parlist[i])
    #change directory to participant directory
    os.chdir('/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis/%s' %parlist[i])
    #fsl split the 10 gradient nifti file into 10 niftis, one per gradient
    os.system('fslsplit /groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis/%s/%saligned_10comp.nii.gz' %(parlist[i], parlist[i]))
    #for each participant, remove all but gradient two niftis
    for k in Clist:
        os.remove('/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis/%s/vol%04d.nii.gz' %(parlist[i], k)) 
    #for each participant, remove 10 gradient nifti file
    os.remove('/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis/%s/%saligned_10comp.nii.gz' %(parlist[i], parlist[i]))

#read in low and high participant numbers for gradient two similarity scores
with open('/groups/labs/semwandering/BrainSpace/TempResults3/low.csv') as b:
    bottom = b.readlines()
    bottom = [x.strip() for x in bottom]

b.close()

with open('/groups/labs/semwandering/BrainSpace/TempResults3/high.csv') as t:
    top = t.readlines()
    top = [x.strip() for x in top]

t.close()

#set prefix and suffix of pathname for each of the gradient two nifti images to merge them
prepath = '/groups/labs/semwandering/BrainSpace/TempResults3/grad2niftis'
postpath = 'vol0001.nii.gz'

#merge all low gradient 2 niftis and merge all high gradient 2 niftis
os.system('fslmerge -t /groups/labs/semwandering/BrainSpace/TempResults3/grad2/low.nii.gz %s' %(' '.join('%s/%s/%s' %(prepath,x,postpath) for x in bottom)))
os.system('fslmerge -t /groups/labs/semwandering/BrainSpace/TempResults3/grad2/top.nii.gz %s' %(' '.join('%s/%s/%s' %(prepath,x,postpath) for x in top)))

#average low and high merged gradient 2 volumes
#output averaged low and high to directory
os.system('fslmaths /groups/labs/semwandering/BrainSpace/TempResults3/grad2/low.nii.gz -Tmean /groups/labs/semwandering/BrainSpace/TempResults3/grad2/low_mean.nii.gz')
os.system('fslmaths /groups/labs/semwandering/BrainSpace/TempResults3/grad2/top.nii.gz -Tmean /groups/labs/semwandering/BrainSpace/TempResults3/grad2/top_mean.nii.gz')

#use fslmaths fslsub to subtract the difference between the averaged niftis
#outputs nifti image of the difference between low and high similarity individuals for gradient 2
os.system('fslmaths /groups/labs/semwandering/BrainSpace/TempResults3/grad2/top_mean.nii.gz -sub /groups/labs/semwandering/BrainSpace/TempResults3/grad2/low_mean.nii.gz /groups/labs/semwandering/BrainSpace/TempResults3/grad2/delta2_mean.nii.gz')




