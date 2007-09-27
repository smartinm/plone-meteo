#!/usr/bin/python
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
"""
Módulo para obtener la predicción meteorológica por localidades ofrecida por
el Instituto Nacional de Meteorologia (www.inm.es), utilizando BeautifulSoup
para parsear el código HTML.

Tenga en cuenta que este módulo está muy ligado al código HTML devuelto por
la página web del Instituto Nacional de Meteorologia y es posible que deje
funcionar ante cualquier cambio en el mismo. Sin embargo, para su tranquilidad
la página no ha cambiado durante años.

Dependencias:
	BeautifulSoup [http://www.crummy.com/software/BeautifulSoup]
"""

__author__ = "Sergio Martín Morillas (smartin@gmv.com)"
__version__ = "0.1.0"
__copyright__ = "Copyright (C) 2007 GMV SGI Team <http://www.gmv-sgi.es>"
__license__ = "GPLv2"

import re
import socket
import urllib2

from BeautifulSoup import BeautifulSoup

SERVER_URL = "http://www.inm.es/cgi-bin/locali.cgi?ig=%s"

########################################################
# Funciones auxiliares
########################################################

def parse_tables(soup_html):
    """Devuelve un array de tablas (arrays de dos dimensiones) con el contenido
       de todas las tablas que encuentre en el html que recibe como parámetro.
       El contenido de las celdas puede ser texto o una etiqueta <img />, si
       aparecen los dos el texto tiene preferencia.
    """
    res = []
    
    for table in soup_html.findAll('table'):
        array = []
        for row in table.findAll('tr', recursive=False):
            tmp = []
            for cell in row.findAll('td', recursive=False):
                plain_text = cell.find(text=True)
                if plain_text:
                    # Si la celda contiene texto tiene preferencia
                    tmp.append(plain_text.strip())
                else:
                    # En otro caso se busca una etiqueta <img>
                    tmp.append(cell.find('img'))
            array.append(tmp)
        res.append(array)

    return res
   
def img_filename(img_tag):
	if img_tag and img_tag.has_key('src'):
		src = img_tag['src']
		res = re.search("^.*/(.*?)$", src)
		if res:
		    return res.group(1)
	return ""

def img_alt(img_tag):
	if img_tag and img_tag.has_key('alt'):
		return img_tag['alt']
	return ""

def format_location(location):
    res = re.search("(.*) - (.*)", location)
    if res:
        return res.groups()
    else:
        return location

def fomat_date(date):
    res = re.search(".*: (.*)", date)
    if res:
        return res.group(1)
    else:
        return date

def fomat_altitude(altitude):
    res = re.search(".* \((.*)\)", altitude)
    if res:
        return res.group(1)
    else:
        return altitude

def parse_forecast(forecast_table):
    forecast = []
    
    for i in range(7):
        forecast.append({
            'fecha'      : None,
            'estado_img' : None,
            'estado_alt' : None,
            'prob_prec'  : None,
            'temp_max'   : None,
            'temp_min'   : None,
            'viento_img' : None,
            'viento_alt' : None,
            'viento_kmh' : None,
            'indice_uv'  : None,
        })
    
    isWindKmh = False
    for row in forecast_table:
    	name = row[0]
    	if isinstance(name, basestring):
        	name = name.lower()
        else:
        	name = ""

        if isWindKmh:
            day = 0
            for i in range(1,7,2):
                forecast[day]['viento_kmh'] = (row[i-1], row[i])
                day += 1
            for i in range(7,11):
                forecast[day]['viento_kmh'] = (row[i-1],)
                day +=1
            isWindKmh = False
            
        elif name.find(u'fecha') != -1:
            for i in range(7):
                forecast[i]['fecha'] = row[i+1]
    
        elif name.find(u'cielo') != -1:
            day = 0
            for i in range(1,7,2):
                forecast[day]['estado_img'] = (img_filename(row[i]),
											   img_filename(row[i+1]))

                forecast[day]['estado_alt'] = (img_alt(row[i]),
											   img_alt(row[i+1]))
                day += 1
            for i in range(7,11):
                forecast[day]['estado_img'] = (img_filename(row[i]),)
                forecast[day]['estado_alt'] = (img_alt(row[i]),)
                day +=1
    
        elif name.find(u'precipitación') != -1:
            for i in range(7):
                forecast[i]['prob_prec'] = row[i+1]
    
        elif name.find(u'máxima') != -1:
            for i in range(7):
                forecast[i]['temp_max'] = row[i+1]
    
        elif name.find(u'mínima') != -1:
            for i in range(7):
                forecast[i]['temp_min'] = row[i+1]
    
        elif name.find(u'viento') != -1:
            day = 0
            for i in range(1,7,2):
                forecast[day]['viento_img'] = (img_filename(row[i]),
											   img_filename(row[i+1]))
                
                forecast[day]['viento_alt'] = (img_alt(row[i]),
											   img_alt(row[i+1]))
                day += 1
            for i in range(7,11):
                forecast[day]['viento_img'] = (img_filename(row[i]),)
                forecast[day]['viento_alt'] = (img_alt(row[i]),)
                day += 1
            isWindKmh = True # La siguiente fila son KMh del viento
    
        elif name.find(u'uv') != -1:
            for i in range(3):
                forecast[i]['indice_uv'] = row[i+1]
    # end for
    return forecast
# end def

########################################################
# Public API
########################################################

def local_weather(location_code, timeout=None):
    url = SERVER_URL % location_code
    
    warn_msg = None
    location = None
    date     = None
    altitude = None
    forecast = None
    
    try:
        if timeout > 0:
            oldtimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)

        try:
            data_stream = urllib2.urlopen(url)
        except urllib2.URLError, e:
            raise IOError, e
        except Exception:
            error_message = "Failed contacting server"
            raise RuntimeError, error_message
    finally:
        if timeout > 0:
            socket.setdefaulttimeout(oldtimeout)
    
    try:
    	# Process HTML with BeautifulSoup
        soup = BeautifulSoup(data_stream,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        
        # Convert parse tree in an array
        tables = parse_tables(soup.find('table'))
        
        # Extract weather data
        warn_msg = tables[0][0][0]
        
        location = format_location(tables[1][0][0])
        date     = fomat_date(tables[1][0][1])
        altitude = fomat_altitude(tables[1][1][0])
        
        forecast = parse_forecast(tables[2])
        
    except:
        error_message = "Failed parsing HTML"
        raise RuntimeError, error_message
       
    # Close data stream
    data_stream.close()
 
    return {
        "notice"   : warn_msg,
        "location" : location,
        "date"     : date,
        "altitude" : altitude,
        "forecast" : forecast
    }
