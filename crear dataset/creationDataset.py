# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:11:30 2022

@author: Mishell
"""

# LIBRERÍAS A UTILIZAR
import pandas as pd
# Clase website creado
import feature_extraction_DeAd

#IMPORTAMOS LOS DATOS
datasetUrl = pd.read_csv('/Users/denniscaisa/Desktop/DENNIS/TITULACION/Codigo DA/ids-phishing-main/crear dataset/ok-part1 copy.csv')

dataframeUrl = pd.DataFrame(data = datasetUrl)

websiteList = []
listDoubt = []
##Website legítimos y con phishing
n = len(dataframeUrl)

for i in range(n - 1):
    label = 0
    print('*** Url {}'.format(dataframeUrl.iloc[i]['url']))
    if dataframeUrl.iloc[i]['result'] == 0:
        label = 1
    else:
        label = -1a