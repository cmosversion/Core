#!/usr/bin/env python
# coding: utf8
from gluon import *

from codetable_db import CodeTableDb

class CodeLanguageTypeDb(CodeTableDb):
    def __init__(self, db=None):
        super(CodeTableDb, self).__init__(self, db, 'code_language_type')
