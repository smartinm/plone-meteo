## Controller Script (Python) "prefs_meteo_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=location_code, portlet_type, portlet_days, RESPONSE=None
##title=Set Meteo Prefs
##

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

REQUEST=context.REQUEST

meteoTool = getToolByName(context, 'meteo_tool', None)

meteoTool.manageFormResults(locationCode=location_code,
                            numDaysInPortlet=int(portlet_days),
                            portletType=portlet_type)

status = "success"
portal_msg = "Meteo Configuration has been successfully updated."
#context.plone_utils.addPortalMessage(_(u'Mail Host Updated'))

return state.set(status=status,
                 portal_status_message=portal_msg)
