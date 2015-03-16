#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb
from language_db import CodeLanguageTypeDb
from ethnicity_db import CodeEthnicityTypeDb
from gender_db import CodeGenderTypeDb

class PersonDb(CoreDb):
    def _init_db(self):
        if self.has_connection():
            self.define_code_language_type()
            self.define_code_ethnicity_type()
            self.define_code_gender_type()
            self.define_person()
    def define_code_language_type(self):
        CodeLanguageTypeDb(self._db)
    def define_code_ethnicity_type(self):
        CodeEthnicityTypeDb(self._db)
    def define_code_gender_type(self):
        CodeGenderTypeDb(self._db)
    def define_person(self):
        if (self.is_table_undefined('person')):
            self.define_table(
                'person'
                , Field('first_name', 'string'), Field('middle_name', 'string'), Field('last_name', 'string')
                , Field('gender_id', self._db.code_gender_type), Field('birth_date', 'date'), Field('primary_language_id', self._db.code_language_type)
                , Field('primary_ethnicity_id', self._db.code_ethnicity_type)
            )
