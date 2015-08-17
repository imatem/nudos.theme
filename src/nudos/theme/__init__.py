# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('nudos.theme')


# Products/PythonScripts/module_access_examples.py
from AccessControl import allow_type
from AccessControl import ModuleSecurityInfo

ModuleSecurityInfo('re').declarePublic(
    'compile',
    'findall',
    'match',
    'search',
    'split',
    'sub',
    'subn',
    'error',
    'I',
    'L',
    'M',
    'S',
    'X',
)
import re
allow_type(type(re.compile('')))
allow_type(type(re.match('x','x')))
