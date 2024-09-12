#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mussgill
"""

import physeng as pe

import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

class MaterialProperty():
    def __init__(self, name, values):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('MaterialProperty')
        self._logger.debug(f'__init__: {name}')
        #print(f'MaterialProperty: __init__: {name}')

        self.__Name = name
        self.__Tref = 20.0
        self.__Tunit = '°C'
        if 'T' in values.keys() and 'Tunit' in values.keys():
            self.__Tref = float(values['T'])
            self.__Tunit = values['Tunit']
        self.__Value = float(values['Value'])
        self.__Unit = values['Unit']

    def name(self):
        return self.__Name

class Material():
    
    def __init__(self, name, title, category):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('Material')
        self._logger.debug(f'__init__: {name}, {title}')
        
        self.__Name = name
        self.__Title = title
        self.__Category = category
        self.__Groups = []
        self.__Properties = {}
        
        self.__MaterialDB = None
        #self.__MaterialDB = MaterialDB()

    def name(self):
        return self.__Name

    def title(self):
        return self.__Title

    def category(self):
        return self.__Category
    
    def addToGroup(self, group):
        self.__Groups.append(group)
        #print(group)
    
    def addProperty(self, prop):
        self._logger.debug(f'addProperty: {prop.name()}')
        self.__Properties[prop.name()] = prop
        #print(group)

class IsotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'IsotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title} 2')

class OrthotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'OrthotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title} 2')

class MaterialDB(metaclass=pe.Singleton):
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self.__logger = logging.getLogger('MaterialDB')

        self.__logger.debug('__init__')
        
        self.__materials = []
        self.__materialsByName = {}
        self.__materialsByTitle = {}
        self.__groups = {}
        self.__categories = {}
        
        self.__readDB()
  
    def __processFile(self, xmlfile):
        try:
            self.__logger.debug(f'processing {xmlfile}')
            tree = ET.parse(xmlfile)
            root = tree.getroot()
            for child in root:
                self.__logger.debug(f'processing {child.tag}')
                
                name = child.find('Name').text
                title = child.find('Title').text
                category = child.find('Category').text
                
                if child.tag == 'IsotropicMaterial':
                    material = IsotropicMaterial(name, title, category)
                elif child.tag == 'OrthotropicMaterial':
                    material = OrthotropicMaterial(name, title, category)
                else:
                    print(child.tag)
                    continue
                
                groups = child.find('Groups')
                if groups is not None:
                    for group in groups:
                        material.addToGroup(group.text)
                
                props = child.find('Properties')
                if props is not None:
                    for prop in props:
                        prop = MaterialProperty(prop.tag, prop.attrib)
                        material.addProperty(prop)
                
                self.addMaterial(material)
        except:
            print('exception')
            pass
        
    def __readDB(self):
        filenames = ['MaterialDB_elements.xml',
                     'MaterialDB_alloys.xml',
                     'MaterialDB_polymers.xml',
                     'MaterialDB_ceramics.xml',
                     'MaterialDB_compounds.xml',
                     'MaterialDB_composites.xml']
        for filename in filenames:
            self.__logger.debug(f'reading {filename}')
            xmlfile = pkg_resources.files('physeng.data').joinpath(filename)
            self.__processFile(xmlfile)
    
    def addMaterial(self, material):
        self.__materials.append(material)
        self.__materialsByName[material.name()] = material
        self.__materialsByTitle[material.title()] = material
        self.__logger.info(f'addMaterial: {material.name()}, {material.title()}')

#matDB = MaterialDB()
