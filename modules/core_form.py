#!/usr/bin/env python
# coding: utf8
from gluon import *
from gluon.sqlhtml import SQLFORM
from text_db import TIDb
from core_db import CoreDb
from component import Component
from core_util import CoreUtil

class CoreForm(object):
    ADD_PREFIX = 'add_core_'
    DEFAULT_RESOURCE = 'CoreForm__None__None'
    _allow_replicate_core_label = True
    _auto_define = True
    _params = dict()
    _text_manager = None
    _field_list = []
    __option_list={}
    _form = None
    def __init__(self, **params):

        self._params = params
        self._init_form()
        self.__setup_params()
        self.define_fields()

        if self._auto_define == True:
            self.__define_form()

    def __setup_params(self):
        if self._params.get('options_list') != None:
            self.set_option_list(self._params.get('option_list'))
        if self._params.get('field_list') != None:
            self.set_field_list(self._params.get('field_list'))

        if self._params.get('text_manager') != None:
            self.set_text_manager(self._params.get('text_manager'))
        else:
            self.define_text_manager()

        if self._params.get('auto_define') != None:
            if self._params.get('auto_define')==False:
                self._auto_define = False

        if self._params.get('allow_replicate_core_label') is not None:
            self._allow_replicate_core_label = self._params.get('allow_replicate_core_label')

    def define_text_manager(self):
        db = self._params.get('db')
        core_db = CoreDb(db)
        db = core_db.getDb()

        resource = self._params.get('resource')

        if isinstance(resource, str) != True:
            resource = self.DEFAULT_RESOURCE

        self.text_manager = TIDb(db, resource)

    def set_text_manager(self, text_manager):
        if isinstance(text_manager, TIDb):
            self.text_manager = text_manager

    def __define_form(self, **params):
        if self.__has_component() and self.__has_attribute():
            components = params.get('components') + tuple(self._field_list)
            self._form = SQLFORM.factory(components, params.get('attributes'))
        elif self.__has_component() and self.__has_attribute()!=True:
            components = params.get('components') + tuple(self._field_list)
            self._form = SQLFORM.factory(components)
        elif self.__has_component()!=True and self.__has_attribute():
            if len(self._field_list)>0:
                self._form = SQLFORM.factory(params.get('attributes'))
                return
            self._form = SQLFORM.factory(params.get('attributes'))
        else:
            if len(self._field_list)>0:
                self._form = SQLFORM.factory(*tuple(self._field_list))
                return
            self._form = SQLFORM.factory()

    def __has_component(self):
        return self._params.get('components') != None
    def __has_attribute(self):
        return self._params.get('attributes') != None
    def _init_form(self):
        pass
    def set_field_list(self, field_list):
        if isinstance(field_list, list):
            self._field_list = field_list

    def set_option_list(self, option_list):
        if isinstance(option_list, dict):
            self.__option_list = {}
            for option_key, option_data in option_list:
                if (isinstance (option_data, dict)) or (isinstance(option_data, list)):
                    self.__option_list[option_key] = option_data

    def get_option_list(self, option_name, option_type='option'):
        if self.__option_list.get(option_name) != None:
            if option_type=='option':
                options = []
                for option_key, option_data in self.__option_list[option_name]:
                    options.append(
                        OPTION(_name=option_key, _value=option_key, _label=str(option_data))
                    )
                return options
            return self.__option_list[option_name]
        return []

    def define_field(self, fieldname):

        if (hasattr(self, fieldname)) and callable(getattr(self, fieldname)):
            getattr(self, fieldname)()

    def define_fields(self):
        if len(self._field_list)>0:
            for fieldname in self._field_list:
                if isinstance(fieldname, str):
                    self.define_field(self.ADD_PREFIX + fieldname)
            return self

        for callable_method in [method for method in dir(self) if callable(getattr(self, method))]:

            if callable_method.startswith(self.ADD_PREFIX):
                self.define_field(callable_method)

    def get_field_list(self):
        return self._field_list

    def get_option_list(self, ident):
        if isinstance(self.__option_list, dict):
            if hasattr(self.__option_list, ident):
                return self.__option_list
        return []

    def add_field(self, field):
        if isinstance(field, Field)!=True:
            raise TypeError(type(self).__name__() + ".add_field requires a Field type but " + type(field).__name__ + " was passed")
        self._field_list.append(field)

    def add_field_with_label(self, field_type, field_name):
        label = self.get_label(field_name + '_label')
        self.add_field(Field(field_name, field_type, label))

    def get_label(self, **params):
        resource = params.get('resource')
        request_resource = resource

        if (CoreUtil.is_str(resource) != True):
            resource = self.DEFAULT_RESOURCE

        identifier = params.get('identifier')

        if identifier is None:
            raise NotImplementedError("identifier undefined")

        label = self.text_manager.getText(resource, identifier)

        if sel._allow_replicate_core_label and request_resource is not None and label is None:
            label = self.text_manager.getText(self.DEFAULT_RESOURCE, identifier)
            self.text_manager.add_definition_identifier(label, resource, identifier)

        return label

    def get_form(self):
        return self._form

    def get_fields(self):
        return self._field_list

    def xml(self):
        return self._form.xml()
