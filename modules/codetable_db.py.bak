#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreTableDb

import six

class CodeTableDb(CoreTableDb):
    _table_name = None
    _fields = [
        Field('code_key', 'string')
        , Field('code_translation', 'string')
        , Field('code_identifier', 'string')
        , Field('code_order', 'integer')
        , Field('deactivated_on', 'datetime')
    ]
