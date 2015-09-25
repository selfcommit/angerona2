from pyramid.response import Response
from pyramid.view import view_config

from angerona2 import DBSession
from angerona2.models.secret import Secret
from angerona2.controllers import (
    ViewController,
    SecretController,
    )

@view_config(route_name='api_secret', request_method='GET')
@view_config(route_name='api_secret:uuid', request_method='GET')
def api_secret_get(request):
    show_immediately = request.matchdict.get('data', False)

    return {}


@view_config(route_name='api_secret', request_method='POST')
def api_secret_post(request):
    return {}


@view_config(route_name='api_secret:uuid', request_method='DELETE')
def api_secret_delete(request):
    return {}
