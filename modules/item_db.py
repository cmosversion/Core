#!/usr/bin/env python
# coding: utf8

# Base code for dynamic item creation
#
#

# Standard python library for regular expression
import re

# Web2py library
from gluon import *

# Core database
from core_db import CoreTableDb
from core_util import DataUtil

# Core table base
from codetable_db import CodeTableDb

# Item type code table database definition
class ItemTypeCodeDb(CodeTableDb):
    _table_name = 'item_type_code'

    def code_identifier_exists(code_identifier):
        code_identifier_condition = self._db(self.get_table_column('code_identifier')==item_type)
        item_types = self.get_all(condition=condition)

        for item_type in item_types:
            return True

        return False

    def get_item_type_by_id(self,item_type_id, field):
        condition = self._db(self.get_table_column('id').belongs(item_type_id))
        item_type = self._item_type_db.get_one(fields=[field], condition=condition)

        return item_type

# Base item
#
#
class ItemDb(CoreTableDb):
    # depth level limit in recursion to avoid memory scarcity
    MAX_DEPTH = 20

    # Required name of this object (required for db table generation)
    # Must be defined before along in instantiation (Can't use get_class because often times it is used in during class instantiation)
    _name = 'Item'

    # Item type db holder
    _item_type_db = None

    # Items db holder
    _items_db = None

    # Items type
    _items_type_db = dict()

    def _init_db(self):
        self._define_item_type()
        self._define_table_name()
        self._define_fields()

    def _define_item_type(self):
        self._item_type_db = ItemTypeCodeDb(self._db)

    def _init_table(self):
        self._define_default_item_types()

    def _define_default_item_types(self):

        item_types = self.get_default_item_types()

        for item_type in item_types:
            self._item_type_db.save(item_type)

    def get_default_item_types(self):
        code = self._get_name()
        code_identifier = self.camel_case_to_underscore(code)

        item_types = [
            dict(code_key=code, code_translation=code, code_identifier=code_identifier)
        ]

        return item_types

    def _define_table_name(self):
        return self._get_table_name()

    def _define_fields(self):
        self._fields = [
            Field('item', 'string')
            , Field('description', 'string')
            , Field('is_primary', 'boolean')
            , Field('version', 'number')
            , Field('revision', 'number')
            , Field('version_id', 'integer')
            , Field('item_type_id', self._item_type_db.get_table())
            , Field('lt', 'integer')
            , Field('rt', 'integer')
            , Field('created_on', 'datetime')
            , Field('updated_on', 'datetime')
            , Field('deleted_on', 'datetime')
        ]

        def save(self, item):
            items = item.get('items')
            item_fields = item.get('fields')
            data = item.get('data')

            if items is not None:
                del item['items']

            parent_item_id = item.get('parent_item_id')
            parent_item_type_id = item.get('parent_item_type_id')

            if parent_item_id is not None:
                del item['parent_item_id']

            item_id = item.get('item_id')
            item_type_id = item.get('item_type_id')
            item_type = self._item_type_db.get_item_type_by_id(item_type_id, 'code_identifier')
            item_class = self.underscore_to_camel_case(item_type) + 'Db'

            if item_id is None:
                item_id = super(globals()[item_class], self).save(item)
            else:
                item_id = super(globals()[item_class], self).save(item, (self.get_table_column('id')==item_id))

            if parent_item_id is not None:
                items_condition = self._db(
                    (self._items_db.get_column('item_id')==parent_item_id)
                    &
                    (self._items_db.get_column('sort_order')==item.get('sort_order'))
                )

                data = dict(
                    item_id=parent_item_id
                    , sort_order=item.get('sort_order')
                    , item_type_id=item_type_id
                )

                parent_item_name = self._item_type_db.get_item_type_by_id(parent_item_type_id, 'code_identifier')
                parent_items_class = self.underscore_to_camel_case(parent_item_name) + 'ItemsDb'
                parent_items_db = globals()[parent_item_class](self._db)

                parent_items_id = parent_items_db.save(data, condition=items_condition)

                parent_child_item_db = self.__get_parent_child_item_db(parent_item_name, item_name)

                data = dict(items_id=parent_items_id, child_item_id=item_id)
                condition = self._db(parent_child_item_db.get_table_column('items_id')==parent_items_id)

                parent_child_item_db.save(data, condition)

            for item in items:
                self.save(item)

    def get_primary_items(self):
        condition = self._db(self.get_table_column('is_primary')==True)
        primary_items = self.get_all(condition)

        return primary_items

    def __get_parent_child_item_db(self, parent_item_name, item_name):
        parent_child_item_name = '_'.join([parent_item_name, item_name])
        parent_child_item_class = self.underscore_to_camel_case(parent_child_item_name)
        parent_child_item_db = globals()[parent_child_item_class](self._db)

        return parent_child_item_db

    def create_item_objects(self, item_type, item_types=None):
        item_object = self.create_item_object(item_type)
        item_items = self.create_item_items(item_type)
        item_data = self.create_item_data(item_type)
        item_relations = self.create_item_relations(item_type, item_types)

        item_objects = dict(
            item=item_object
            , item_items=item_items
            , item_data=item_data
            , item_relations=item_relations
        )

        return item_objects

    def create_item_object(self, item_type):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_name_db = item_type_class_name + 'Db'

        if item_type_class_name_db in globals():
            return globals[item_type_class_name_db]

        item = type(item_type_class_name_db, (ItemDb), dict(_name=item_type_class_name))
        globals()[item_type_class_name_db] = item

        return item

    def create_item_items(self, item_type):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_name_db = item_type_class_name + 'ItemsDb'

        if item_type_class_name_db in globals():
            return globals[item_type_class_name_db]

        item = type(item_type_class_name_db, (ItemItemsDb), dict(_name=item_type_class_name))
        globals()[item_type_class_name_db] = item

        return item

    def create_item_data(self, fields):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_name_db = item_type_class_name + 'DataDb'

        if item_type_class_name_db in globals():
            return globals[item_type_class_name_db]

        item = type(item_type_class_name_db, (ItemItemsDb), dict(_name=item_type_class_name))
        globals()[item_type_class_name_db] = item

        return item

    def create_item_relations(self, item, item_types=None):
        if item_types is None:
            item_types = self._item_type_db.get_all()

        item_relations = {}

        item_class_name = self.underscore_to_camel_case(item)

        for item_type in item_types:
            item_relation = item + '_' + item_type

            if item_relation in item_relations:
                continue

            child_class_name = self.underscore_to_camel_case(item_type)
            item_class_name_db = self.underscore_to_came_case(item_relation + '_db')

            if item_class_name_db in globals():
                item_relations[item_relation] = globals[item_class_name_db]
                continue

            item = type(
                item_class_name_db
                , (ItemItemDb)
                , dict(_name=item_class_name, _child_name=child_class)
            )

            item_relations[item_relation] = item

            globals()[item_type_class_name_db] = item

        return item_relations

    def get_item_object_dbs(self, item_type, item_types=None):
        return self.create_item_objects

    def get_items(self, **params):
        depth = params.get('depth', self.MAX_DEPTH)
        result = params.get('result', [])
        item_type = params.get('item_type')
        item_id = params.get('item_id')
        item_data_object_list = params.get('item_data_object_list', dict())
        item_object_list = params.get('item_data_object_list', [])

        if item_type is None or item_id is None:
            return result

        code_identifier_exists = self._item_type_db.code_identifier_exist(item_type)

        if code_identifier_exists is False:
            return result

        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_db_name = item_type_class_name + 'ItemsDb'

        item_type_class_db_object = item_type_class_db_name(self._db)

        items = item_type_class_db_object.get_items_by_item_id(item_id)

        item_list = {}
        item_data_list = {}

        for item in items:
            pass

class ItemItemsDb(CoreTableDb):
    _parent_table_db = None
    _item_type_db = None
    _name = 'ItemItems'

    def _init_db(self):
        self._define_parent_table()
        self._define_item_type()
        self._define_table_name()
        self._define_fields()

    def _define_parent_table(self):
        self._get_parent_table()

    def _get_parent_table(self):
        if self._parent_table_db is None:
            name = self._get_name()
            parent_table_name = re.sub('Items$', 'Db', name)
            parent_table_db = globals()[parent_table_name](self._db)
            self._parent_table_db = parent_table_db

        return self._parent_table

    def _define_table_name(self):
        return self._get_table_name()

    def _define_fields(self):
        self._fields = [
            Field('item_id', self._parent_table_db.get_table())
            , Field('item_type_id', self._parent_table_db.get_table())
            , Field('sort_order', 'number')
            , Field('identifier', 'number')
        ]

    def get_items_by_item_id(self, item_id):
        condition = self._db(self.get_table_column('item_id')==item_id)
        items = self.get_all(condition)

        return items

class ItemDataDb(ItemItemsDb):
    _name = 'ItemData'

    def _get_parent_table(self):
        if self._parent_table is None:
            name = self._get_name()
            parent_table_name = re.sub('Data$', 'Db', name)
            parent_table_db = globals()[parent_table_name](self._db)
            self._parent_table_db = parent_table_db

        return self._parent_table

    def _define_fields(self):
        self._fields = [
            Field('item_id', self._parent_table_db.get_table())
            , Field('data', 'string')
            , Field('identifier', 'string')
        ]

class ItemItemDb(CoreTableDb):
    _items_db=None
    _child_db=None
    _name='Item'
    _child_name='Item'

    def _init_db(self):
        self._define_items_db()
        self._define_child_db()
        self._define_table_name()
        self._define_fields()

    def _define_items_db(self):
        parent_name = self._get_name()
        items_db_name = ''.join([parent_name, 'ItemsDb'])
        self._items_db = globals()[items_db_name](self._db)

    def _define_child_db(self):
        child_name = self._child_name
        child_db_name = ''.join([child_name, 'Db'])

        self._child_db = globals()[child_db_name](self._db)

    def _define_table_name(self):
        parent_name = self._get_name()
        self._table_name = ''.join([parent_name, child_name, 'Db'])

    def _define_fields(self):
        self._fields = [
            Field('items_id', self._items_db.get_table())
            , Field('child_item_id', self._child_db.get_table())
        ]

class ItemUtil(DataUtil):

    @staticmethod
    def item_to_form_data(item, **params):
        prefix = params.get('prefix')
        form_data = params.get('form_data', dict())
        item_form = params.get('item_form', dict())

        item_data = item.get('data')
        item_field = item.get('field')
        item_items = item.get('items')
        item_type = item.get('item')


        if (item_field is not None) and (len(item_field) > 0):
            for field_name, field in item_field.iteritems():
                prefixes = []
                if prefix is not None:
                    prefixes.append(prefix)
                prefixes.append(item_type)
                prefixes.append('field')
                prefixes.append(field_name)
                field_key = '-'.join(prefixes)
                form_data[field_key] = field.get('value', '')
                field_params = dict()
                field_params['item_id'] = field_key
                field_params['value'] = field.get('value', '')
                item_form[field_name] = field_params

        if (item_data is not None) and (len(item_data) > 0):
            for data_key, data in item_data.iteritems():
                data_field = data.get('field')
                prefixes = []
                if prefix is not None:
                    prefixes.append(prefix)
                prefixes.append(item_type)
                prefixes.append('data')
                prefixes.append(str(data_key))

                if (data_field is not None) and (len(data_field) > 0):
                    for field_name, field in data_field.iteritems():
                        prefixes.append('data')
                        prefixes.append('field')
                        prefixes.append(field_name)
                        field_key = '-'.join(prefixes)
                        form_data[field_key] = field.get('value', '')
                        field_params = dict()
                        field_params['item_id'] = field_key
                        field_params['value'] = field.get('value', '')
                        item_form['data_' + field_name] = field_params

        if item_items is not None:
            item_form['items'] = item_form.get('items', dict())
            item_form_items = item_form['items']

            for item_item_key, item_item in item_items.iteritems():
                item_item_type = item_item.get('item')
                prefixes = []
                if prefix is not None:
                    prefixes.append(prefix)

                prefixes.append(item_type)
                prefixes.append(item_item_type)
                prefixes.append(str(item_item_key))

                item_field_name = '-'.join(prefixes)

                item_params = dict(
                    prefix=item_field_name
                    , form_data=form_data
                )

                item_form_items[item_item_key] = item_form_items.get(item_item_key, dict())
                item_form_items_item = item_form_items[item_item_key]
                item_params['item_form'] = item_form_items_item

                ItemUtil.item_to_form_data(item_item, **item_params)

        return item_form#form_data

    @staticmethod
    def form_data_to_item(form_data, item_type_ids):
        part_depth = 3
        min_depth = 0
        item_format = {}
        orig_current_item = None
        special_fields = ['data', 'field']

        for name, value in form_data.iteritems():
            parts = name.split('-')
            parts_count = len(parts)
            max_depth = parts_count/part_depth

            current_item = item_format
            for depth_count in range(min_depth, max_depth):
                offset = (depth_count*part_depth)
                length = offset + part_depth
                element = parts[offset:length]
                sort_order = element[2]
                child_item = element[1]
                item = element[0]

                if orig_current_item is not None and child_item != 'field':
                        current_item = orig_current_item
                        orig_current_item = None

                if current_item.get(item) is None:
                        if item in item_type_ids:
                                current_item['item'] = item

                                current_item['item_type_id'] = item_type_ids[item]

                if child_item == 'data':
                        if  current_item.get('data') is None:
                                current_item['data'] = dict()

                        if  current_item['data'].get(sort_order) is None:
                                current_item['data'][sort_order] = dict()

                        if depth_count == (max_depth-1):
                                current_item['data'][sort_order]['value'] = value
                        else:
                                orig_current_item = current_item
                                current_item = current_item['data'][sort_order]
                elif child_item == 'field':
                        if  current_item.get('field') is None:
                                current_item['field'] = dict()

                        if  current_item['field'].get(sort_order) is None:
                                current_item['field'][sort_order] = dict()

                        if depth_count == (max_depth-1):
                                #print sort_order
                                #print current_item
                                current_item['field'][sort_order]['value'] = value

                        if orig_current_item is not None:
                                current_item = orig_current_item
                                orig_current_item = None

                else:
                        if current_item.get('items') is None:
                                current_item['items'] = {}


                        if current_item['items'].get(sort_order) is None:
                                current_item['items'][sort_order] = dict(
                                        item=child_item
                                        , sort_order=sort_order
                                        , parent_type=item
                                        , parent_type_id=item_type_ids[item]
                        )

                        if depth_count == (max_depth-1):
                                current_item['value'] = value
                        else:
                                current_item = current_item['items'][sort_order]


        return item_format

    @staticmethod
    def form_data_to_ui(form_data):

        return form_data

    @staticmethod
    def fill_dict_on_none(item, fields=[]):
        for field in fields:
            if item.get(field) is None:
                item[field] = dict()

            item = item[field]
