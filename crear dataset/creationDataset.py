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
        label = -1
    aux = feature_extraction_DeAd.website(dataframeUrl.iloc[i]['url'], label)
    aux.getFeatures()
    if aux.doubt == 0:
        websiteList.append(aux.features)
    else:
        listDoubt.append(dataframeUrl.iloc[i])

    
dtFinish = pd.DataFrame(websiteList, columns=['lengthUrl','domainAge','anchorUrl','abnormalURL','requestUrl','domainRegisterAge','httpsToken','haveSubdomain','hasMD5','hasSHA1','hasYara','hasSHA256','hasShort','hasDateTime','hasDomain','hasHostname','hasIPDst','hasIPSrc','result'])
#print(dtFinish)
dtFinish.to_csv('dataset-part2.csv', index_label='Ord.')

##
print('Lista de url que dieron problemas: ')
print(listDoubt)

#Ver los primeros
##print(dataframeUrl) 
