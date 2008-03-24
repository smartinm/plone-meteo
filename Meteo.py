#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Meteo
# Copyright (C) 2008 GMV SGI Team <http://www.gmv-sgi.es>
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
"""

__author__ = "Sergio Martín Morillas (smartin@gmv.com)"
__version__ = "0.2.0"
__copyright__ = "Copyright (C) 2008 GMV SGI Team <http://www.gmv-sgi.es>"
__license__ = "GPLv2"

import re
import socket
import urllib2

from BeautifulSoup import BeautifulSoup, Tag

SERVER_URL = "http://www.aemet.es/%s/eltiempo/prediccion/localidades?l=%s"

########################################################
# Funciones auxiliares
########################################################

"""
<table summary="..." class="tabla_datos" cellspacing="2">
    <thead>
        <tr class="cabecera_niv1">
            <th rowspan="2"><div class="cabecera_celda">Fecha</div></th>
            <th colspan="2">mié 12</th>
            <th colspan="2">jue 13</th>
            <th colspan="2">vie 14</th>
            
            <th rowspan="2">sáb 15</th>
            <th rowspan="2">dom 16</th>
            <th rowspan="2">lun 17</th>
            <th rowspan="2">mar 18</th>
        </tr>

        <tr class="cabecera_niv2">
            <th colspan="2">pm</th>
            <th>am</th>
            <th>pm</th>
            <th>am</th>
            <th>pm</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <th class="borde_rlb_th">Estado del cielo</th>
            <td class="borde_rb" colspan="2"><img src="/imagenes/gif/estado_cielo/15.gif" title="Muy nuboso" alt="Muy nuboso"></td>
            <td class="borde_b"><img src="/imagenes/gif/estado_cielo/15.gif" title="Muy nuboso" alt="Muy nuboso"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/15.gif" title="Muy nuboso" alt="Muy nuboso"></td>
            <td class="borde_b"><img src="/imagenes/gif/estado_cielo/15.gif" title="Muy nuboso" alt="Muy nuboso"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/15.gif" title="Muy nuboso" alt="Muy nuboso"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/13.gif" title="Intervalos nubosos" alt="Intervalos nubosos"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/14.gif" title="Nuboso" alt="Nuboso"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/14.gif" title="Nuboso" alt="Nuboso"></td>
            <td class="borde_rb"><img src="/imagenes/gif/estado_cielo/13.gif" title="Intervalos nubosos" alt="Intervalos nubosos"></td>
        </tr>

        <tr>
            <th class="borde_rlb_th">Prob. precip.(%)</th>
            <td class="borde_rb" colspan="2">0&nbsp;</td>
            <td class="borde_rb" colspan="2">0&nbsp;</td>
            <td class="borde_rb" colspan="2">0&nbsp;</td>
            <td class="borde_rb">15&nbsp;</td>
            <td class="borde_rb">5&nbsp;</td>
            <td class="borde_rb">15&nbsp;</td>
            <td class="borde_rb">25&nbsp;</td>
        </tr>

        <tr>
            <th class="borde_rlb_th">T. Máxima (ºC)</th>
            <td colspan="2" class="borde_rb"><font class="texto_rojo">22&nbsp;</font></td>
            <td colspan="2" class="borde_rb"><font class="texto_rojo">23&nbsp;</font></td>
            <td colspan="2" class="borde_rb"><font class="texto_rojo">23&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_rojo">21&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_rojo">20&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_rojo">19&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_rojo">18&nbsp;</font></td>
        </tr>

        <tr>
            <th class="borde_rlb_th">T. Mínima (ºC)</th>
            <td colspan="2" class="borde_rb"><font class="texto_azul">10&nbsp;</font></td>
            <td colspan="2" class="borde_rb"><font class="texto_azul">11&nbsp;</font></td>
            <td colspan="2" class="borde_rb"><font class="texto_azul">12&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_azul">11&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_azul">9&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_azul">9&nbsp;</font></td>
            <td class="borde_rb"><font class="texto_azul">8&nbsp;</font></td>
        </tr>

        <tr>
            <th class="borde_rlb_th">Viento</th>
            <td colspan="2" class="borde_rb"><img src="/imagenes/gif/iconos_viento/N.gif" title="Norte" alt="Norte"></td>
            <td class="borde_b"><img src="/imagenes/gif/iconos_viento/N.gif" title="Norte" alt="Norte"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/O.gif" title="Oeste" alt="Oeste"></td>
            <td class="borde_b"><img src="/imagenes/gif/iconos_viento/SE.gif" title="Sudeste" alt="Sudeste"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/SE.gif" title="Sudeste" alt="Sudeste"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/NO.gif" title="Noroeste" alt="Noroeste"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/N.gif" title="Norte" alt="Norte"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/NO.gif" title="Noroeste" alt="Noroeste"></td>
            <td class="borde_rb"><img src="/imagenes/gif/iconos_viento/N.gif" title="Norte" alt="Norte"></td>
        </tr>

        <tr>
            <th class="borde_rlb_th">(km/h)</th>
            <td colspan="2" class="borde_rb">18&nbsp;</td>
            <td class="borde_b">14&nbsp;</td>
            <td class="borde_rb">14&nbsp;</td>
            <td class="borde_b">14&nbsp;</td>
            <td class="borde_rb">14&nbsp;</td>
            <td class="borde_rb">14&nbsp;</td>
            <td class="borde_rb">11&nbsp;</td>
            <td class="borde_rb">14&nbsp;</td>
            <td class="borde_rb">29&nbsp;</td>
        </tr>

        <tr>
            <th class="borde_rlb_th">Indice UV Máximo</th>
            <td colspan="2" class="borde_rb"><span class="raduv_pred_nivel2" title="índice ultravioleta moderado">&nbsp;&nbsp;4</span></td>
            <td colspan="2" class="borde_rb"><span class="raduv_pred_nivel2" title="índice ultravioleta moderado">&nbsp;&nbsp;4</span></td>
            <td colspan="2" class="borde_rb"><span class="raduv_pred_nivel2" title="índice ultravioleta moderado">&nbsp;&nbsp;5</span></td>
            <td class="borde_rb">&nbsp;</td>
            <td class="borde_rb">&nbsp;</td>
            <td class="borde_rb">&nbsp;</td>
            <td class="borde_rb">&nbsp;</td>
        </tr>
    </tbody>
</table>
"""

########################################################
# Parsers
########################################################

def parse_table_head(thead):
    """Obtiene un array de fechas a partir de la cabecera de la tabla.
    """
    dates_array = []
    row = thead.find('tr', 'cabecera_niv1')
    for cell in row.findAll('th')[1:]:
        dates_array.append(elem2str(cell))
    return dates_array
    
def parse_table_body(tbody):
    """Obtiene un array de celdas con el cuerpo de la tabla.
    """
    table_array = []
    for row in tbody.findAll('tr', recursive=False):
        row_array = []
        row_array.append(elem2str(row.find('th')))

        for cell in row.findAll('td', recursive=False):
            contents = cell.contents[0]
            row_array.append(contents)
            if cell.has_key('colspan'):
                row_array.append(contents)
        
        table_array.append(row_array)
    
    return table_array

########################################################
# Decoders
########################################################

def decode_forecast(dates, data):
    forecast = []
    
    for i in range(7):
        forecast.append({
            'fecha'      : dates[i],
            'estado_img' : (),
            'estado_alt' : (),
            'prob_prec'  : -1,
            'temp_max'   : -1,
            'temp_min'   : -1,
            'viento_img' : (),
            'viento_alt' : (),
            'viento_kmh' : (),
            'indice_uv'  : -1,
        })
    
    for row in data:
        name = row[0].lower()
        day = 0
        
        if name.find(u'cielo') != -1:
            for i in range(1,7,2):
                forecast[day]['estado_img'] = (decode_image_src(row[i]),
                                               decode_image_src(row[i+1]))
                forecast[day]['estado_alt'] = (decode_image_alt(row[i]),
                                               decode_image_alt(row[i+1]))
                day += 1
            for i in range(7,11):
                forecast[day]['estado_img'] = (decode_image_src(row[i]),)
                forecast[day]['estado_alt'] = (decode_image_alt(row[i]),)
                day += 1

        elif name.find(u'precip') != -1:
            for i in (1,3,5,7,8,9,10):
                forecast[day]['prob_prec'] = elem2str(row[i])
                day += 1
    
        elif name.find(u'máxima') != -1:
            for i in (1,3,5,7,8,9,10):
                forecast[day]['temp_max'] = elem2str(row[i])
                day += 1
    
        elif name.find(u'mínima') != -1:
            for i in (1,3,5,7,8,9,10):
                forecast[day]['temp_min'] = elem2str(row[i])
                day += 1
    
        elif name.find(u'viento') != -1:
            for i in range(1,7,2):
                forecast[day]['viento_img'] = (decode_image_src(row[i]),
                                               decode_image_src(row[i+1]))
                forecast[day]['viento_alt'] = (decode_image_alt(row[i]),
                                               decode_image_alt(row[i+1]))
                day += 1
            for i in range(7,11):
                forecast[day]['viento_img'] = (decode_image_src(row[i]),)
                forecast[day]['viento_alt'] = (decode_image_alt(row[i]),)
                day += 1

        elif name.find(u'km/h') != -1:
            for i in range(1,7,2):
                forecast[day]['viento_kmh'] = (elem2str(row[i]),
                                               elem2str(row[i+1]))
                day += 1
            for i in range(7,11):
                forecast[day]['viento_kmh'] = (elem2str(row[i]),)
                day +=1
    
        elif name.find(u'uv') != -1:
            for i in (1,3,5,7,8,9,10):
                forecast[day]['indice_uv'] = elem2str(row[i])
                day += 1
                
    return forecast


########################################################
# xxx
########################################################

def elem2str(elem):
    if isinstance(elem, Tag):
        contents = elem.find(text=True).string
    else:
        contents = str(elem)
    return re.sub('[\s\xc2\xa0]+', ' ', contents).strip()


########################################################
# Decoders
########################################################

def decode_image_src(img):
	if img and img.has_key('src'):
		src = img['src']
		res = re.search("^.*/(.*?)$", src)
		if res:
		    return res.group(1)
	return ""

def decode_image_alt(img):
	if img and img.has_key('alt'):
		return img['alt']
	return ""

def decode_location(title):
    location = elem2str(title)
    res = re.search(".*\. (.*) (.*)", location)
    if res:
        location = res.groups()
        res = re.search("(.*), (.*)", location[0])
        if res:
            groups = res.groups()
            return ("%s %s" % (groups[1], groups[0]), location[1])
        else:
            return location
    else:
        return location


########################################################
# 
########################################################

def connect_to_server(location_code, language, timeout):
    """Devuelve un stream que es necesario cerrarlo después de usarlo
    """
    url = SERVER_URL % (language, location_code)

    data_stream = None
    
    try:
        if timeout > 0:
            oldtimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)

        try:
            data_stream = urllib2.urlopen(url)
        except urllib2.URLError, e:
            raise IOError, e
        except Exception:
            error_message = "Failed contacting server."
            raise RuntimeError, error_message
    finally:
        if timeout > 0:
            socket.setdefaulttimeout(oldtimeout)
            
    return data_stream

    
########################################################
# Public API
########################################################

def local_weather(location_code, language='es', path_src='meteo_icons/', timeout=0):
    """Devuelve un dict con la predicción de la web AEMET
    """
    # Connecto to server
    data_stream = connect_to_server(location_code, language, timeout)

    # Process HTML with BeautifulSoup
    soup = BeautifulSoup(data_stream,
                         convertEntities=BeautifulSoup.HTML_ENTITIES)

    # Close data stream
    data_stream.close()

    location = ("", "")    # Localidad, Provincia
    capital  = ""          # Localidad (altitud)
    date     = ""          # Fecha de elaboración
    forecast = []          # Predicción
    forecast_html = ""

    try:
        # Extract location
        title = soup.find('h2', 'titulo')
        if title is not None:
            location = decode_location(title)
        
        # Extract capital, date and HTML
        notes = soup.find('div', 'notas_tabla')
        if notes is not None:
            spans = notes.findAll('span')
            if len(spans) == 2:
                capital = elem2str(spans[0].nextSibling)
                date    = elem2str(spans[1].nextSibling)
    
            # HTML
            forecast_html = notes.parent
            forecast_html['class'] = 'meteoDetails'
    
            for img in forecast_html.findAll('img'):
                img['src'] = path_src + decode_image_src(img)

        # Extract forecast
        table = soup.find('table', 'tabla_datos')

        thead = table.thead
        dates = parse_table_head(thead)
        
        tbody = table.tbody
        data  = parse_table_body(tbody)
        
        forecast = decode_forecast(dates, data)
    
    except:
        error_message = "Failed parsing HTML."
        raise RuntimeError, error_message
 
    return {
        "location" : location,
        "capital"  : capital,
        "date"     : date,
        "forecast" : forecast,
        "html"     : forecast_html,
    }
