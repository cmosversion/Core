#!/usr/bin/env python
# coding: utf8
from gluon import *
from core_form import CoreForm

class TextDefinitionForm(CoreForm):
    def add_core_definition(self):
        self.add_field(Field('defintion', 'string', label=self.get_label(identifier='definition_label')))
