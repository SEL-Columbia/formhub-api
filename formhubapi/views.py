from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    Form
    )


@view_config(context=User, route_name='user', name='forms',
             renderer='json')
def forms(request):
    user = request.context
    return {'forms': user.forms}


@view_config(context=Form, route_name='user', name='',
             renderer='json')
def form(request):
    form = request.context
    return {'form': form}