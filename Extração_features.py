#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 19:48:45 2021

@author: joanamorgado
"""
import numpy as np
from radiomics import featureextractor  # This module is used for interaction with pyradiomics
import SimpleITK as sitk
import pandas as pd
import six



lung_mask = np.load('/Users/joanamorgado/Desktop/Lung_nodule_mask/LungNod_R01-146.npy')

ct = np.load('/Users/joanamorgado/Desktop/CTs/R01-146.npy')



image = sitk.GetImageFromArray(ct)

mask = sitk.GetImageFromArray(lung_mask)


params = {}
params['sigma'] = [1, 2, 3, 4, 5]
extractor = featureextractor.RadiomicsFeatureExtractor(**params)
extractor.enableImageTypeByName('LoG')
extractor.enableImageTypeByName('Wavelet')
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
df_transposed.to_excel ('/Users/joanamorgado/Desktop/output146.xlsx', index = False, header=True)

