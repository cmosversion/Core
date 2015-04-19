#!/usr/bin/env python
# coding: utf8
from gluon import *

from applications.Core.modules.item_db import ItemDb
from applications.Core.modules.item_db import ItemItemsDb
from applications.Core.modules.item_db import ItemDataDb
from applications.Core.modules.item_db import ItemItemDb

class GoalDb(ItemDb):
    _name = 'Goal'

class GoalItemsDb(ItemItemsDb):
    _name = 'GoalItems'

class GoalDataDb(ItemDataDb):
    _name = 'PlanData'

class GoalItemDb(ItemItemDb):
    _name = 'Plan'
    _child_name = 'Item'

class GoalObjectivesDb(ItemItemDb):
    _name = 'Plan'
    _child_name = 'Objectives'
