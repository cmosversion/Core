#!/usr/bin/env python
# coding: utf8
from gluon import *
from gluon.dal import DAL
from core_util import CoreUtil
from core_util import DataUtil

class Core(object):
    def get_class(self, class_name=None):
        if class_name is None:
            return CoreUtil.get_class(self)
        return CoreUtil.get_class(class_name)

class CoreDb(Core):
    _db=None
    def __init__(self, db=None):
        if self.has_no_connection():
            self._db = db
        else:
            self._db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
        self._init_db()
    def is_table_undefined(self, table_name):
        return not hasattr(self._db, table_name)
    def has_no_connection(self):
        return (isinstance(self._db, DAL) != True)
    def _init_db(self):
        pass
    def getDb(self):
        return self._db
    def getArgVal(self, source_dict, ident, default):
        if hasattr(source_dict, ident):
            return source_dict[ident]
        return default

    def has_connection_and_table():
        return (self.has_no_connection()!=True and self.is_table_undefined(self._table)!=True)

class CoreTableDb(CoreDb):
    _table_name=None
    _fields=None
    def __init__(self, db=None, table_name=None):
        super(CoreTableDb, self).__init__(db)
        #if (table_name is None) is not True:
        #    self._table_name = table_name
        if CoreUtil.is_str(self._table_name)!=True:
            raise TypeError('Table name should be a string type')
        if DataUtil().is_valid_table_name(self._table_name)!=True:
            raise ValueError(DataUtil().get_valid_table_name_message())

        self._init_table()

    def _init_db(self):
        self._define_table_name()
        self._define_fields()

    def _is_valid_table_name(self, table_name):
        if isinstance(table_name, str) != True:
             return False
        return True

    def _define_table_name(self):
        if self._is_valid_table_name(self._table_name)!=True:
            raise ValueError(self.get_class() + ' requires a table name')

    def _define_fields(self):
        if self._fields is None:
            raise ValueError(self.get_class() + ' requires a list of Field')

    def _init_table(self):
        if self.is_table_undefined(self._table_name):
            self._db.define_table(self._table_name, fields=self._fields)

    def set_table_name(self, table_name):
        self._table_name = table_name

    def get_all(self, **kwargs):
        condition = (getattr(self._db, self._table_name).id>0)

        if hasattr(kwargs, 'condition'):
            condition = kwargs.condition
        elif hasattr(kwargs, 'id'):
            primary_id = CoreUtil.int_to_list(kwargs.id)
            condition = (getattr(self._db, self._table_name).id.belongs(primary_id))

        field_list = []
        if hasattr(kwargs, 'fields'):
            for field in kwargs.fields:
                field_list.append(getattr((getattr(self._db, self._table_name)), field))
        else:
            field_list = (getattr(self._db, self._table_name)).ALL

        return self._db(condition).select(field_list)

    def get_row(self, **kwargs):
        for row in self.get_all(**kwargs):
            return row

    def get_one(self, **kwargs):
        data = []
        delimeter = ''
        if hasattr(kwargs, 'delimeter'):
            if isinstance(str, kwargs.delimeter):
                delimeter = kwargs.delimeter
        for field_key, field in self.get_row(**kwargs):
            data.append(field)
        return delimeter.join(data)

    def save(self, data, condition=None):
        if condition==None:
           return self._db(getattr(self._db, self._table_name)).insert(data)
        return self._db(getattr(self._db, self._table_name)).insert_or_update(condition, data)

    def get_table(self):
        return getattr(self._db, self._table_name)
