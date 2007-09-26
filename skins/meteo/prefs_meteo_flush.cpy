## Controller Python Script "prefs_meteo_flush"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Flush Meteo Cache

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

request=context.REQUEST

if hasattr(request, 'form.button.flush'):
    meteoTool = getToolByName(context, 'meteo_tool', None)
    if meteoTool:
        meteoTool.flushCache()
        context.plone_utils.addPortalMessage(_(u'Cache flushed.'))
    return request.RESPONSE.redirect(context.absolute_url() +'/prefs_meteo_form')
