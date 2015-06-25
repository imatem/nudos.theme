# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from nudos.theme.testing import NUDOS_THEME_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that nudos.theme is properly installed."""

    layer = NUDOS_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if nudos.theme is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('nudos.theme'))

    def test_uninstall(self):
        """Test if nudos.theme is cleanly uninstalled."""
        self.installer.uninstallProducts(['nudos.theme'])
        self.assertFalse(self.installer.isProductInstalled('nudos.theme'))

    def test_browserlayer(self):
        """Test that INudosThemeLayer is registered."""
        from nudos.theme.interfaces import INudosThemeLayer
        from plone.browserlayer import utils
        self.assertIn(INudosThemeLayer, utils.registered_layers())
