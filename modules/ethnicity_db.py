#!/usr/bin/env python
# coding: utf8
from gluon import *

from codetable_db import CodeTableDb

class CodeEthnicityTypeDb(CodeTableDb):
    def __init__(self, db=None):
        super(CodeEthnicity, self).__init__(db, 'code_ethnicity_type')
