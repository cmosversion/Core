#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb

import six

class CodeTableDb(CoreDb):
    def __init__(self, db=None, table_name=None):
        super(CodeTableDb, self).__init__(db)
        if isinstance (table_name, six.string_types):
             self.define_codetable(table_name)
    def define_codetable(self, table_name):
        if self.is_table_undefined(table_name):
            self._db.define_table(
                table_name
                , Field('code_key', 'string')
                , Field('code_translation', 'string')
                , Field('code_identifier', 'string')
                , Field('code_order', 'integer')
                , Field('deactivated_on', 'datetime')
             )
