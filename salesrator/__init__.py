from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from salesrator.a3user import groupfinder
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy('r4nd0m$3cr3tk3y', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='salesrator.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('signup', '/api/signup')
    config.add_route('login', '/api/login')
    config.add_route('loginsuccess', '/api/loginsuccess')
    config.add_route('operations','/api/operations')
    config.add_route('cleanup','/api/cleanup')
    config.add_route('plot','/api/plot')
    config.add_route('userdata', '/api/userdata')
    config.add_route('fileupload' ,'/api/fileupload')
    config.add_route('fileupdate', '/api/fileupdate')
    config.add_route('logout', '/logout')
    config.add_route('home', '/home')
    config.add_route('app', '/')
    config.scan()
    return config.make_wsgi_app()
