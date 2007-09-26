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
from AccessControl import allow_module

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.Meteo import MeteoTool
from Products.Meteo.config import *

allow_module('Products.Meteo.config')

# Register our directory in Zope
registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context) :
    # Initialize the tool
    utils.ToolInit(config.PROJECTNAME + ' Tool',
                   tools=(MeteoTool.MeteoTool,),
                   product_name=config.PROJECTNAME,
                   icon='tool.gif',
    ).initialize(context)
