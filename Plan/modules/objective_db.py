#!/usr/bin/env python
# coding: utf8
from gluon import *

from applications.Core.modules.item_db import ItemDb
from applications.Core.modules.item_db import ItemItemsDb
from applications.Core.modules.item_db import ItemDataDb
from applications.Core.modules.item_db import ItemItemDb

class ObjectivesDb(ItemDb):
    _name = 'Objectives'

class ObjectivesItemsDb(ItemItemsDb):
    _name = 'ObjectivesItems'

class ObjectivesDataDb(ItemDataDb):
    _name = 'ObjectivesData'

class ObjectivesItemDb(ItemItemDb):
    _name = 'Objectives'
    _child_name = 'Item'

class ObjectivesObjectiveDb(ItemItemDb):
    _name = 'Objectives'
    _child_name = 'Objective'


class ObjectiveDb(ItemDb):
    _name = 'Objective'

class ObjectiveItemsDb(ItemItemsDb):
    _name = 'ObjectiveItems'

class ObjectiveDataDb(ItemDataDb):
    _name = 'ObjectiveData'

class ObjectiveItemDb(ItemItemDb):
    _name = 'Objective'
    _child_name = 'Item'
