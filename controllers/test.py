# coding: utf8
# try something like
def index(): return dict(message="hello from test.py")

def item():
    response.files.insert(4, '/Plan/static/css/plan/default.css')
    from item_db import ItemDb
    from item_db import ItemUtil

    names = {
        'plan-field-item':'Plan'
        , 'plan-title-1-title-field-item':'(Title)'
        , 'plan-goals-2-goals-field-item':'Goals'
        , 'plan-goals-2-goals-goal-1-goal-field-item':'Goal'
        , 'plan-goals-2-goals-goal-1-goal-objectives-1-objectives-field-item':'Objectives'
        , 'plan-goals-2-goals-goal-1-goal-objectives-1-objectives-objective-1-objective-data-1-data-field-data':''
        , 'plan-goals-2-goals-goal-1-goal-objectives-1-objectives-objective-2-objective-data-1-data-field-data':''
    }


    item_type_ids = {'item':1,'plan':2,'goals':4,'goal':5,'objectives':6,'objective':7,'title':8}
    html_data = ItemUtil.form_data_to_item(names, item_type_ids)
    html_data = ItemUtil.item_to_form_data(html_data)
    return dict(items={}, html_data=html_data)
