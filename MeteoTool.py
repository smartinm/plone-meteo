# -*- coding: utf-8 -*-
#
# Meteo
# Copyright (C) 2007 GMV SGI Team <http://www.gmv-sgi.es>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#
# $Id$
#
import time

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager

from Globals import InitializeClass

from OFS.SimpleItem import SimpleItem

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName 
from Products.CMFCore.utils import UniqueObject

from Products.Meteo.config import *

import Meteo

import LocationsTable

class MeteoTool(UniqueObject, SimpleItem):
    """
    """
    id = 'meteo_tool'
    meta_type = 'Meteo Tool'
    plone_tool = 1
    title = 'Meteo Tool'

    security = ClassSecurityInfo()

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container) :
        """
        """
        SimpleItem.manage_afterAdd(self, item, container)

        self.locationCode = ""
        
        self.cacheDuration = 60 * 60 * CACHE_DURATION_IN_HOURS
        
        self.numDaysInPortlet = 3
        
        self.portletType = PORTLET_MULTIPLE
        
        self.languageCode = "es"

        self.cache = {
            "date" : 0,
            "data" : {"error" : "No data"},
        }

    security.declarePublic("getLocationCode")
    def getLocationCode(self):
        """ """
        return self.locationCode

    security.declarePublic("getNumDaysInPortlet")
    def getNumDaysInPortlet(self):
        """ """
        return self.numDaysInPortlet
    
    security.declarePublic("getLocationUrl")
    def getLocationUrl(self):
        """ """
        return Meteo.SERVER_URL % (self.languageCode +'/-m', self.locationCode)

    security.declarePublic("getPortletType")
    def getPortletType(self):
        """ """
        return self.portletType

    security.declarePublic("getNumDaysInPortlet")
    def getMaxIndexForPortlet(self):
        """ """
        data = self.getWeatherData()
        return min(self.numDaysInPortlet, len(data["forecast"]))

    security.declareProtected(permissions.ManagePortal, "searchLocation")
    def searchLocation(self, search):
        """ """
        # XXX: ugly
        results = []
        search = search.lower()
        search = search.replace('Á','a')
        search = search.replace('á','a')
        search = search.replace('É','e')
        search = search.replace('é','e')
        search = search.replace('Í','i')
        search = search.replace('í','i')
        search = search.replace('Ó','o')
        search = search.replace('ó','o')
        search = search.replace('Ú','u')
        search = search.replace('ú','u')
        
        for location in LocationsTable.locations:
            name = location[1].lower()
            if name.find(search) != -1:
                results.append(location)
        
        return results

    security.declareProtected(permissions.ManagePortal, "searchLocationByCode")
    def searchLocationByCode(self, code):
        """ """
        for location in LocationsTable.locations:
            if location[0] == code:
                return location[1]
        
        return ""

    security.declareProtected(permissions.ManagePortal, "manageFormResults")
    def manageFormResults(self, **params) :
        """ """
        purgeCache = False

        if self.locationCode != params["locationCode"]:
            self.locationCode = params["locationCode"]
            purgeCache = True

        if self.numDaysInPortlet != params["numDaysInPortlet"]:
            self.numDaysInPortlet = params["numDaysInPortlet"]

        if self.portletType != params["portletType"]:
            self.portletType = params["portletType"]
            
        if purgeCache:
            self.flushCache()
        
        return "manageFormResults success"
    
    security.declareProtected(permissions.ManagePortal, "flushCache")
    def flushCache(self):
        """ """
        self.cache["date"] = 0
        self.cache = self.cache
        
        return "flushCache success"

    security.declareProtected(permissions.ManagePortal, "renewCache")
    def renewCache(self, timeout=0):
        """ """
        LOGGER.info("renewCache: manual update cache (timeout: %s)", timeout)
        
        result = "renewCache success"
        try:
            data = Meteo.local_weather(self.locationCode,
                                       language=self.languageCode,
                                       timeout=timeout)
            self.cache["data"] = data
            self.cache["date"] = time.time()
            self.cache = self.cache
        except:
            raise
            result = "renewCache failed"
        
        return result

    security.declarePublic("getDayOfWeek")
    def getDayOfWeek(self, date):
        """ """
        dayOfWeek = ""
        
        if date.startswith(u'lun'):
            dayOfWeek = u"Monday"
        elif date.startswith(u'mar'):
            dayOfWeek = u"Tuesday"
        elif date.startswith(u'mié'):
            dayOfWeek = u"Wednesday"
        elif date.startswith(u'jue'):
            dayOfWeek = u"Thursday"
        elif date.startswith(u'vie'):
            dayOfWeek = u"Friday"
        elif date.startswith(u'sáb'):
            dayOfWeek = u"Saturday"
        elif date.startswith(u'dom'):
            dayOfWeek = u"Sunday"

        return dayOfWeek

    security.declarePublic("getSimpleWeatherData")
    def getSimpleWeatherData(self):
        """Return a dictionnary with the following keys:
            location : the location returned by the server, or an error message.
            forecast : a list of forecast which contains for each element
                iconUrl : the url of the icon to display
                iconAlternativeText : the text of the icon
                maxTemperature : the max temperature pretty formated
                minTemperature : the min temperature pretty formated
                dayOfWeek : a little label showing the day of week
            today : a dictonary contains the following elements
                iconUrlAM
                iconUrlPM
                iconAlternativeTextAM
                iconAlternativeTextPM
                maxTemperature
                minTemperature
                dayOfWeek
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
            "iconUrlAM" : "%s/meteo_icons/%s" % (portal_url,
                                                 today["estado_img"][0]),
                                                 
            "iconUrlPM" : "%s/meteo_icons/%s" % (portal_url,
                                                 today["estado_img"][1]),
                                                 
            "iconAlternativeTextAM" : today["estado_alt"][0],
            "iconAlternativeTextPM" : today["estado_alt"][1],
            "maxTemperature" : u"%s&nbsp;°C" % today["temp_max"],
            "minTemperature" : u"%s&nbsp;°C" % today["temp_min"],
            "dayOfWeek": self.getDayOfWeek(today["fecha"])
        }
        
        nowHour = int(time.strftime("%H"))

        for i in range(self.getMaxIndexForPortlet()):
            x = 0 # Por defecto se muestra predicción para antes de medio día

            # Para el día actual, mostramos la predicción de la mañana o de la
            # tarde según a que hora se realiza la petición.
            if i == 0 and nowHour >= 12:
                x = 1
            
            forecast = data["forecast"][i]
            dData = {
                "iconUrl" : "%s/meteo_icons/%s" % (portal_url,
                                                   forecast["estado_img"][x]),
                                                   
                "iconAlternativeText" : forecast["estado_alt"][x],
                "maxTemperature" : u"%s&nbsp;°C" % forecast["temp_max"],
                "minTemperature" : u"%s&nbsp;°C" % forecast["temp_min"],
                "dayOfWeek" : self.getDayOfWeek(forecast["fecha"])
            }
            weather["forecast"].append(dData)

        return weather

    security.declarePublic("getWeatherData")
    def getWeatherData(self):
        """Return the complete dictionnary returned by Meteo.py.
           More details can be found in the docstrings of local_weather()
        """
        now = time.time()
        cacheTime = self.cache["date"]
        
        if cacheTime + self.cacheDuration < now:
            # Caché ha expirado
            LOGGER.info("getWeatherData: cache has expired (cache date: %s)",
                        time.ctime(cacheTime))
            
            try:
                data = Meteo.local_weather(self.locationCode,
                                           language=self.languageCode,
                                           timeout=TIMEOUT_IN_SECONDS)
                self.cache["data"] = data
                self.cache["date"] = now
                self.cache = self.cache
            
            except IOError, e:
                # Si hay un error conectando al servidor se utiliza la cache
                LOGGER.warning("getWeatherData: IOError (%s)", e)
                data = self.cache["data"]
                self.cache["date"] = now
                self.cache = self.cache
                
            except RuntimeError, e:
                return {"error" : e}
        else:
            data = self.cache["data"]
            
        return data

    security.declarePublic("adminLink")
    def adminLink(self):
        """True if admin link have to be displayed
        """
        return getSecurityManager().checkPermission('Manager', self)

InitializeClass(MeteoTool)
