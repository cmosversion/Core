#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb

class PhoneTypeDb(CoreDb):
    def _init_db(self):
        self.define_phone_type()
    def define_phone_type(self):
        if self.is_table_undefined('phone_type'):
            self._db.define_table('phone_type'
                , Field('phone_type', 'string')
                , Field('description', 'text')
            )

class PhoneDb(CoreDb):
    def _init_db(self):
        self.define_phone_type()
        self.define_phone()
    def define_phone_type(self):
        PhoneTypeDb(self._db)
    def define_phone(self):
        if self.is_table_undefined('phone'):
            self._db.define_table('phone'
                , Field('phone_number', 'integer')
                , Field('phone_number_type_id', self._db.phone_number_type)
            )

class TelephoneDb(PhoneDb):
    def _init_db(self):
        super(TelephoneDb, self)._init_db()
        self.define_telephone()
    def define_telephone(self):
        if self.is_table_undefined('telephone'):
            self._db.define_table('telephone'
                , Field('phone_id', self._db.phone)
                , Field('country_code', 'integer')
                , Field('area_code', 'integer')
                , Field('network_code', 'integer')
                , Field('phone_code', 'integer')
                , Field('extension_code', 'integer')
            )

class MobilePhoneDb(PhoneDb):
    def _init_db(self):
        super(MobilePhoneDb, self)._init_db()
        self.define_mobile_phone()
    def define_mobile_phone(self):
        if self.is_table_undefined('mobile_phone'):
            self._db.define_table('mobile_phone'
                , Field('phone_id', self._db.phone)
                , Field('country_code', 'integer')
                , Field('mobile_prefix', 'integer')
                , Field('national_significant_number', 'integer')
            )
