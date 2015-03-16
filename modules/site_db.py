#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb
from core_db import CoreTableDb
from contact_db import ContactDb
from codetable_db import CodeTableDb

class SiteTypeCodeDb(CodeTableDb):
    def __init__(self, db=None):
        super(SiteTypeCodeDb, self).__init__(db, 'site_type_code')

class SiteDb(CoreTableDb):
    _table_name = 'site'
    def _init_db(self):

        self.define_contact()
        self.define_site_type()

        super(SiteDb, self)._init_db()

    def define_contact(self):
        ContactDb(db)
    def define_site_type(self):
        SiteTypeCode(self._db)
    def define_fields(self):
        self._fields = [
            Field('site_id', 'integer')
            , Field('site_name', 'string')
            , Field('site_type_code', self._db.site_type_code)
            , Field('lt', 'integer')
            , Field('gt', 'integer')
            , Field('contact_id', self._db.contact)
        ]


class SiteChild(CoreDb):
    def _init_db(self):
        self.define_site()
        self.define_site_child()
    def define_site(self):
        SiteDb(self._db)
    def define_site_child(self):
        if self.is_table_undefined('site_child'):
            self._db.define_table('site_child'
                , Field('site_id', self._db.site)
                , Field('child_site_id', self._db.site)
            )
