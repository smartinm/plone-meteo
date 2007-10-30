Meteo

  Meteo is a product that let your Plone site shows the local weather forecast
  for Spain provided by the National Institute of Meteorology
  ("www.inm.es":http://www.inm.es)


Features

 * Meteo contains one portlet with a configurable look:

   * Multiple days layout: shows the weather forecast (sky status, maximum and
     minimum temperature) for today and next days.
     
   * Single day layout: shows the weather forecast for today only (sky status
     on morning and afternoon, maximum and minimum temperature).
 
 * Meteo provide a detailed weather forecast page for the next seven days: sky
   status, rainfall probability, maximum and minimum temperature, wind status
   and maximum ultraviolet index.

 * Meteo use a cache system: the INM website will not be asked on every request
   on your site. Every two hours, the INM website will be requested for fresh
   information.
   
 * Meteo contains one configlet that will easily let you enters all the
   configuration information (location code and portlet's look). Moreover is
   possible flush cache data.
 
 * Meteo is translated in english and spanish.
 

Quickstart

 * Install using the normal Plone way.
 
 * Go to the Meteo Configlet and set up your location and portlet's look.

 * That's all


Proxy support

 Define the http_proxy variable in the format http://host:port/. If you have to
 login then use the format http://username:password@host:port/. To define this
 variable add the following lines to the root login file /etc/profile:

 http_proxy=http://host:port/
 export http_proxy


License

  Copyright (C) 2007 GMV SGI Team ("www.gmv-sgi.es":http://www.gmv-sgi.es)
 
  This program is free software; you can redistribute it and/or
  modify it under the terms of version 2 of the GNU General Public
  License as published by the Free Software Foundation.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  USA

  Meteo is based on "Weather Forecast for Plone":http://plone.org/products/ploneweatherforecast
  original code source.

  The icons used by the product have been provided by National Institute of
  Meteorology website.
  
Credits

  Developed by Sergio Martín Morillas ("smartin@gmv.com":mailto:smartin@gmv.com)
