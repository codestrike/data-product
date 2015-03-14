import hashlib
from datetime import datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

SIZE_255 = 255

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=SIZE_255)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(SIZE_255))
    email = Column(String(SIZE_255))
    passhash = Column(String(SIZE_255), nullable=True)
    u3id = Column(String(SIZE_255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    acti_tkn = Column(String(SIZE_255), nullable=True)

    def to_dict(self):
      return {
        'name': self.name,
        'email': self.email,
        'u3id': self.u3id
      }

Index('my_index_e', User.email, unique=True, mysql_length=SIZE_255)

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'public'),
                (Allow, 'user:auth', 'auth') ]
    def __init__(self, request):
        pass

class Udf(Base):
    __tablename__ = 'udf'
    id = Column(Integer, primary_key=True)
    u3id = Column(String(SIZE_255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    stamp = Column(String(SIZE_255))

    def to_dict(self):
      return {
        'updated_at': str(self.updated_at),
        'stamp': self.stamp
      }
       