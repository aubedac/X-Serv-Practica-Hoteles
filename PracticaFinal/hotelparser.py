#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.saxutils import escape, unescape
import urllib2
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.data = {'name': '', 'body': '','web': '', 'address': '', 'latitude': '', 'longitude': '', 'images': [], 'category' : []}
        self.dataType = ['basicData', 'geoData', 'multimedia','extradata'] #modified ['basicData', 'geoData', 'multimedia', 'extradata']
        self.imageList = []
        self.starList = []
        self.flagImage = False
        self.flagItem = False
        self.flagEmptyImg = False
        self.listType = [False] * len(self.dataType)
        self.dataSection = ['name', 'web', 'body', 'address', 'latitude', 'longitude', 'url', 'item']
        self.listSection = [False] * len(self.dataSection)
        self.inSection = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name in self.dataType:
            self.flagEmptyImg = True
            self.listType[self.dataType.index(name)] = True
        elif self.listType:
            self.flagEmptyImg = False
            if name in self.dataSection:
                self.listSection[self.dataSection.index(name)] = True

    def endElement (self, name):
        if name in self.dataType:
            if self.listType[2] and self.flagEmptyImg:
                self.data['images'].append(self.imageList)
                self.flagEmptyImg = False
            self.listType[self.dataType.index(name)] = False
        elif self.listSection:
            contador = 0
            for i,j in enumerate(self.listSection):
                if j:
                    contador = i
                    break

            if name == self.dataSection[contador]:
                if name == "url":
                    self.imageList.append(self.theContent)
                    self.flagImage = True
                if name == "item":
                    self.starList.append(self.theContent)
                    self.flagItem = True
                else:
                    try:
                        self.data[name] += self.theContent + '|'
                    except KeyError:
                        pass
                    if self.flagImage:
                        if len(self.imageList) != 0 and name != 'url':
                            self.data['images'].append(self.imageList)
                            self.imageList = []
                            self.flagList = False
                    if self.flagItem:
                        #print self.starList
                        self.starList = [self.starList[3],self.starList[5]]
                        #self.starList = [self.starList[0],self.starList[1]]
                        self.data['category'].append(self.starList)
                        self.starList = []
                        self.flagItem = False
            self.theContent = ""
            try:
                self.listSection[self.dataSection.index(name)] = False
            except ValueError:
                pass

    def characters (self, chars):
        html_escape_table = {
            "&quot;" : '"',
            "&apos;" : "'",
            "&iexcl" : u'¡',
            "&iquest" : u'¿',
            "&aacute;" : u'á',
            "&iacute;" : u'í',
            "&oacute;" : u'ó',
            "&uacute;" : u'ú',
            "&eacute;" : u'é',
            "&ntilde;" : u'ñ',
            "&Ntilde;" : u'Ñ',
            "&Aacute;" : u'Á',
            "&Iacute;" : u'Í',
            "&Oacute;" : u'Ó',
            "&Uacute;" : u'Ú',
            "&Eacute;" : u'É',
            "&Ocirc;" : u'Ô',
            "&ocirc;" : u"ô",
            "&uuml;" : u'ü',
            "&Uuml;" : u'Ü',
            "&nbsp;" : '\n',
            "&rdquo;" : '"',
            "&ldquo;" : '"',
            "&lsquo;" : "'",
            "&rsquo;" : "'",
        }
        if self.listSection:
         text = self.theContent + chars
         self.theContent = unescape(text, html_escape_table)

# --- Main prog
def getHotels(flagEsp, flagFr, flagEn):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    if flagEn:
        theParser.parse('http://cursosweb.github.io/etc/alojamientos_en.xml')
    elif flagFr:
        theParser.parse('http://cursosweb.github.io/etc/alojamientos_fr.xml')
    elif flagEsp:
        theParser.parse('http://cursosweb.github.io/etc/alojamientos_es.xml')
    theHandler.data["category"].append([theHandler.starList[3], theHandler.starList[5]])
    theHandler.data['images'].append([theHandler.imageList])
#print theHandler.data['body']
    return theHandler.data
