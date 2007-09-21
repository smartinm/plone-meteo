# -*- coding: utf-8 -*-
import logging 

# The product name is specified. 
PROJECTNAME = "Meteo"

# Logger
LOGGER = logging.getLogger(PROJECTNAME)

# The directory that stores skin of this product is specified. 
SKINS_DIR = 'skins'

# A global name space when this product is loaded into Python is 
# preserved. It passes to the package_home() etc.
GLOBALS = globals()

# Please don't touch
PORTLET_SINGLE   = 'single'
PORTLET_MULTIPLE = 'multiple'

# Configurable (min 1, max 24)
CACHE_DURATION_IN_HOURS = 2
