def plugin_datatable_include():
    response.files.append(URL(r=request,c='static',f='plugin_datatable/jquery.dataTables.min.js'))
    response.files.append(URL(r=request,c='static',f='plugin_datatable/jquery.dataTables.css'))

def plugin_datatable(rows,**attributes):
    if not '_class' in attributes:
        raise SyntaxError, "plugin_database needs a _class attribute"
    params = '';
    if '_params' in attributes:
        params = attributes['_params']
    return TAG[''](SCRIPT("jQuery(document).ready(function() {jQuery('.%s').dataTable(%s);});" % (attributes['_class'],params)),
                   SQLTABLE(rows,**attributes))

plugin_datatable_include()
