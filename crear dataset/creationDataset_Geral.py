"""
@authors: Dennis - Adrian

"""

# LIBRERÍAS A UTILIZAR
import pandas as pd
# Clase website creado
import feature_extraction

#IMPORTAMOS LOS DATOS
try:
    datasetUrl = pd.read_csv('/Users/denniscaisa/Desktop/DENNIS/TITULACION/Codigo DA/ids-phishing-main/Geral.csv')
except pd.errors.ParserError as e:
    print(f"Error al leer el archivo CSV: {e}")
    datasetUrl = pd.DataFrame()

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
    aux = feature_extraction.website(dataframeUrl.iloc[i]['url'], label)
    aux.getFeatures()
    if aux.doubt == 0:
        websiteList.append(aux.features)
    else:
        listDoubt.append(dataframeUrl.iloc[i])

dtFinish = pd.DataFrame(websiteList, columns=['haveIp', 'lengthUrl','haveAtSymbol','sslState','domainAge','slashDouble','anchorUrl','prefixSuffix','linksInTags','clicRigth',
                                              'windowsPopUp', 'favicon','abnormalURL','iframe','dnsRegister','googleIndex','port','requestUrl','sfh','websiteForwarding',
                                              'mouseOver','webTraffic', 'shorterService','domainRegisterAge','httpsToken','emailInformation','pageRank','staticalInform','haveSubdomain','linksToPage',
                                              'result'])

dtFinish.to_csv('Dataset_Legitime_Geral.csv', index_label='Ord.')

print('Lista de url que dieron problemas: ')
print(listDoubt)
