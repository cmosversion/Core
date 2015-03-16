#!/usr/bin/env python
# coding: utf8
from gluon import *

from core_db import CoreDb
from component import Component
from component import DataTable
from text_db import TextIdentifierDb
from text_db import TextDefinitionDb
from text_db import TextDefinitionIdentifierDb
from text_db import TIDb

class TextComponent(Component):
    _class = None
    _width = None
    _text_db = None
    _request = None
    _response = None
    _resource = 'Core___text_manager___index'
    _text_manager = None
    _form = None

    def __init__(self, text_db, request, response, **params):
        self.set_text_db(text_db)
        self.set_request(request)
        self.set_response(response)
        self.set_resource(**params)
        self.validate()
        self._init_text_manager(**params)

    def validate(self):
        raise NotImplementedError(self.get_class(self) + " must implement a validate method")

    def set_request(self, request):
        self._request = request
    def set_response(self, response):
        self._response = response
    def set_text_db(self, text_db):
        self._text_db = text_db
    def set_resource(self, **params):
        resource = params.get('resource')
        if resource != None:
            self._resource = resource
    def _init_text_manager(self, **params):
        text_manager = params.get('text_manager')

        if isinstance(text_manager, TIDb):
            self._text_manager = text_manager
            return

        self._text_manager = TIDb(self._text_db.getDb(), self._resource)

    def get_datatable(self):
        raise NotImplementedError(self.get_class(self) + " must implement a get_datatable method")

    def _get_delete_link(self, f, params, confirm_message):
        return A(
            XML(I(_class="fa fa-trash-o fa-fw", _style="color:red"))
            , _onclick='return confirm("' + confirm_message + '")', _href=URL(f=f, vars=params)
        )

    def _get_delete_all_selected_link(self, f, confirm_message, no_selected_message, name):
        process_select = no_selected_message.join([
            'if (! TextManagerIndexJs.actions.processSelected(this)){alert("'
            , '"); return false;};'
        ])

        confirmation = ' if (confirm("' + confirm_message + '")) { location = $(this).attr("href");} return false;'
        click_process = process_select + confirmation

        return A(
            XML(I(_class="fa fa-trash-o fa-fw", _style="color:red"))
            , _href=URL(f=f)
            , _onclick=click_process
            , _name=name
        )

    def get_text_definition(self, identifier):
        return self._text_manager.getText(self._resource, identifier)

    def get_datatable(self):
        headers = self.get_headers()
        record = self.get_record()
        options = self.get_options()
        extra_columns = self.get_extra_columns()

        datatable = DataTable(self._request, self._response).create(
            record
            , headers=headers
            , extracolumns=extra_columns
            , _class=self._class, _style='width:' + str (self._width) + '%', _id=self._class + '_id'
            , _params=options
        )

        return datatable

    def get_headers(self):
        raise NotImplementedError(self.get_class(self) + " must implement a get_headers method")

    def get_record(self):
        raise NotImplementedError(self.get_class(self) + " must implement a get_record method")

    def get_options(self):
        raise NotImplementedError(self.get_class(self) + " must implement a get_options method")

    def get_extra_columns(self):
        raise NotImplementedError(self.get_class(self) + " must implement a get_extra_coulumns method")

class TextDefinitionIdentifierComponent(TextComponent):
    _class = 'text_definition_identifier'
    _width = 100

    def validate(self):
        if not isinstance(self._text_db, TextDefinitionIdentifierDb):
            identifier_db = TextDefinitionIdentifierDb(CoreDb().getDb())
            self.set_text_db(identifier_db)

    def get_record(self):
        query = self._text_manager.get_all_definition()

        text_definition_id = self._text_manager.get_definition_db().get_text_definition_id()
        text_definition = self._text_manager.get_definition_db().get_text_definition()
        text_definition_uid = self._text_manager.get_definition_db().get_text_definition_uid()

        record_fields = (text_definition_id, text_definition, text_definition_uid)

        record = query.select(*record_fields, distinct=True)

        return record

    def get_headers(self):
        return {
            'text_definition.id':{'label':'ID', 'width':'10%', 'class':'hidden', 'truncate': 100, 'selected':False}
            , 'text_definition.definition':{'label':'Definition', 'width':'88%;', 'class':'definitions_header', 'truncate':500, 'selected':False}
            , 'text_definition.i_uid':{'label':'Unique Identifier', 'width':'5%', 'class':'hidden', 'truncate': 100, 'selected':False}
        }

    def get_options(self):
        return "{\"aoColumns\": [{\"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": false }]}"

    def get_extra_columns(self):
        confirm_message = self.get_text_definition('confirm_delete_definition_identifier')
        no_selected_message = self.get_text_definition('select_definition_identifier')
        f = 'delete_selected_definition_identifier_by_ids'

        identifier_column = {
            'label':'Identifier', 'class': 'identifier_td', 'width':'40%', 'selected':False
            , 'content': lambda row, rc: self.__get_row_text(row)
        }

        identifier_header = XML(
            DIV(
                (
                    self._get_delete_all_selected_link(f, confirm_message, no_selected_message, 'definition_id')
                    + INPUT(_name='definition_id', _value='all', _type='checkbox', _onclick="TextManagerIndexJs.actions.selectAll(this);")
               )
               , _style="width:60px;"
            )
        )

        return [
            identifier_column
            , {
                'label': identifier_header
                , 'class': 'identifier_actions', 'width':'5%', 'selected':False
                , 'content': lambda row, rc:
                    self._get_delete_link(
                        'delete_definition_identifier_by_id'
                        , dict(definition_id=row.id)
                        , confirm_message
                    )
                    + INPUT(_name='definition_id_'+  str(row.id), _value=row.id, _type='checkbox')
            }
        ]

    def __get_row_text(self, row):
        r = []

        identifier_definition = self._text_manager.get_definition_identifier_db().get_identifier_aff()
        identifier_row = (self._text_manager.get_definition_identifier_db().get_text_definition_id()==row.id)
        resource = self._text_manager.get_identifier_db().get_text_resource()
        identifier = self._text_manager.get_identifier_db().get_text_identifier()
        identifier_id = self._text_manager.get_identifier_db().get_text_identifier_id()

        confirm_message = self.get_text_definition('unassign_identifier')

        f = 'unassign_identifier'
        db = self._text_manager.getDb()
        query = (identifier_definition & identifier_row)
        for dr in db(query).select(resource, identifier, identifier_id):
            params = dict(identifier_id=dr.id)
            r.append(A(
                XML('<i class="fa fa-times  fa-fw" style="color:red"></i>' + '.'.join([dr.i_resource, dr.i_identifier])), _style="margin-left:5px;"
                , _onclick='return confirm("' + confirm_message + '")', _href=URL(f=f, vars=params)
            ))

        return r

# Text Identifier Component
#
class TextIdentifierComponent(TextComponent):
    _class = 'text_identifier'
    _width = 100

    def validate(self):
        if not isinstance(self._text_db, TextIdentifierDb):
            identifier_db = TextIdentifierDb(CoreDb().getDb())
            self.set_text_db(identifier_db)

    def get_record(self):
        return self._text_db.get_all()

    def get_headers(self):
        return {
            'text_identifier.id':{'label':'ID', 'width':'5%', 'class':'hidden', 'truncate': 100, 'selected':False}
            , 'text_identifier.i_resource':{'label':'Resource', 'width':'50%', 'class':'test', 'truncate':100, 'selected':False}
            , 'text_identifier.i_identifier':{'label':'Identifier', 'width':'40%', 'class':'test', 'truncate': 100, 'selected':False}
            , 'text_identifier.i_uid':{'label':'Unique Identifier', 'width':'5%', 'class':'hidden', 'truncate': 100, 'selected':False}
        }

    def get_options(self):
         return "{\"aoColumns\": [{\"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": false }]}"

    def get_extra_columns(self):
        confirm_message = self.get_text_definition('confirm_delete_identifier')
        no_selected_message = self.get_text_definition('select_identifier')
        f = 'delete_selected_identifier_ids'
        return [
            {
                'label': XML(
                    DIV(
                        (
                            self._get_delete_all_selected_link(f, confirm_message, no_selected_message, 'identifier_id')
                            + I(_class="fa fa-pencil fa-fw", _style="color:white")
                            + INPUT(_name='identifier_id', _value='all', _type='checkbox', _onclick="TextManagerIndexJs.actions.selectAll(this);")
                        )
                        , _style="width:60px;" 
                    )
                )
                , 'class': 'identifier_actions no-sort', 'width':'12%', 'selected':False
                , 'content': lambda row, rc:
                    self._get_delete_link(
                        'delete_identifier_by_id'
                        , dict(identifier_id=row.id)
                        , confirm_message
                    )
                    + I(_class="fa fa-pencil fa-fw", _style="color:blue")
                    + INPUT(_name='identifier_id_' + str(row.id), _value=row.id, _type='checkbox')
            }
        ]


class TextDefinitionComponent(TextComponent):
    _class = 'text_definition'
    _width = 100

    def validate(self):
        if not isinstance(self._text_db, TextDefinitionDb):
            definition_db = TextDefinitionDb(CoreDb().getDb())
            self.set_text_db(definition_db)

    def get_record(self):
        return self._text_db.get_all()

    def get_headers(self):
        return {
            'text_definition.id':{'label':'ID', 'width':'10%', 'class':'hidden', 'truncate': 100, 'selected':False}
            , 'text_definition.definition':{'label':'Definition', 'width':'88%;', 'class':'definitions_header', 'truncate':500, 'selected':False}
            , 'text_definition.i_uid':{'label':'Unique Identifier', 'width':'5%', 'class':'hidden', 'truncate': 100, 'selected':False}
        }
    def get_options(self):
        return "{\"aoColumns\": [{\"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": true },{ \"bSortable\": false }]}"

    def get_extra_columns(self):
        confirm_message = self.get_text_definition('confirm_delete_definition')
        no_selected_message = self.get_text_definition('select_definition')

        f = 'delete_selected_definition_ids'
        return [
            {
                'label': XML(
                    DIV(
                        (
                            self._get_delete_all_selected_link(f, confirm_message, no_selected_message, 'definition_id')
                            + I(_class="fa fa-pencil fa-fw", _style="color:white")
                            + INPUT(_name='definition_id', _value='all', _type='checkbox', _onclick="TextManagerIndexJs.actions.selectAll(this);")
                        )
                        , _style="width:60px;" 
                    )
                )
                , 'class': 'identifier_actions', 'width':'12%;', 'selected':False
                , 'content': lambda row, rc:
                    self._get_delete_link(
                        'delete_definition_by_id'
                        , dict(definition_id=row.id)
                        , confirm_message
                    )
                    + I(_class="fa fa-pencil fa-fw", _style="color:blue")
                    + INPUT(_name='definition_id_' + str(row.id), _value=row.id, _type='checkbox')
            }
        ]
