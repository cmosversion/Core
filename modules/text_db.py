#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb
from core_db import CoreTableDb
from core_util import CoreUtil
from core_util import DataUtil
from hashlib import md5

#Text Manager
class TIDb(CoreDb):

    text_definition = {}

    __text=''
    _identifier_db = None
    _definition_db = None
    _definition_identifier_db = None

    def __init__(self, db=None, resource=None, identifier=None):
        super(TIDb, self).__init__(db)

        self.define_definition_identifier()
        self.process_fresh()

        if resource==None and identifier==None:
            return

        self._init_text_definition(resource)
        text_data = self.getText(resource, identifier)

        self.__text = text_data

    def define_definition_identifier(self):
        self._definition_identifier_db = TextDefinitionIdentifierDb(self._db)
        self._identifier_db = self._definition_identifier_db.get_identifier_db()
        self._definition_db = self._definition_identifier_db.get_definition_db()

    def _init_text_definition(self, resource):
        identifier_aff = self._definition_identifier_db.get_identifier_aff()
        definition_aff = self._definition_identifier_db.get_definition_aff()
        identifier_source = (self._identifier_db.get_text_resource()==resource)
        definition_source = (self._definition_db.get_text_definition()==self._definition_identifier_db.get_text_identifier_id())

        text_definition = self._db(
            identifier_aff & definition_aff & identifier_source & definition_source
        ).select(self._identifier_db.get_text_identifier(), self._definition_db.get_text_definition())

        if len(text_definition) > 0:
            for identifier_definition in text_definition:
                if hasattr(self.text_definition, resource) != True:
                    self.text_definition[resource] = {}
                self.text_definition[resource][identifier_definition.identifier] = identifier_definition.definition

    def get_identifier_db(self):
        return self._identifier_db

    def get_definition_db(self):
        return self._definition_db

    def get_definition_identifier_db(self):
        return self._definition_identifier_db

    def getText(self, resource, identifier):
        if resource == None:
            resource = 'None'

        if identifier == None:
            identifier = 'None'

        if hasattr(self.text_definition, resource):
            if hasattr(self.text_definition[resource], identifier):
                return self.text_definition[resource][idenfier]

        identifier_aff = self._definition_identifier_db.get_identifier_aff()
        definition_aff = self._definition_identifier_db.get_definition_aff()
        identifier_source = (self._identifier_db.get_text_resource()==resource)
        identifier_identifier = (self._identifier_db.get_text_identifier()==identifier)

        text_definition = self._db(
            identifier_aff & definition_aff & identifier_source & identifier_identifier
        ).select(self._definition_db.get_text_definition())

        if len(text_definition) > 0:
            definition = text_definition.first().definition
            if hasattr(self.text_definition, resource) != True:
                self.text_definition[resource] = {}
            self.text_definition[resource][identifier] = definition
            return definition

        return ''

    def add_basic_definition_identifier(self, appl, cont, func, iden, definition):
        return self._definition_identifier_db.add_basic_definition_identifier(
            appl, cont, func, iden, definition
        )


    def add_definition_identifier(self, definition, resource, identifier):
        return self._definition_identifier_db.add_definition_identifier(
            definition, resource, identifier
        )

    def reassign_identifier(self, identifier_id, definition_id=None):
        return self._definition_identifier_db.reassign_identifier(identifier_id, definition_id)

    def assign_definition_to_identifier(self, definition_id, identifier_id):
        return self._definition_identifier_db.assign_definition_to_identifier(definition_id, identifier_id)

    def get_definition_assignments(self, definition_id):
        return False

    def get_identifier_assignment(self, identifier_id):
        return False

    def delete_definition_assignment(self, definition_id, identifier_id=None):
        return self._definition_identifier_db.delete_definition_assignment(definition_id, identifier_id)

    def get_default_identifier(self):
        return dict(application='', controller='', function='', identifier='')

    def get_default_definition(self):
        return dict(definition='')

    def get_identifier(self, identifier_id):
        return self._identifier_db.get_identifier(identifier_id)

    def get_all_identifier(self, identifier_id):
        return self._identifier_db.get_all_identifier(identifier_id)

    def get_all_definition(self):
        all_definition = (self._definition_db.get_table().id>0)
        all_definition_identifier = self._definition_identifier_db.get_definition_aff()
        return self._db(all_definition & all_definition_identifier)

    def process_fresh(self):

        if (self.get_all_definition().count()>0)!=True:
            self.define_definition_identifier_data()

    # Initial or Default definitions and identifier w/ assignments
    #
    def __get_initial_definition_identifier(self):
        return [
            #Labels
            dict(identifier='identifier_label', definition='Identifier')
            , dict(identifier='definition_label', definition='Definition')
            , dict(identifier='application_label', definition='Application')
            , dict(identifier='controller_label', definition='Controller')
            , dict(identifier='function_label', definition='Function')
            , dict(identifier='save_label', definition='Save')

            #Titles
            , dict(identifier='identifier_table_title', definition='Identifier List')
            , dict(identifier='definition_table_title', definition='Definition List')
            , dict(identifier='definition_identifier_table_title', definition='Definition w/ Identifier(s) List')
            , dict(identifier='identifier_form_title', definition='Identifier')
            , dict(identifier='definition_form_title', definition='Definition')
            , dict(identifier='definition_identifier_form_title', definition='Definition/Idenfier Form')
            , dict(identifier='definition_identifier_title', definition='Definition/Identifier List')
            , dict(identifier='page_title', definition='Text Manager')

            #Messages
            , dict(identifier='confirm_delete_identifier', definition='Are you sure you want to remove this identifier(s) including all association to definitions')
            , dict(identifier='confirm_delete_definition', definition='Are you sure you want to remove this definition(s) including all association to identifiers')
            , dict(identifier='confirm_delete_definition_identifier', definition='Are you sure you want to remove this association between definition(s) and identifier(s)')
            , dict(identifier='delete_identifier_succeed', definition='Identifier successfully deleted')
            , dict(identifier='delete_definition_succeed', definition='Definition successfully deleted')
            , dict(identifier='delete_definition_identifier_succeed', definition='Definition w/ identifier(s) successfully deleted')
            , dict(identifier='delete_selected_identifier_succeed', definition='Selected identifier(s) successfully deleted')
            , dict(identifier='delete_selected_definition_identifier_succeed', definition='Selected definition(s) w/ identifier(s) successfully deleted')
            , dict(identifier='delete_selected_definition_succeed', definition='Selected definition(s) successfully deleted')
            , dict(identifier='select_definition', definition='Please select at least one(1) definition')
            , dict(identifier='select_definition_identifier', definition='Please select at least one(1) definition identifier(s) association')
            , dict(identifier='select_identifier', definition='Please select at least one(1) identifier')
            , dict(identifier='unassign_identifier', definition='Are you sure you want to unassign this identifier?')
        ]

    def define_definition_identifier_data(self):
        initial_definition_identifier = self.__get_initial_definition_identifier()

        for definition_identifier in initial_definition_identifier:
            self.add_basic_definition_identifier(
                'Core', 'text_manager', 'index', definition_identifier.get('identifier'), definition_identifier.get('definition')
            )

    def get_text_definition(self):
        return self.text_definition
    def __str__(self):
        return self.__text

# DEFINITION IDENTIFIER
#
class TextDefinitionIdentifierDb(CoreTableDb):
    _table_name = 'text_definition_identifier'
    _identifier_db = None
    _definition_db = None

    def _init_db(self):
        self.define_identifier()
        self.define_definition()
        self.define_fields()

    def define_identifier(self):
        self._identifier_db = TextIdentifierDb(self._db)

    def define_definition(self):
        self._definition_db = TextDefinitionDb(self._db)

    def define_fields(self):
        self._fields = [
            Field('text_identifier_id', self._identifier_db.get_table())
            , Field('text_definition_id', self._definition_db.get_table())
        ]

    def get_text_identifier_id(self):
        return getattr(self._db, self._table_name).text_identifier_id

    def get_text_definition_id(self):
        return getattr(self._db, self._table_name).text_definition_id

    def get_identifier_db(self):
        return self._identifier_db

    def get_definition_db(self):
        return self._definition_db

    def get_identifier_aff(self):
        return (self._identifier_db.get_table().id==self.get_text_identifier_id())

    def get_definition_aff(self):
        return (self._definition_db.get_table().id==self.get_text_definition_id())

    def delete_by_identifier_id(self, identifier_id):
        identifier_id = DataUtil().int_to_list(identifier_id)
        return self._db(self.get_text_identifier_id().belongs(identifier_id)).delete()

    def delete_by_definition_id(self, identifier_id):
        definition_id = DataUtil().int_to_list(definition_id)

        return self._db(self.get_text_definition_id().belongs(definition_id)).delete()

    def delete_definition_assignment(self, definition_id, identifier_id=None):
        definition_id = DataUtil().int_to_list(definition_id)

        if identifier_id == None:
            return self._db(self.get_text_definition_id().belongs(definition_id)).delete()

        identifier_id = CoreUtil.int_to_list(identifier_id)

        return self._db(
            (self.get_text_identifier_id().belongs(identifier_id))
            &
            (self.get_text_definition_id().belongs(definition_id))
        ).delete()

    def add_basic_definition_identifier(self, appl, cont, func, iden, definition):

        if self._identifier_db.is_valid_basic_identifier(appl, cont, func, iden) != True:
            return False

        if self._definition_db.is_valid_definition(definition) != True:
            return False

        identifier_id = self._identifier_db.add_basic_identifier(appl, cont, func, iden)
        definition_id = self._definition_db.add_definition(definition)

        return self.assign_definition_to_identifier(definition_id, identifier_id)

    def add_definition_identifier(self, definition, resource, identifier):
        definition_id = self._definition_db.add_definition(definition)

        if definition_id == False:
            return False

        identifier_id = self._identifier_db.add_identifier(resource, identifier)

        if identifier_id == False:
            return False

        self.assign_definition_to_identifier(definition_id, identifier_id)

    def reassign_identifier(self, identifier_id, definition_id=None):
        if definition_id==None:
            return self.delete_by_identifier_id(identifier_id)

        return self.assign_definition_to_identifier(definition_id, identifier_id)

    def assign_definition_to_identifier(self, definition_id, identifier_id):
        return self.get_table().update_or_insert(
            (self.get_text_identifier_id()==identifier_id)
            , text_identifier_id=identifier_id
            , text_definition_id=definition_id
        )



# DEFINITION
#
class TextDefinitionDb(CoreTableDb):
    _table_name = 'text_definition'
    _fields = [
        Field('definition', 'text', label='Definition')
        , Field('i_uid', 'string', label='Unique Identifier')
    ]

    def get_text_definition(self):
        return self.get_table().definition

    def get_text_definition_id(self):
        return self.get_table().id

    def get_text_definition_uid(self):
        return self.get_table().i_uid

    def get_all_definition(self, definition_id):
        identifier_id = DataUtil().int_to_list(identifer_id)
        query = self._db(self.get_text_identifier_id.belongs(identifier_id))
        return query.select(self.get_table().ALL)

    def add_definition(self, definition):
        if isinstance(definition, str):
            md5_lib = md5(definition)
            u_id = md5_lib.hexdigest()

            condition = getattr(self._db, self._table_name).i_uid==u_id
            field = getattr(self._db, self._table_name).id

            for text_definition in self._db(condition).select(field, limitby=(0,1)):
                return text_definition.id

            definition_id = getattr(self._db, self._table_name).insert(
                definition=definition
                , i_uid=u_id
            )
            return definition_id
        return False

    def delete_definition_by_id(self, definition_id):
        definition_id = DataUtil().int_to_list(definition_id)
        self._db(getattr(self._db, self._table_name).id.belongs(definition_id)).delete()
        return True

    def is_valid_definition(self, definition):
        return True

# IDENTIFIER
#
class TextIdentifierDb(CoreTableDb):
    RESOURCE_SEPARATOR = '___'

    _table_name = 'text_identifier'
    _fields = [
        Field('i_resource', 'string')
        , Field('i_identifier', 'string')
        , Field('i_uid', 'string')
    ]

    def get_text_resource(self):
        return self.get_table().i_resource

    def get_text_identifier(self):
        return self.get_table().i_identifier

    def get_text_identifier_id(self):
        return self.get_table().id

    def get_identifier(self, identifier_id):
        for identifier_data in self.gel_all_identifier(identifier_id):
            return identifier_data

    def get_all_identifier(self, identifier_id):
        identifier_id = DataUtil().int_to_list(identifer_id)
        query = self._db(self.get_text_identifier_id().belongs(identifier_id))
        return query.select(self.get_table().ALL)

    def add_identifier(self, resource, identifier):
        if self.is_valid_identifier(resource, identifier):
            identifier_full = '.'.join([resource, identifier])
            md5_lib = md5(identifier_full)
            u_id = md5_lib.hexdigest()

            for text_identifier in self._db(self.get_table().i_uid==u_id).select(self.get_table().id, limitby=(0,1)):
                return text_identifier.id

            identifier_id = getattr(self._db, self._table_name).insert(
                i_resource=resource
                , i_identifier=identifier
                , i_uid=u_id
            )

            return identifier_id
        return False

    def delete_identifier_by_id(self, identifier_id):
        identifier_id = DataUtil().int_to_list(identifier_id)

        self._db(getattr(self._db, self._table_name).id.belongs(identifier_id)).delete()
        return True

    def add_basic_identifier(self, appl, cont, func, iden):
        if self.is_valid_basic_identifier(appl, cont, func, iden):
            rsrc = self.RESOURCE_SEPARATOR.join([appl, cont, func])
            return self.add_identifier(rsrc, iden)
        return False

    def is_valid_identifier(self, resource, identifier):
        return True

    def is_valid_basic_identifier(self, appl, cont, func, iden):
        return True
