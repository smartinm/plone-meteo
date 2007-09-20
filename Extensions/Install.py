# -*- coding: utf-8 -*-

from cStringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName

from Products.Meteo.config import *

import string

# Configlets to be added to control panels or removed from them
configlets = (
    {
        'id'         : 'meteo_config',
        'name'       : 'Meteo Configuration',
        'action'     : 'string:${portal_url}/prefs_meteo_form',
        'condition'  : '',
        'category'   : 'Products',    # section to which the configlet should be added:
                                      # (Plone,Products,Members)
        'visible'    : 1,
        'appId'      : PROJECTNAME,
        'permission' : ManagePortal,
        'imageUrl'   : 'prefs_meteo_icon.png',
    },
)

# Portlet
portletPath = "here/portlet_meteo/macros/portlet"

def installPortlet(self, outStream):
    if hasattr(self, "right_slots"):
        if portletPath in self.right_slots:
            outStream.write("Meteo portlet already installed, nothing to do.\n")
        else:
            right_slots_list = list(self.right_slots)
            self._delProperty('right_slots')
            right_slots_list.append(portletPath)
            self._setProperty('right_slots', tuple(right_slots_list), 'lines')
            outStream.write("Meteo was installed on the right. To change this, edit the left and right_slots properties in the ZMI.\n")
    else:
        outStream.write("No attribute right_slots was found in context, nothing done. You have to add manually '%s' in the left and right_slots properties in the ZMI.\n" % portletPath)


def uninstallPortlet(self, outStream):
    for attributeName in ["right_slots", "left_slots"]:
        try:
            attrib = getattr(self, attributeName)
            if portletPath in attrib:
                slotsList = list(attrib)
                self._delProperty(attributeName)
                slotsList.remove(portletPath)
                self._setProperty(attributeName, tuple(slotsList), 'lines')
                outStream.write("Meteo was removed from %s.\n" % attributeName)
            else:
                pass
#                 outStream.write("debug : portlet not found in %s.\n" % (attributeName))
        except AttributeError:
            outStream.write("Warning : No attribute %s was found in context.\n" % attributeName)

def installSubSkin(context, skinFolder, outStream):
    """ Install a subskin in portal_skins
    """
    skinsTool = getToolByName(context, 'portal_skins')
    for skin in skinsTool.getSkinSelections():
        path = skinsTool.getSkinPath(skin)
        path = map(string.strip, string.split(path,',' ))
        if not skinFolder in path:
            try:
                path.insert( path.index( 'custom')+1, skinFolder )
            except ValueError:
                path.append(skinFolder)
            path = string.join( path, ', ' )
            skinsTool.addSkinSelection( skin, path )
            outStream.write('Subskin successfully installed into %s.\n' % skin)
        else:
            outStream.write('Subskin was already installed into %s.\n' % skin)

def addWeatherTool(self, out):
    # Check that the tool has not been added using its id
    if not hasattr(self, 'meteo_tool'):
        addTool = self.manage_addProduct['Meteo'].manage_addTool
        # Add the tool by its meta_type
        addTool('Meteo Tool')
    weatherTool = getToolByName(self, 'meteo_tool', None)
    #result = weatherTool.migrate()
    #out.write(result + "\n")

def installConfiglet(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

def uninstallConfiglet(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

def install_css(self, out):
    """ install custom CSS used by ATAudio """
    portal_css = getToolByName(self, 'portal_css')
    portal_css.manage_addStylesheet(# Object name to registration.
                                    id = 'meteo_style.css',
                                    # TAL expression for using condition
                                    expression = '',
                                    # browser media type
                                    media = 'all',
                                    # Title for portal_css
                                    title = 'Meteo styles',
                                    # initial available status.
                                    enabled = True)
                                    
    out.write("Installed CSS for Meteo into portal_css.\n") 
    
def install(self):
    outStream = StringIO()

    skinsTool = getToolByName(self, 'portal_skins')
    addDirectoryViews(skinsTool, SKINS_DIR, GLOBALS)
    installSubSkin(self, 'meteo', outStream)
    install_css(self, outStream)
    addWeatherTool(self, outStream)
    installPortlet(self, outStream)
    installConfiglet(self, outStream)
    return outStream.getvalue()

def uninstall(self):
    outStream = StringIO()
    uninstallPortlet(self, outStream)
    uninstallConfiglet(self, outStream)
    return outStream.getvalue()
