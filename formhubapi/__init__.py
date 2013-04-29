from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .models import (
    DBSession,
    Base,
    group_finder,
    UserFactory
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session_key'])
    authentication_policy = AuthTktAuthenticationPolicy(
        settings['auth_key'], callback=group_finder)
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    includeme(config)
    return config.make_wsgi_app()

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # url matched routes
    config.add_route('favicon', '/favicon.ico')
    # traversed routes
    config.add_route(
        'user', '/*traverse', factory=UserFactory)
    config.scan()