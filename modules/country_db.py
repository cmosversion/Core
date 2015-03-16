#!/usr/bin/env python
# coding: utf8
from gluon import *

from codetable_db import CodeTableDb

class LanguageCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(LanguageCodeDb, self).__init__(db, 'language_code')

class CountryCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(CountryCodeDb, self).__init__(db, 'country_code')

class CountryAreaCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(CountryAreaCodeDb, self).__init__(db, 'country_area_code')

class ZipCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(ZipCodeDb, self).__init__(db, 'zip_code')
