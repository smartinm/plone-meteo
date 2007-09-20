# -*- coding: utf-8 -*-
import time
import re
import os
import urllib2

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName 
from Products.CMFCore.utils import UniqueObject

from Products.Meteo.config import *

import Meteo
import LocationsTable


# security.declareProtected(Permission, methodNameAsString)
# security.declarePrivate(methodNameAsString)
# security.declarePublic(methodNameAsString)
# default manager permission is CMFCorePermissions.ManagePortal

# Create a Custom Tool
# http://plone.org/documentation/how-to/create-a-tool/

class MeteoTool(UniqueObject, SimpleItem):
    """
        Enable Plone to ask a weather forecast server.
    """
    id = 'meteo_tool'
    meta_type = 'Meteo Tool'
    plone_tool = 1
    title = 'Meteo Tool'

    security = ClassSecurityInfo()

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container) :
        """
            Create default structures
        """
        SimpleItem.manage_afterAdd(self, item, container)

        self.locationCode = ""
        
        # update every two hours
        self.cacheDuration = 60 * 60 * 2
        
        self.numDaysInPortlet = 3
        
        self.portletType = PORTLET_MULTIPLE

        self.cache = {
            "date" : 0,
        }

    security.declarePublic("getLocationCode")
    def getLocationCode(self):
        """
        """
        return self.locationCode

    security.declarePublic("getNumDaysInPortlet")
    def getNumDaysInPortlet(self):
        """
        """
        return self.numDaysInPortlet
    
    security.declarePublic("getLocationUrl")
    def getLocationUrl(self):
        """
        """
        return Meteo.SERVER_URL % self.locationCode

    security.declarePublic("getPortletType")
    def getPortletType(self):
        """
        """
        return self.portletType

    security.declarePublic("getNumDaysInPortlet")
    def getMaxIndexForPortlet(self):
        """
        """
        data = self.getWeatherData()
        return min(self.numDaysInPortlet,
                   len(data["forecast"]))

    security.declareProtected(CMFCorePermissions.ManagePortal, "searchLocation")
    def searchLocation(self, search):
        """
        """
        results = []
        search = search.lower()
        
        for location in LocationsTable.locations:
            name = location[1].lower()
            if name.find(search) != -1:
                results.append(location)
        
        return results

    security.declareProtected(CMFCorePermissions.ManagePortal, "searchLocationByCode")
    def searchLocationByCode(self, code):
        """
        """
        for location in LocationsTable.locations:
            if location[0] == code:
                return location[1]
        
        return ""

    security.declareProtected(CMFCorePermissions.ManagePortal, "manageFormResults")
    def manageFormResults(self, **params) :
        """
            Update the conf values
        """
        purgeCache = False

        if self.locationCode != params["locationCode"]:
            self.locationCode = params["locationCode"]
            purgeCache = True

        if self.numDaysInPortlet != params["numDaysInPortlet"]:
            self.numDaysInPortlet = params["numDaysInPortlet"]

        if self.portletType != params["portletType"]:
            self.portletType = params["portletType"]
            
        if purgeCache and hasattr(self, "cache"):
            self.cache["date"] = 0
            self.cache = self.cache

        return ("pwf_config_ok", "success")
    
    security.declareProtected(CMFCorePermissions.ManagePortal, "flushCache")
    def flushCache(self):
        """
            handy method to flush cache
        """
        self.cache["date"] = 0
        self.cache = self.cache
        return "Caché reiniciado."

    security.declarePublic("getDayOfWeek")
    def getDayOfWeek(self, date):
        """
        """
        dayOfWeek = ""
        
        if date.startswith(u'Lun'):
            dayOfWeek = u"Lunes"
        elif date.startswith(u'Mar'):
            dayOfWeek = u"Martes"
        elif date.startswith(u'Mié'):
            dayOfWeek = u"Miércoles"
        elif date.startswith(u'Jue'):
            dayOfWeek = u"Jueves"
        elif date.startswith(u'Vie'):
            dayOfWeek = u"Viernes"
        elif date.startswith(u'Sáb'):
            dayOfWeek = u"Sabado"
        elif date.startswith(u'Dom'):
            dayOfWeek = u"Domingo"

        return dayOfWeek

    security.declarePublic("getSimpleWeatherData")
    def getSimpleWeatherData(self):
        """
            Return a dictionnary with the following keys :
            location : the location returned by the server, or an error message.
            forecast : a list of forecast which contains for each element
                iconUrl : the url of the icon to display
                iconAlternativeText : the text of the icon
                maxTemperature : the max temperature pretty formated
                minTemperature : the min temperature pretty formated
                dayOfWeek : a little label showing the day of week
        """
        data = self.getWeatherData()

        if "error" in data.keys():
            return data

        weather = {
            "location" : data["location"][0],
            "today"    : {},
            "forecast" : [],
        }
        
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal_url = portal.absolute_url()

        today = data["forecast"][0]
        weather["today"] = {
            "iconUrlAM" : "%s/meteo_icons/%s" % (portal_url, today["estado_img"][0]),
            "iconUrlPM" : "%s/meteo_icons/%s" % (portal_url, today["estado_img"][1]),
            "iconAlternativeTextAM" : today["estado_alt"][0],
            "iconAlternativeTextPM" : today["estado_alt"][1],
            "maxTemperature" : u"%s&nbsp;°C" % today["temp_max"],
            "minTemperature" : u"%s&nbsp;°C" % today["temp_min"],
            "dayOfWeek": self.getDayOfWeek(today["fecha"])
        }
        
        nowHour = int(time.strftime("%H"))

        for i in range(self.getMaxIndexForPortlet()):
            # Comprobamos si la petición se realizar por la mañana o
            # por la tarde para el primer día (hoy)

            x = 0 # Por defecto se muestra predicción para antes de medio día
           
            if i == 0 and nowHour >= 12:
                x = 1
            
            forecast = data["forecast"][i]
            dData = {
                "iconUrl" : "%s/meteo_icons/%s" % (portal_url, forecast["estado_img"][x]),
                "iconAlternativeText" : forecast["estado_alt"][x],
                "maxTemperature" : u"%s&nbsp;°C" % forecast["temp_max"],
                "minTemperature" : u"%s&nbsp;°C" % forecast["temp_min"],
                "dayOfWeek" : self.getDayOfWeek(forecast["fecha"])
            }
            weather["forecast"].append(dData)

        return weather

    security.declarePublic("getWeatherData")
    def getWeatherData(self):
        """
            Return the complete dictionnary returned by Meteo.py.
            More details can be found in the docstrings of local_weather()

            Run Meteo.py if you want a sample dictionnary.
        """

        if self.cache["date"] + self.cacheDuration < time.time():
            ## cache has expired
            try:
                data = Meteo.local_weather(self.locationCode)
                self.cache["data"] = data
                self.cache["date"] = time.time()
                self.cache = self.cache

            except RuntimeError, e:
                return {
                    "error" : e,
                }
        else:
            data = self.cache["data"]
        return data

    
    security.declarePublic("adminLink")
    def adminLink(self):
        """
            True if admin link have to be displayed
        """
        return getSecurityManager().checkPermission('Manager', self)

InitializeClass(MeteoTool)
