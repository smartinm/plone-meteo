Meteo

  Meteo es un producto que muestra en tu sitio Plone la predicción
  meteorológica por localidades ofrecida por la Agencia Estatal de
  Meteorología ("www.aemet.es":http://www.aemet.es).

Características

 * Meteo incluye un portlet con dos tipos de apariencia:

   * Múltiples días: muestra el pronóstico (estado del cielo, temperatura
     máxima y mínima) para el día actual y los próximos.
     
   * Un día: muestra el pronóstico sólo para el día actual (estado del
     cielo por la mañana y por la tarde, temperatura máxima y mínima).
  
 * Meteo ofrece una página de información del tiempo detallada, es posible ver
   la siguiente información meteorológica para los próximos siete días: estado
   del cielo, probabilidad de precipitaciones, temperatura máxima y mínima,
   estado del viento e índice ultravioleta máximo.
 
 * Meteo incorpora un sistema de caché para no solicitar datos al INM cada vez
   que un usuario realiza una petición al servidor, este caché se actualiza
   automáticamente cada 2 horas y sirve de respaldo en caso de caída del
   servidor de INM.
   
 * Meteo viene con un sencillo panel de configuración para Plone donde es
   posible configurar la apariencia del portlet y la localidad que se desea
   mostrar. También es posible forzar la limpieza del caché.
 
 * Meteo está traducido al castellano, euskera e inglés.

Módulos

  Meteo utiliza los siguientes módulos para funcionar:
  
  * Meteo.py: módulo encargado de conectarse al servidor de INM y procesar la
    respuesta, devuelve un diccionario con todos los datos de la predicción
    para una localidad dada.
  
  * BeautifulSoup.py: módulo para parsear código HTML/XHTML, aunque sea
    inválido, convirtiéndolo en una representación en forma de árbol, con
    posibilidad de navegar, buscar y modificar elementos.

Guía rápida de uso

  * Instala el producto Meteo en Plone de la forma habitual.
  
  * Indica una localidad en el panel de configuración, puedes buscar la
    localidad utilizando el buscador incorporado.
    
  * Elige el tipo de portlet que deseas mostrar (varios días o un día), en
    caso de múltiples días puedes configurar el número de días que se muestran.
  
  * Por defecto el portlet aparecerá en la columna derecha, puedes cambiar su
    posición desde el Zope Management Interface (ZMI).

  * Este producto se conecta al servidor web del INM para obtener los datos
    meteorológicos, si en tu red se utiliza un proxy para salir a internet es
    necesario que la siguiente variable de entorno de sistema esté configurada:
    
    http_proxy=http://host:port/
