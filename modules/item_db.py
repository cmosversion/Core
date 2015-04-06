#!/usr/bin/env python
# coding: utf8
from gluon import *
import re

from core_db import CoreTableDb
from codetable_db import CodeTableDb

class ItemTypeCodeDb(CodeTableDb):
    _table_name = 'item_type_code'


class ItemDb(CoreTableDb):
    _name = 'Item'
    _item_type_db = None
    _items_db = None
    _items_type_db = dict()

    def _init_db(self):
        self._define_table_name()
        self._define_item_type()
        self._define_fields()
        self._define_items()


    def _define_item_type(self):
        item_type_name = ItemTypeCodeDb(self._db)
        self._item_type_db = item_type_name

    def _init_table(self):
        self._define_default_item_types()

    def _define_default_item_types(self):

        item_types = self._get_default_item_types()

        for item_index, item_type in item_types:
            self.save(item_type)

    def _get_default_item_types(self):
        code = self._get_name()
        code_identifier = self.camel_case_to_underscore(code)

        item_types = dict(
            dict(code_key=code, code_translation=code, code_identifier=code_identifier)
        )

        return item_types

    def _define_table_name(self):
        return self._get_table_name()

    def _define_items(self):
        if self._items_db is None:
            item_name = self._get_name()
            item_items_name = item_name + 'ItemsDb'
            self._items_db = globals()[item_items_name](self._db)

    def _define_fields(self):
        self._fields = [
            Field('item', 'string')
            , Field('description', 'string')
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

        def inter_item(self, data):
            pass

        def save(self, item):
            items = item.get('items')

            if items is not None:
                del item['items']

            parent_item_id = item.get('parent_item_id')
            parent_item_type_id = item.get('parent_item_type_id')

            if parent_item_id is not None:
                del item['parent_item_id']

            item_id = item.get('item_id')
            item_type_id = item.get('item_type_id')
            condition = self._db(self._item_type_db.get_table_column('id').belongs(item_type_id))
            item_type = self._item_type_db.get_one(fields=['code_identifier'], condition=condition)
            item_class = self.underscore_to_camel_case(item_type) + 'Db'

            if item_id is None:
                item_id = super(globals()[item_class], self).save(item)
            else:
                item_id = super(globals()[item_class], self).save(item, (self.get_table_column('id')==item_id))

            if parent_item_id is not None:
                items_condition = self._db(
                    (self._items_db.get_column('item_id')==parent_item_condition)
                    &
                    (self._items_db.get_column('sort_order')==item.get('sort_order'))
                )

                data = dict(
                    item_id=parent_item_id
                    , sort_order=item.get('sort_order')
                    , item_type_id=item_type_id
                )

                condition = self._db(self._item_type_db.get_table_column('id').belongs(parent_item_type_id))
                parent_item_type = self._item_type_db.get_one(fields=['code_identifier'], condition=condition)
                parent_item_name = parent_item_type
                parent_items_class = self.underscore_to_camel_case(item_type) + 'ItemsDb'
                parent_items_db = globals()[parent_item_class](self._db)

                parent_items_id = parent_items_db.save(data, condition=items_condition)

                class_ = string.__class__
                parent_child_item_name = class_.join('_', [parent_item_name, item_name])
                parent_child_item_class = self.underscore_to_camel_case(parent_child_item_name)
                parent_child_item_db = globals()[parent_child_item_class](self._db)

                data = dict(items_id=parent_items_id, child_item_id=item_id)
                condition = self._db(parent_child_item_db.get_table_column('items_id')==parent_items_id)

                parent_child_item_db.save(data, condition)

            for item in items:
                    self.save(item)
    def create_item_objects(self, item_type):
        item_object = self.create_item_object(item_type)
        item_items = self.create_item_items(item_type)
        item_data = self.create_item_data(item_type)
        item_relations = self.create_item_relations(item_type)

        item_objects = dict(
            item=item_object
            , item_items=item_items
            , item_data=item_data
            , item_relations=item_relations
        )

        return item_objects

    def create_item_object(self, item_type):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_db_name = item_type_class_name + 'Db'
        item = type(item_type_class_name, (ItemDb), dict(_name=item_type_class_name))

        return item

    def create_item_items(self, item_type):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_db_name = item_type_class_name + 'ItemsDb'
        item = type(item_type_class_name, (ItemItemsDb), dict(_name=item_type_class_name))

        return item

    def create_item_data(self, fields):
        item_type_class_name = self.underscore_to_came_case(item_type)
        item_type_class_db_name = item_type_class_name + 'DataDb'
        item = type(item_type_class_name, (ItemItemsDb), dict(_name=item_type_class_name))

        return item

    def create_item_relations(self, item, item_types=None):
        if item_types is None:
            item_types = self._item_type_db.get_all()

        item_relations = {}

        for item_type in item_types:
            item_relation = item + '_' + item_type
            child_class = self.underscore_to_camel_case(item_type)
            item_class_name = self.underscore_to_came_case(item_relation + '_db')

            item_realations[item_relation] = type(
                item_type_class_name
                , (ItemItemDb)
                , dict(_name=item_type_class_name, _child_name=child_class)
            )

        return item_relations

    def get_item_objects(self, item_type):
        return self.create_item_objects

class ItemItemsDb(CoreTableDb):
    _parent_table_db = None
    _item_type_db = None
    _name = 'ItemItems'

    def _init_db(self):
        self._define_parent_table()
        self._define_item_type()
        self._define_table_name()
        self._define_fields()

    def _define_parent_table(sef):
        self._get_parent_table()

    def _get_parent_table(self):
        if self._parent_table is None:
            name = self._get_name()
            parent_table_name = re.sub('/Items$/', 'Db', name)
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


class ItemDataDb(ItemItemsDb):
    _name = 'ItemData'

    def _get_parent_table(self):
        if self._parent_table is None:
            name = self._get_name()
            parent_table_name = re.sub('/Data$/', 'Db', name)
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
        class_ = string.__class__
        parent_name = self._get_name()
        items_db_name = class_.join('', [parent_name, 'ItemsDb'])
        self._items_db = globals()[items_db_name](self._db)

    def _define_child_db(self):
        class_ = string.__class__
        child_name = self._child_name
        child_db_name = class_.join('', [child_name, 'Db'])

        self._child_db = globals()[child_db_name](self._db)

    def _define_table_name(self):
        class_ = string.__class__
        parent_name = self._get_name()
        self._table_name = class_.join('', [parent_name, child_name, 'Db'])

    def _define_fields(self):
        self._fields = [
            Field('items_id', self._items_db.get_table())
            , Field('child_item_id', self._child_db.get_table())
        ]
