# -*- coding: utf-8 -*-

# from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
# from StringIO import StringIO
# from matem.sis import MessageFactory as _
# from operator import itemgetter
# from plone.behavior.interfaces import IBehavior
# from plone.dexterity.interfaces import IDexterityFTI
# from zope.component import getMultiAdapter
# from zope.component import getUtility
from zope.component.hooks import getSite
from collections import OrderedDict
# from zope.i18n import translate
# from zope.schema.interfaces import IVocabularyFactory


class RegistersView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # self.form = None

    @property
    def catalog(self):
        return getToolByName(getSite(), 'portal_catalog')

    def monthTranslation(self, fmon):
        # translate((cdate._fmon), domain='plone', target_language=self.context.REQUEST.LANGUAGE)
        _MONTHS = {
            'January': 'Enero',
            'February': 'Febrero',
            'March': 'Marzo',
            'April': 'Abril',
            'May': 'Mayo',
            'June': 'Junio',
            'July': 'Julio',
            'August': 'Agosto',
            'September': 'Septiembre',
            'October': 'Octubre',
            'November': 'Noviembre',
            'December': 'Diciembre',
        }
        return _MONTHS.get(fmon, '')

    def getDataRegisters(self, brains):
        registers = []
        for b in brains:
            obj = b.getObject()
            data = OrderedDict()
            data['name'] = obj.getValue('nombre')
            data['lastname'] = obj.getValue('apellido-paterno')
            data['middlename'] = obj.getValue('apellido-materno')
            data['email'] = obj.getValue('replyto')
            data['gender'] = obj.getValue('genero')
            data['level'] = obj.getValue('nivel')
            data['semester'] = obj.getValue('semestre')
            data['institution'] = obj.getValue('institucion')
            profes = obj.getValue('recomendacion')
            data['recomendation'] = profes[0]['nombre'] +' (' + profes[0]['institucion'] + ') - ' + profes[0]['correo'] + ', ' + profes[1]['nombre'] +' (' + profes[1]['institucion']+ ') - ' + profes[1]['correo']
            data['comments'] = obj.getValue('comments')
            cdate = obj.created()
            data['cdate'] = '%s de %s de %4.4d %s:%2.2d %s' % (
                cdate._day, self.monthTranslation(cdate._fmon),
                cdate._year, cdate._pmhour,
                cdate._minute, cdate._pm)

            registers.append(data)

        return registers

    def Registers(self):
        registers = {'revision': [], 'accepted': [], 'rejected': []}
        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            # review_state=''
        )

        registers['revision'] = self.getDataRegisters(brains)

        return registers
