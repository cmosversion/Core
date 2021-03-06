#!/usr/bin/env python
# coding: utf8
from gluon import *

#!/usr/bin/env python
# coding: utf8
from gluon import *

from core import Core

class CoreComponent(Core):
    pass

class HtmlComponent(CoreComponent):
    def get_html(self):
        raise NotImplementedError("get_html is not implemented in " + self.get_class(self))

class Page(CoreComponent):
    def _print(self):
        raise NotImplementedError("_print is not implemented in " + self.get_class(self))

class DataTable(CoreComponent):
    _response=None
    _request=None
    def __init__(self, request, response):
        self._request = request
        self._response = response
        self.datatable_include()

    def datatable_include(self):
        self._response.files.append(URL(r=self._request,c='static',f='plugin_datatable/jquery.dataTables.min.js'))
        self._response.files.append(URL(r=self._request,c='static',f='plugin_datatable/jquery.dataTables.css'))

    def create(self, rows, **attributes):
        if not '_class' in attributes:
            raise SyntaxError, "plugin_database needs a _class attribute"
        params = '';
        if '_params' in attributes:
            params = attributes['_params']

        return TAG[''](SCRIPT("jQuery(document).ready(function() {jQuery('.%s').dataTable(%s);});" % (attributes['_class'],params)),
                   SQLTABLE(rows,**attributes))
