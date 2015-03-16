# coding: utf8
# try something like
response.debug = dict(ab='1')
def index():
    if hasattr(request.vars, 'flash'):
        response.flash = request.vars.flash

    form = __get_text_manager_form()
    __process_text_manager(form)

    from text_component import TextIdentifierComponent
    from text_component import TextDefinitionComponent
    from text_component import TextDefinitionIdentifierComponent

    identifier_db = text_manager.get_identifier_db()
    definition_db = text_manager.get_definition_db()
    definition_identifier_db = text_manager.get_definition_identifier_db()
    #db(db.text_definition_identifier.id>0).delete()
    identifier_component = TextIdentifierComponent(identifier_db, request, response, text_manager=text_manager)
    definition_component = TextDefinitionComponent(definition_db, request, response, text_manager=text_manager)
    definition_identifier_component = TextDefinitionIdentifierComponent(definition_identifier_db, request, response, text_manager=text_manager)

    identifier_table = identifier_component.get_datatable()
    definition_table = definition_component.get_datatable()
    definition_identifier_table = definition_identifier_component.get_datatable()

    form_data = __get_form_data(form)#form.vars
    response.debug = form.vars#__get_form_data(form)

    resource = text_manager.get_identifier_db().RESOURCE_SEPARATOR.join([request.application, request.controller, 'index'])

    page_title = text_manager.getText(resource, 'page_title')
    definition_identifier_table_title = text_manager.getText(resource, 'definition_identifier_table_title')
    table_title = text_manager.getText(resource, 'definition_identifier_title')
    definition_table_title = text_manager.getText(resource, 'definition_table_title')
    identifier_table_title = text_manager.getText(resource, 'identifier_table_title')

    response.title = page_title

    return dict(
        definition_identifier_table=definition_identifier_table
        , definition_table=definition_table
        , identifier_table=identifier_table
        , form=form
        , form_data=form_data
        , table_title=table_title
        , definition_table_title=definition_table_title
        , identifier_table_title=identifier_table_title
        , definition_identifier_table_title=definition_identifier_table_title
    )

def delete_selected_identifier_ids():
    resource = __get_text_manager_resource()
    delete_message = text_manager.getText(resource, 'delete_selected_identifier_succeed')
    delete_identifier_by_id(delete_message)

def delete_selected_definition_ids():
    resource = __get_text_manager_resource()
    delete_message = text_manager.getText(resource, 'delete_selected_definition_succeed')
    delete_definition_by_id(delete_message)

def delete_definition_by_id():
    delete_definition_by_id(None)

def delete_definition_by_id(flash=None):
    if hasattr(request.vars, 'definition_id'):
        if CoreUtil.is_integer(request.vars.definition_id) or isinstance(request.vars.definition_id, list):
            result = text_manager.get_definition_db().delete_definition_by_id(request.vars.definition_id)
            if flash==None:
                resource = __get_text_manager_resource()
                flash=text_manager.getText(resource, 'delete_definition_succeed')
            redirect (URL(f='index', vars=dict(flash=flash)))
    redirect(URL(f='index'))

def delete_identifier_by_id():
    delete_identifier_by_id(None)

def delete_identifier_by_id(flash=None):
    if hasattr(request.vars, 'identifier_id'):
        if CoreUtil.is_integer(request.vars.identifier_id) or isinstance(request.vars.identifier_id, list):
            result = text_manager.get_identifier_db().delete_identifier_by_id(request.vars.identifier_id)
            if flash==None:
                resource = __get_text_manager_resource()
                flash=text_manager.getText(resource, 'delete_identifier_succeed')
            redirect (URL(f='index', vars=dict(flash=flash)))
    redirect(URL(f='index'))


def delete_selected_definition_identifier_by_ids():
     resource = __get_text_manager_resource()
     flash = text_manager.getText(resource, 'delete_selected_definition_identifier_succeed')
     delete_definition_identifier_by_id(flash)

def delete_definition_identifier_by_id():
    delete_definition_identifier_by_id(None)

def delete_definition_identifier_by_id(flash=None):

    if hasattr(request.vars, 'definition_id'):
        if CoreUtil.is_integer(request.vars.definition_id) or isinstance(request.vars.definition_id, list):
            result = text_manager.delete_definition_assignment(request.vars.definition_id, None)
            if flash == None:
                resource = __get_text_manager_resource()
                flash = text_manager.getText(resource, 'delete_definition_identifier_succeed')
            redirect (URL(f='index', vars=dict(flash=flash)))
    redirect(URL(f='index', flash=dict(flash=vars(request.vars))))


def unassign_identifier():
    if hasattr(request.vars, 'identifier_id'):
        if CoreUtil.is_integer(request.vars.identifier_id):
            result = text_manager.reassign_identifier(request.vars.identifier_id)
            flash="Identifier successfully unassigned"
            redirect (URL(f='index', vars=dict(flash=flash)))
    redirect(URL(f='index'))

#
# Helpers
#
def __get_text_manager_resource():
    return text_manager.get_identifier_db().RESOURCE_SEPARATOR.join([request.application, request.controller, 'index'])

def __get_resource(form):
    a = form.vars.application
    c = form.vars.controller
    f = form.vars.function
    return a + '___' + c + '___' + f

def __process_text_manager(form):

    if form.process().accepted:
        a = form.vars.get('application')
        c = form.vars.get('controller')
        f = form.vars.get('function')
        i = form.vars.get('identifier')
        d = form.vars.get('definition')

        r = __get_resource(form)

        identifier_filled = (a != None and a != '' and c != None and c != '' and f != None and f != '' and i != None and i != '')
        definition_filled = (d != None and d != '')
        all_filled = (
            identifier_filled
            and
            definition_filled
        )

        if all_filled:
            text_manager.get_definition_identifier_db().add_definition_identifier(d, r, i)
        elif definition_filled:
            response.debug = str(text_manager.get_definition_db().add_definition(d))
        elif identifier_filled:
            response.debug = str(text_manager.get_identifier_db().add_basic_identifier(a,c,f,i))

        response.flash = 'Successfully added'
    elif form.errors:
        response.flash = 'form has errors'

def __get_text_manager_form():
    return SQLFORM.factory(
         text_manager.get_definition_db().get_table()
        , Field('application', 'string', default='abc')
        , Field('controller', 'string', default='')
        , Field('function', 'string', default='')
        , Field('identifier', 'string', default='')
    )

    return False

def __get_form_data(form):
    from gluon.storage import Storage

    form_data = dict()
    for field in form.fields:
        form_data[field] = form.vars.get(field, '')
    return Storage(form_data)

def __text_manager_include():
    response.files.append(URL(r=request,c='static',f='js/text_manager/index.js'))

__text_manager_include()
