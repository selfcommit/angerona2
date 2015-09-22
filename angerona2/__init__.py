import angerona2.models
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.decorator import reify
from sqlalchemy import engine_from_config
from uuid import uuid4

from .utilities import hack_thread_name_tween_factory

from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyRequest(Request):
    @reify
    def id(self):
        return str(uuid4())


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.set_request_factory(MyRequest)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('secret', '/secret')
    config.add_route('api_secret', '/v1/secret')

    config.add_tween('angerona2.utilities.hack_thread_name_tween_factory')
    config.scan()
    return config.make_wsgi_app()

