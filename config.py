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

# Cache duration in hours
CACHE_DURATION_IN_HOURS = 2

# Timeout on connect to inm.es (no timeout: None)
TIMEOUT_IN_SECONDS = 20
