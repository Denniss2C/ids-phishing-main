# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 19:15:32 2022

@author: Dennis
"""
import re
import ipaddress
import urllib.parse as urp
import requests as rq
import whois as ws
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup ### Parser utilizado: lxml
from googlesearch import search
import socket

class website:
    """constructor con parámetros"""
    def __init__(self, url, result = None):
        self.url = url
        self.domain = None
        self.response = None
        self.whois = None
        self.soup = None
        self.features = []
        self.result = result
        self.doubt = 0

        
    def printWebsite(self):
        print("La url ingresada es {}".format(self.url))
        
    "Agregar http a las url que no tiene https al inicio de la url"
    def addHttp(self):
        if not re.match(r"^https?", self.url) or not re.match(r"^http?", self.url):
            self.url = "http://" + self.url
        return
        
    "Encontrar el dominio y reemplazo www"
    def findDomain(self):
        self.domain = urp.urlparse(self.url).netloc
        if re.match(r"^www.",self.domain):
            self.domain = self.domain.replace("www.","")
            
    "Obtener el response"
    def getResponse(self): 
        try:
            self.response = rq.get(self.url, timeout=5.0)
            print(self.response)
        except Exception as e:
            return
    "Obtener registro whois"""
    def getWhois(self):
        try:
            self.whois = ws.whois(self.domain)
        except:
            return
    
    "Traer información con BeautifulSoap"
    def getSoup(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "html.parser")
        except :
            return

    """#1. Longitud de la url"""
    def lengthUrl(self):
        if len( self.url) < 54:
            return(1)
        elif len(self.url) < 75:
            return(0)
        else:
            return(-1)
        
    """#2. URL de anclaje"""
    def anchorUrl(self):
        "tag 'a'"
        if self.soup == None:
            return -1
        else:
            i = 0
            countOk = 0
            percentValueOk = 0.0
            for a in self.soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (self.url in a['href'] or self.domain in a['href']): 
                    countOk = countOk+ 1
                i += 1
            try:
                percentValueOk = (countOk * 100) / float(i)
            except:
                return 1
            if percentValueOk < 31.0:
                return 1
            elif percentValueOk < 67.0:
                return 0
            else:
                return -1 
            
    """#3. URL anormal"""
    def abnormalURL(self):
        if self.response == None:
            return -1
        else:
            if self.response.text == self.whois:
                return 1
            else:
                return -1
    
    "#4. Request URL"
    def requestUrl(self):
        'object: img, audio, embed, i_frame'
        if self.soup == None:
            return -1
        else:
            i = 0 
            countOk= 0
            percentValueOk = 0.0
            for img in self.soup.find_all('img', src = True):
                dots = [slash.start() for slash in re.finditer(r'\.', img['src'])                     ]
                if self.domain in img['src'] or self.url in img['src'] or dots == 1: 
                    countOk += 1
                i += 1
            for audio in self.soup.find_all('audio', src = True):
                dots = [slash.start() for slash in re.finditer(r'\.', audio['src']) ] 
                if self.domain in audio['src'] or self.url in audio['src'] or dots == 1: 
                    countOk += 1
                i += 1
            for embed in self.soup.find_all('embed', src = True):
                dots = [slash.start() for slash in re.finditer(r'\.', embed['src']) ] 
                if self.domain in embed['src'] or self.url in embed['src'] or dots == 1: 
                    countOk += 1
                i += 1
            for i_frame in self.soup.find_all('i_frame', src = True):
                dots = [slash.start() for slash in re.finditer(r'\.', i_frame['src']) ] 
                if self.domain in i_frame['src'] or self.url in i_frame['src'] or dots == 1: 
                    countOk += 1
                i += 1
            try:
                percentValueOk = (countOk * 100) / i
            except:
                return 1
            if percentValueOk < 22.0:
                return 1
            elif percentValueOk < 61.0:
                return 0
            else:
                return -1 
    
    """#5. Edad del Dominio"""
    def domainAge(self): 
        if self.whois == None or not self.whois.creation_date :
            return -1
        else:
            try:
                creationDate = self.whois.creation_date[0]
                try:
                    creationDate = self.convertDate(creationDate)
                except:
                    creationDate = self.whois.creation_date[1]
                    creationDate = self.convertDate(creationDate)
            except:
                creationDate = self.whois.creation_date
                try:
                    creationDate = self.convertDate(creationDate)
                except:
                    self.whois.creation_date = None
                    creationDate = None
            try:
                if not creationDate ==  None:
                    if (date.today().year - creationDate.year) < 1:
                        if (date.today().month - creationDate.month) < 6:
                            return -1
                        else:
                            return 1
                    else:
                        return 1
                else:
                    return -1
            except:
                self.doubt = 1
                return
     
    "#6. Tiene un subdomino"
    def haveSubdomain(self):
        if len(re.findall("\.", self.url)) == 1:
            return 1
        elif len(re.findall("\.", self.url)) == 2:
            return 0
        else:
            return -1
        
    "#7. Duración del registro del dominio"
    def domainRegisterAge(self):
        if self.whois == None or not self.whois.expiration_date or not self.whois.creation_date:
            return -1
        else:
            try:
                creationDate = self.whois.creation_date[0]
                if isinstance(creationDate, str):
                    creationDate = self.whois.creation_date[0:19]
                    creationDate = datetime.strptime(creationDate, '%Y-%m-%d %H:%M:%S').date()
            except:
                creationDate = self.whois.creation_date 
            try:
                expirationDate = self.whois.expiration_date[0]
                if isinstance(creationDate, str):
                    expirationDate = self.whois.expiration_date[0:19]
                    expirationDate = datetime.strptime(expirationDate, '%Y-%m-%d %H:%M:%S').date()
            except:
                expirationDate = self.whois.expiration_date 
            try:
                if (expirationDate.year - creationDate.year) <= 1:
                    return -1
                else:
                    return 1
            except:
                self.doubt = 1
                return
        
    "#8. Token HTTPS"
    def httpsToken(self):
        if 'https' in self.domain:
            return (-1)
        else:
            return (1)

    "#9. verificar md5"
    def hasMD5(self):
        md5_pattern = re.compile(r'[a-fA-F\d]{32}')
        if md5_pattern.search(self.url):
            return 1
        else:
            return -1
        
    "#10. verificar SHA1"
    def hasSHA1(self):
        sha1_regex = r"\b[a-fA-F\d]{40}\b"
        match = re.search(sha1_regex, self.url)
        if match:
            return 1
        elif not self.url:
            return -1
        else:
            return 0

    "#11. verificar Yara"   
    def hasYara(self):
        yara_regex = r"\b(rule|import)\s+[a-zA-Z0-9_\.]+(\s*:\s*[a-zA-Z0-9_\.]+)?\s*\{\s*([^\{\}]|\{[^\{\}]*\})*\s*\}"
        match = re.search(yara_regex, self.url)
        if match:
            return 1
        elif not self.url:
            return -1
        else:
            return 0

    "#12. verificar SHA256"
    def hasSHA256(self):
        sha256_regex = r"\b[a-fA-F\d]{64}\b"
        match = re.search(sha256_regex, url)
        if match:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "#13. verificar Short"
    def hasShort(self):
        if "short" in url:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "#14. verificar dataTime"
    def hasDateTime(url):
        datetime_regex = r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
        match = re.search(datetime_regex, url)
        if match:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "#15. verificar Domain"
    def hasDomain(url):
        domain_regex = r"(?<=://)[\w\.-]+"
        match = re.search(domain_regex, url)
        if match:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "#16. verificar hostname"
    def hasHostname(url):
        parsed_url = urlparse(url)
        if parsed_url.netloc:
            hostname_regex = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
            match = re.search(hostname_regex, parsed_url.netloc)
            if match:
                return 1
            else:
                return 0
        elif not url:
            return -1
        else:
            return 0

    "#17. verificar IPDSt"    
    def hasIPDst(url):
        ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        match = re.search(ip_regex, url)
        if match:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "#18. verificar IPDSt"
    def hasIPSrc(url):
        ip_src_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?:/\d{1,2})?\b"
        match = re.search(ip_src_regex, url)
        if match:
            return 1
        elif not url:
            return -1
        else:
            return 0

    "Reunir todas las características"
    def getFeatures(self):
        self.printWebsite()
        self.addHttp()
        self.findDomain()
        self.getResponse()
        self.getWhois()
        self.getSoup()
        self.features.append(self.lengthUrl())
        self.features.append(self.domainAge())
        if self.doubt == 0:
            self.features.append(self.anchorUrl())
            self.features.append(self.abnormalURL())
            self.features.append(self.requestUrl())
            self.features.append(self.domainRegisterAge())
            if self.doubt == 0:
                self.features.append(self.httpsToken())
                self.features.append(self.haveSubdomain())
                self.features.append(self.hasMD5())
                self.features.append(self.hasSHA1())
                self.features.append(self.hasYara())
                self.features.append(self.hasSHA256())
                self.features.append(self.hasDataTime())
                self.features.append(self.hasDomain())
                self.features.append(self.hasHostname())
                self.features.append(self.hasIPDst())
                self.features.append(self.hasIPSrc())
        if not self.result == None:
            self.features.append(self.result)

##try:
##x = website('https://www.srb.org.hk/board.html')
##x.getFeatures()
##print(x.features)
##except:
  ##  print('No es posible')
