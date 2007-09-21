from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Meteo.config import PORTLET_SINGLE
from Products.Meteo.config import PORTLET_MULTIPLE

request = context.REQUEST

required = ('location_code',)
intvals = ('location_code', 'portlet_days', ) 

for k in required:
    v = request.form.get(k, '').strip()
    if not v:
        state.setError(k, _(u'Input is required but not given.'))

for k in intvals:
    v = request.form.get(k, '').strip()
    if v:
        try:
            int(v)
        except ValueError:
            state.setError(k, _(u'Input must be an integer.'))
            
type = request.form.get('portlet_type', '').strip()
if type not in (PORTLET_SINGLE, PORTLET_MULTIPLE):
    state.setError('portlet_type', _(u'Input is required but not given.'))

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
