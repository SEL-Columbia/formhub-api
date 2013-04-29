from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPForbidden,
    HTTPUnauthorized,
    )
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    Form
    )


@view_config(context=HTTPForbidden)
def basic_challenge(request):
    response = HTTPUnauthorized()
    response.headers.update(forget(request))
    return response


@view_config(route_name='logout')
def logout(request):
    response = Response("Logged out")
    response.headers.update(forget(request))
    return response


@view_config(context=User, route_name='user', name='forms',
             renderer='json', permission='view')
def forms(request):
    user = request.context
    return {'forms': user.forms}


@view_config(context=Form, route_name='user', name='',
             renderer='json', permission='view')
def form(request):
    form = request.context
    return {'form': form}