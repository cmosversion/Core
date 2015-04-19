#!/usr/bin/env python
# coding: utf8
from gluon import *

from applications.Core.modules.item_db import ItemDb

from applications.Core.modules.core_component import CoreComponent

class PlanComponent(CoreComponent):

    _template = None
    _form = None
    _item_db = None
    _item_type_objects = None

    def __init__(self, db, request, response):
        self._item_db = ItemDb(db)

    def __get_plan_item_types(self):
        self._item_types_objects = self._item_db.get_item_objects('plan')

    def get_template(self):
        if self._template is None:
            return dict(
                html='plan/default.html'
                , html_list='plan/default_list.html'
                , css='/Plan/static/css/plan/default.css'
                , js='/Plan/static/js/plan/default.js'
            )

        return self._template

    def get_data(self):
        return None

    def get_control(self):
        return None

    def get_errors(self):
        return None
