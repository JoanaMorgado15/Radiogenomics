#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:43:33 2021

@author: joanamorgado
"""
import numpy as np
import matplotlib.pyplot as plt
from radiomics import featureextractor  # This module is used for interaction with pyradiomics
import SimpleITK as sitk
import pandas as pd
import six

Ct = np.load('/Users/joanamorgado/Documents/Radiogenomics/Masks/R01-003.npy')


lung_mask = np.load('/Users/joanamorgado/Documents/Radiogenomics/Masks/R01-146.npy')
nod_mask = np.load('/Users/joanamorgado/Documents/Radiogenomics/Nodule_Masks/R01-146.npy')

def get_biggest_nodule(nod_mask):
    nod_areas = [len(np.column_stack(np.where(nod_mask[j, :, :] == 1))) for j in range(nod_mask.shape[0])]
    idx = nod_areas.index(max(nod_areas))
    return idx

# buscar a slice com maior secçao do nodulo
idx = get_biggest_nodule(nod_mask)
biggest_nod_slice = nod_mask[idx, :, :]

# coordenadas da boundig box do nodulo
coords = np.column_stack(np.where(biggest_nod_slice == 1)) 
x_min, x_max, y_min, y_max = min(coords[:,0]), max(coords[:,0]), min(coords[:,1]), max(coords[:,1])

y_centre = (y_min + y_max)/2
side = 'right' if y_centre > lung_mask[idx, :, :].shape[0]//2 else 'left'

one_lung_mask = []
for i in range(lung_mask.shape[0]):
    copy_slice = np.copy(lung_mask[i, :, :])
    if side == 'right':
        for x in range(lung_mask[i, :, :].shape[0]):
            for y in range(lung_mask[i, :, :].shape[1]):
                if y < lung_mask[i, :, :].shape[0]//2:
                    copy_slice[x,y] = 0

    elif side == 'left':
        for x in range(lung_mask[i, :, :].shape[0]):
            for y in range(lung_mask[i, :, :].shape[1]):
                if y >= lung_mask[i, :, :].shape[0]//2:
                    copy_slice[x,y] = 0
    
    one_lung_mask.append(copy_slice)
one_lung_mask = np.asarray(one_lung_mask)


# mostrar exemplo na slice identificada como a que tem a maior secçao do nodulo

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(10, 5), sharex=True, sharey=True)                                              
ax1.imshow(lung_mask[idx, :, :], cmap = 'gray')
ax1.set_title('original slice')
ax1.axis('off')
ax2.imshow(nod_mask[idx, :, :], cmap = 'gray')
ax2.set_title('biggest nodule mask')
ax2.axis('off')
ax3.imshow(one_lung_mask[idx, :, :], cmap = 'gray')
ax3.set_title('lung with nodule')
ax3.axis('off')
plt.show()



np.save('LungNod_R01-146.npy',one_lung_mask)

imageArray=np.load('/Users/joanamorgado/Documents/Radiogenomics/CTs/R01-146.npy')


image = sitk.GetImageFromArray(imageArray)

mask = sitk.GetImageFromArray(one_lung_mask)

params = {}

extractor = featureextractor.RadiomicsFeatureExtractor(**params)

print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor.enabledImagetypes)
print('Enabled features:\n\t', extractor.enabledFeatures)


result = extractor.execute(image, mask)

for key, val in six.iteritems(result):
  print("\t%s: %s" %(key, val))

print('Result type:', type(result))  # result is returned in a Python ordered dictionary)
print('')
print('Calculated features')
for key, value in six.iteritems(result):
   print('\t', key, ':', value)

df = pd.DataFrame(list(result.items()))
df_transposed = df.T
df_transposed.to_excel ("/Users/joanamorgado/Documents/Radiogenomics/output146.xlsx", index = False, header=True)

