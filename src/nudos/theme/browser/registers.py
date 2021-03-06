# -*- coding: utf-8 -*-

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from collections import OrderedDict
from zope.component.hooks import getSite
import logging


logger = logging.getLogger("Plone")


class RegistersView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # self.form = None

    def __call__(self):
        form = self.request.form
        if form:
            if 'Aceptar' in form.items()[0][1]:
                self.changeState(form.items()[0][0], 'aceptar')
            elif 'Rechazar' in form.items()[0][1]:
                self.changeState(form.items()[0][0], 'rechazar')
            elif 'Reconsiderar' in form.items()[0][1]:
                self.changeState(form.items()[0][0], 'revisar')
            self.request.response.redirect(self.context.absolute_url() + '/lregistros2016')
        return self.index()

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

    def getDataRegisters2016(self, brains):
        registers = []
        for b in brains:
            obj = b.getObject()
            data = OrderedDict()
            # data['url'] = obj.absolute_url()
            data['uid'] = obj.UID()
            data['name'] = obj.getValue('nombre')
            data['lastname'] = obj.getValue('apellido-paterno')
            data['middlename'] = obj.getValue('apellido-materno')
            data['email'] = obj.getValue('replyto')
            data['gender'] = obj.getValue('genero')
            data['tiposol'] = obj.getValue('tipo-de-inscripcion')
            data['institution'] = obj.getValue('institucion')
            data['comments'] = obj.getValue('comments')
            data['level'] = obj.getValue('nivel')
            data['semester'] = obj.getValue('semestre')
            data['apoyo'] = ', '.join(obj.getValue('solicita-apoyo-para'))
            recomendations = obj.getValue('recomendacion')

            profes = []

            for recomendation in recomendations:
                if not all(map(lambda x: x == '', recomendation.values())):
                    profeval = recomendation['nombre']
                    if recomendation['institucion']:
                        profeval += ' (' + recomendation['institucion'] + ')'
                    if recomendation['correo']:
                        profeval += ' - ' + recomendation['correo']
                    profes.append(profeval)
            data['recomendation'] = ', '.join(profes)

            cdate = obj.created()
            data['cdate'] = '%s de %s de %4.4d %s:%2.2d %s' % (
                cdate._day, self.monthTranslation(cdate._fmon),
                cdate._year, cdate._pmhour,
                cdate._minute, cdate._pm)

            registers.append(data)

        return registers

    def Registers2016(self):
        registers = {'revision': [], 'aceptado': [], 'rechazado': []}
        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='revision',
            path='/escuelanudos2015/registro-2016',
        )
        registers['revision'] = self.getDataRegisters2016(brains)

        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='aceptado',
            path='/escuelanudos2015/registro-2016',
        )
        registers['aceptado'] = self.getDataRegisters2016(brains)

        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='rechazado',
            path='/escuelanudos2015/registro-2016',
        )
        registers['rechazado'] = self.getDataRegisters2016(brains)

        return registers

    def getDataRegisters(self, brains):
        registers = []
        for b in brains:
            obj = b.getObject()
            data = OrderedDict()
            # data['url'] = obj.absolute_url()
            data['uid'] = obj.UID()
            data['name'] = obj.getValue('nombre')
            data['lastname'] = obj.getValue('apellido-paterno')
            data['middlename'] = obj.getValue('apellido-materno')
            data['email'] = obj.getValue('replyto')
            data['gender'] = obj.getValue('genero')
            data['level'] = obj.getValue('nivel')
            data['semester'] = obj.getValue('semestre')
            data['institution'] = obj.getValue('institucion')
            recomendations = obj.getValue('recomendacion')

            profes = []
            for recomendation in recomendations:
                if not all(map(lambda x: x == '', recomendation.values())):
                    profes.append(recomendation)
            data['recomendation'] = profes[0]['nombre'] + ' (' + profes[0]['institucion'] + ') - ' + profes[0]['correo'] + ', ' + profes[1]['nombre'] + ' (' + profes[1]['institucion'] + ') - ' + profes[1]['correo']
            data['comments'] = obj.getValue('comments')
            cdate = obj.created()
            data['cdate'] = '%s de %s de %4.4d %s:%2.2d %s' % (
                cdate._day, self.monthTranslation(cdate._fmon),
                cdate._year, cdate._pmhour,
                cdate._minute, cdate._pm)

            registers.append(data)

        return registers

    def Registers(self):
        registers = {'revision': [], 'aceptado': [], 'rechazado': []}
        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='revision'
        )
        registers['revision'] = self.getDataRegisters(brains)

        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='aceptado'
        )
        registers['aceptado'] = self.getDataRegisters(brains)

        brains = self.catalog.searchResults(
            portal_type='FormSaveData2ContentEntry',
            review_state='rechazado'
        )
        registers['rechazado'] = self.getDataRegisters(brains)

        return registers

    def changeState(self, uid_register, status_register):
        brains = self.catalog.searchResults(
            UID=uid_register,
        )
        obj = brains[0].getObject()
        workflowTool = getToolByName(obj, "portal_workflow")
        try:
            workflowTool.doActionFor(obj, status_register)
        except WorkflowException:
            logger.info("Could not change status:" + str(obj.getId()))
