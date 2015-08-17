# -*- coding: utf-8 -*-
"""Init and utils."""

from AccessControl import ModuleSecurityInfo
from AccessControl import allow_type
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('nudos.theme')


# Products/PythonScripts/module_access_examples.py


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
