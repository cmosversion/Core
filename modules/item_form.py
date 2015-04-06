#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_form import CoreForm

class ItemForm(CoreForm):
    def add_core_item_id(self):
        self.add_field_with_label('item_id', 'integer')

    def add_core_item(self):
        self.add_field_with_label('item', 'string')

    def add_core_item(self):
        self.add_field_with_label('description', 'string')

    def add_core_version(self):
        self.add_field_with_label('version', 'number')

    def add_core_revision(self):
        self.add_field_with_label('revision', 'number')

    def add_core_version_id(self):
        self.add_field_with_label('version_id', 'number')

    def add_core_item_type_id(self):
        self.add_field_with_label('item_type_id', 'number')

    def add_core_version(self):
        self.add_field_with_label('lt', 'number')

    def add_core_revision(self):
        self.add_field_with_label('rt', 'number')

    def add_core_created_on(self):
        self.add_field_with_label('created_on', 'datetime')

    def add_core_updated_on(self):
        self.add_field_with_label('updated_on', 'datetime')

    def add_core_deleted_on(self):
        self.add_field_with_label('deleted_on', 'datetime')

class ItemItemsForm(CoreForm):
    def add_core_item_items_id(self):
        self.add_field_with_label('item_items_id', 'integer')

    def add_core_item_id(self):
        self.add_field_with_label('item_id', 'integer')

    def add_core_item_type_id(self):
        self.add_field_with_label('item_type_id', 'integer')

    def add_core_sort_order(self):
        self.add_field_with_label('sort_order', 'integer')

    def add_core_identifier(self):
        self.add_field_with_label('identifier', 'string')

class ItemDataForm(CoreForm):
    def add_core_item_data_id(self):
        self.add_field_with_label('item_data_id', 'integer')

    def add_core_item_id(self):
        self.add_field_with_label('item_id', 'integer')

    def add_core_sort_order(self):
        self.add_field_with_label('data', 'string')

    def add_core_identifier(self):
        self.add_field_with_label('identifier', 'string')
