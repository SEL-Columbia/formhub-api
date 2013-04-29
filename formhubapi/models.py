from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Index,
    ForeignKey,
    desc,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from pyramid.security import (
    Allow,
    Deny,
    Everyone,
    Authenticated,
    ALL_PERMISSIONS,
    DENY_ALL,
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
class ModelBase(object):
    @classmethod
    def query(cls):
        return DBSession.query(cls)

    @classmethod
    def newest(cls, **kwargs):
        return cls.query().order_by(desc(by_field)).first()


Base = declarative_base(cls=ModelBase)


def group_finder(user_id, request):
    try:
        user = User.query().filter_by(id=user_id).one()
    except NoResultFound:
        pass
    else:
        groups = []#"g:%s" % g.name for g in user.groups]
        # add u: based permission
        groups.append('u:%d' % user.id)
        return groups
    return []


class UserFactory(object):
    __acl__ = [
        (Allow, "g:su", ALL_PERMISSIONS),
        ]
    __name__ = None
    __parent__ = None
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        try:
            user = User.query().filter_by(username=key).one()
        except NoResultFound as e:
            raise KeyError
        else:
            user.__parent__ = self
            user.__name__ = key
            return user

class FormFactory(object):
    def __getitem__(self, key):
        try:
            form = Form.query().filter_by(
                user=self.__parent__, id_string=key).one()
        except NoResultFound as e:
            raise KeyError
        else:
            form.__parent__ = self
            form.__name__ = key
            return form


class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String(128), nullable=False)
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    last_login = Column(DateTime)
    date_joined = Column(DateTime)
    factories = {'form': FormFactory}

    def __getitem__(self, key):
        factory = self.factories[key]()
        factory.__parent__ = self
        factory.__name__ = key
        return factory

    @property
    def __acl__(self):
        return [
            (Allow, 'u:%d' % self.id, 'view'),
            ]


class Form(Base):
    __tablename__ = 'odk_logger_xform'
    __table_args__ = (
        Index('odk_logger_xform_id_string_5f0b06be_uniq', 'id_string', 
        'user_id', unique=True),)
    id = Column(Integer, primary_key=True)
    downloadable = Column(Boolean)
    user_id = Column(
        Integer, ForeignKey('auth_user.id'), nullable=False, index=True)
    user = relationship(
        'User', backref=backref('forms', cascade="all, delete-orphan"))
    id_string = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    shared = Column(Boolean)
    has_start_time = Column(Boolean)
    description = Column(String(255), nullable=True)
    shared_data = Column(Boolean)
    uuid = Column(String(255))
    is_crowd_form = Column(Boolean)
    bamboo_dataset = Column(String(255), nullable=True)
    _sdf = Column(Text, nullable=True)

    def __json__(self, request):
        return {
            'id_string': self.id_string,
            'title': self.title,
            'date_created': self.date_created.isoformat(),
            'date_modified': self.date_modified.isoformat(),
            'shared': self.shared,
            'has_start_time': self.has_start_time,
            'description': self.description,
            'shared_data': self.shared_data,
            'is_crowd_form': self.is_crowd_form,
            'bamboo_dataset': self.bamboo_dataset,
            'sdf_schema': self._sdf
        }