import hashlib
import uuid
from datetime import datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from .models import *

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

SIZE_255 = 255

def add_user(email, plain, name):
  if DBSession.query(User).filter(User.email==email).first():
    return None
  u3id = str(uuid.uuid3(uuid.NAMESPACE_DNS, email.encode('ascii', 'ignore')))
  DBSession.add(User(email=email, passhash=hashlib.sha1(plain).hexdigest(), name=name, u3id=u3id))
  return u3id

def get_user(u3id=None, email=None):
  by = u3id if u3id==None else email
  if not u3id == None:
    return DBSession.query(User).filter(User.u3id==u3id).first()
  elif not email == None:
    return DBSession.query(User).filter(User.email==email).first()

def get_udf_data(u3id):
  with u3id:
    return DBSession.query(Udf).filter(Udf.u3id==u3id)

def auth_user(email, plain):
  u = DBSession.query(User).filter(User.email==email).first()
  if not u == None:
    return ['user:auth'] if u.passhash == hashlib.sha1(plain).hexdigest() else False
  return False

def groupfinder(userid, request):
  return ['user:auth']