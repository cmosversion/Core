#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb

class AddressTypeDb(CoreDb):
    def _init_db(self):
        self.define_address_type()
    def define_address_type(self):
        if self.is_table_undefined('address_type'):
            self._db.define_table('address_type', Field('address_type', 'string'), Field('address_type_identifier', 'string'))

class AddressDb(CoreDb):
    def _init_db(self):
        self.define_address_type()
        self.define_address()

    def define_address_type(self):
        address_type_db = AddressTypeDb(self._db)

    def define_address(self):
        self._db.define_table('address', Field('address', 'text'), Field('address_type', self._db.address_type))

    def define_all(self):
        self.define_url_address()
        self.define_email_address()
        self.define_mail_address()

    def define_address_email(self):
        db.define_table('email_address', db.address
            , Field('username', 'string')
            , Field('domain', 'string')
        )
    def define_address_url(self):
        db.define_table('url_address', db.address
            , Field('protocol', 'string')
            , Field('domain', 'string')
            , Field('path', 'string')
            , Field('query_string', 'string')
        )
    def define_address_mail(self):
        db.define_table('mail_address', db.address
            , Field('location', 'string')
            , Field('city', 'string')
            , Field('state', 'string')
            , Field('country', 'string')
            , Field('zip_code', 'string')
        )
