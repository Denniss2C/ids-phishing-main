# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 08:56:20 2022

@author: Mishell
"""# -*- coding: utf-8 -*-

# LIBRERÍAS A UTILIZAR
import pandas as pd
# Clase website creado
import requests as rq
import re

#IMPORTAMOS LOS DATOS
datasetUrl = pd.read_csv('datasetPhishing.csv')

dataframeUrl = pd.DataFrame(data = datasetUrl)

websiteList = []
"Agregar http a las url que no tiene https al inicio de la url"
def addHttp(url):
    if not re.match(r"^https?", url) or not re.match(r"^http?", url):
        url = "http://" + url
    return url
"Obtener el response"
def getResponse(url): 
    try:
        url = addHttp(url)
        response = rq.get(url, timeout=5.0)
        print('respose {}'.format(response.status_code))
        if response.status_code == 200:
            return 0
        else:
            return -999
        print(response)
    except Exception as e:
        print(str(e))
        return -999
##Website legítimos y con phishing
#O puedes cambiarle por el número de características que te toca
n = len(dataframeUrl)
##https://www.express.co.uk/entertainment/gaming/615072/South-by-Southwest-gaming-event-cancelled-GamerGate

for i in range(n):
    label = 0
    print('*** Url {}'.format(dataframeUrl.iloc[i]['url']))
    if dataframeUrl.iloc[i]['result'] == 0:
        label = 1
    else:
        label = -1
    aux = getResponse(dataframeUrl.iloc[i]['url'])
    if aux == 0:
        websiteList.append(dataframeUrl.iloc[i])
   ## print(len(aux.features))

    
dtFinish = pd.DataFrame(websiteList)
#print(dtFinish)
dtFinish.to_csv('datasetPhishingPreprocesado.csv', index=False)

#Ver los primeros
##print(dataframeUrl) 

