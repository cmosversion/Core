#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb
from codetable_db import CodeTableDb
from person_db import PersonDb

class ContactTypeCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(ContactTypeCodeDb, self).__init__(db, 'contact_type_code')

class ContactOrderDb(CoreDb):
    def _init_db(self):
        self.define_contact_order()
    def define_contact_order(self):
        db.define_table('contact_order', Field('sort_order', 'integer'), Field('order_name', 'string'), Field('order_idenfier', 'string'))

class ContactDb(CoreDb):
    def _init_db(self):
        self.define_contact_type()
        self.define_contact()

    def define_contact_type(self):
        self.define_contact_person()
        self.define_contact_address()
        self.define_contact_phone()

    def define_contact(self):
        if self.is_table_undefined('contact'):
            self._db.define_table('contact'
                , Field('contact_type', self._db.contact_type)
                , Field('description', 'text')
                , Field('created_on', 'datetime')
                , Field('updated_on', 'datetime')
                , Field('deleted_on', 'datetime')
            )
    def define_contact_person(self):
        ContactPersonDb(self._db)
    def define_contact_address(self):
        ContactAddressDb(self._db)
    def define_contact_phone(self):
        ContactPhoneDb(self._db)

class ContactPerson(CoreDb):
    def _init_db(self):
        self.define_contact()
        self.define_person()
        self.define_contact_order()
        self.define_contact_person()
    def define_contact_order(self):
        ContactOrder(self._db)
    def define_contact(self):
        ContactDb(self._db)
    def define_person(self):
        PersonDb(self._db)
    def define_contact_person(self):
        if self.is_table_undefined('contact_person'):
            self._db.define_table('contact_person'
                 , Field('contact_id', self._db.contact)
                 , Field('person_id', self._db.person)
                 , Field('contact_order_id', self._db.contact_order)
             )
