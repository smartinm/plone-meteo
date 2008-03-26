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
import logging 

from Products.Archetypes.utils import DisplayList

# The product name is specified. 
PROJECTNAME = "Meteo"

# Logger
LOGGER = logging.getLogger(PROJECTNAME)

# The directory that stores skin of this product is specified. 
SKINS_DIR = 'skins'

# A global name space when this product is loaded into Python is 
# preserved. It passes to the package_home() etc.
GLOBALS = globals()

# Porlets internal names, please don't touch.
PORTLET_SINGLE   = 'single'
PORTLET_MULTIPLE = 'multiple'

# XXX: no support yet
AEMET_LANGUAGES = DisplayList((
    ('es', 'Español',    'label_lang_es'),
    ('ca', 'Catalán',    'label_lang_ca'),
    ('gl', 'Gallego',    'label_lang_gl'),
    ('va', 'Valenciano', 'label_lang_va'),
    ('eu', 'Euskera',    'label_lang_eu'),
    ('en', 'Inglés',     'label_lang_en'),
    ('fr', 'Francés',    'label_lang_fr'),
))

# Cache duration in hours
CACHE_DURATION_IN_HOURS = 2

# Timeout on connect to www.aemet.es (set 0 for no timeout, not recommended)
TIMEOUT_IN_SECONDS = 5
