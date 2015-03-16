#!/usr/bin/env python
# coding: utf8
from gluon import *

class CoreUtil(object):
    @staticmethod
    def is_int(int_value):
        return isinstance(int_value, int)

    @staticmethod
    def is_str(str_value):
        return isinstance(str_value, str)

    @staticmethod
    def is_integer(int_value):
        if CoreUtil.is_int(int_value):
            return True
        if CoreUtil.is_str(int_value):
            return int_value.isdigit()

        return False

    @staticmethod
    def get_class(obj):
        return type(obj).__name__

class DataUtil(CoreUtil):

    def int_to_list(self, int_value):
        if self.is_integer(int_value):
            return [int_value]
        return int_value

    def get_valid_table_name_message(self):
        return 'Table name must start in alphabet or underscore followed by alphanumeric or underscore'

    def is_valid_table_name(self, table_name):
        return True
