from pyramid.config import not_
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response

from sqlalchemy.exc import DBAPIError

from angerona2.utilities import ViewController
from angerona2 import DBSession
from angerona2.models.secret import Secret

conn_err_msg = """\
Pyramid is having a problem using your SQL database.
"""

@view_config(route_name='home', renderer='angerona2:templates/page_home.mako')
def page_home(request):
    try:
        one = DBSession.query(Secret).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    view = ViewController(request)
    return {'vc':view}


@view_config(route_name='secret', request_method=not_('POST'),
             renderer='angerona2:templates/page_secret.mako')
def page_secret_get(request):
    view = ViewController(request)
    return {'vc':view}


@view_config(route_name='secret', request_method='POST',
             renderer='angerona2:templates/page_secret_post.mako')
def page_secret_post(request):
    view = ViewController(request)
    return {'vc':view}