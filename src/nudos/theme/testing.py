# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig

import nudos.theme


class NudosThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            nudos.theme,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nudos.theme:default')


NUDOS_THEME_FIXTURE = NudosThemeLayer()


NUDOS_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NUDOS_THEME_FIXTURE,),
    name='NudosThemeLayer:IntegrationTesting'
)


NUDOS_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NUDOS_THEME_FIXTURE,),
    name='NudosThemeLayer:FunctionalTesting'
)


NUDOS_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NUDOS_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='NudosThemeLayer:AcceptanceTesting'
)
