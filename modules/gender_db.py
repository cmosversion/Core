#!/usr/bin/env python
# coding: utf8
from gluon import *

from codetable_db import CodeTableDb

class CodeGenderTypeDb(CodeTableDb):
    def __init__(self, db=None):
        super().__init__(db, 'code_gender_type')
