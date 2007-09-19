# -*- coding: utf-8 -*-
import logging 

# The product name is specified. 
PROJECTNAME = "Meteo"

LOGGER = logging.getLogger(PROJECTNAME)

PORTLET_SINGLE   = 'single'
PORTLET_MULTIPLE = 'multiple'

# The directory that stores skin of this product is specified. 
SKINS_DIR = 'skins'

# A global name space when this product is loaded into Python is 
# preserved. It passes to the package_home() etc.
GLOBALS = globals()
