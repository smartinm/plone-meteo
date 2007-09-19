# -*- coding: utf-8 -*-
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
