from __future__ import division

import logging
import datetime

from pyramid.response import Response
from pyramid.view import view_config

from angerona2 import DBSession
from angerona2.models.secret import Secret
from angerona2.controllers import (
    ViewController,
    SecretController,
    )

from sqlalchemy.exc import DBAPIError
from angerona2 import DBSession
from angerona2.models.secret import Secret


logger = logging.getLogger('pages')


@view_config(route_name='home', renderer='angerona2:templates/page_home.mako')
def page_home(request):
    try:
        one = DBSession.query(Secret).first()
    except DBAPIError:
        return Response('Pyramid is having a problem using your SQL database.',
                        content_type='text/plain', status_int=500)

    return {'vc':ViewController.ViewController(request)}


@view_config(route_name='secret', request_method='GET',
             renderer='angerona2:templates/page_secret.mako')
def page_secret_get(request):
    return {'vc':ViewController.ViewController(request)}


@view_config(route_name='retrieve', request_method='GET',
             renderer='angerona2:templates/page_retieve.mako')
def page_retrieve_get(request):
    show_immediately = request.matchdict.get('show', False)

    return {'vc':ViewController.ViewController(request)}


@view_config(route_name='secret', request_method='POST',
             renderer='angerona2:templates/page_secret_post.mako')
def page_secret_post(request):
    sc = SecretController.SecretController()

    try:
        expiry = sc.is_inrangeor(val=request.POST['hours_until_expiration'],
                                 rmin=1, rmax=168, become=4)
        numviews = sc.is_inrangeor(val=request.POST['maximum_views'],
                                   rmin=-1, rmax=100, become=2)
        syntype = sc.is_supportedtype(val=request.POST['snippet_type'])
        data = bytes(request.POST['data'], encoding='utf-8')
    except ValueError:
        # invalid form (no data to save was given)
        return HTTPFound(location=request.route_url('error'))

    # parse our checkbox if it is there (flip logic)
    early_delete = 'disallow_early_delete' not in request.POST

    friendly_time = '{} day(s) {} hour(s)'.format(expiry // 24, expiry % 24)
    expiry = datetime.datetime.now() + datetime.timedelta(hours=expiry)

    secret, uuid = sc.create_secret(expiry_time=expiry, lifetime_reads=numviews,
                     snippet_type=syntype, early_delete=early_delete,
                     plaintext=data)

    DBSession.add(secret)
    DBSession.flush()

    if secret.flag_unlimited_reads:
        friendly_clicks = 'unlimited'
    else:
        friendly_clicks = numviews

    return {
        'vc':ViewController.ViewController(request),
        'uuid':uuid, 
        'friendly_time': friendly_time,
        'friendly_clicks': friendly_clicks,
        'friendly_delete': not secret.flag_delete_early
    }

