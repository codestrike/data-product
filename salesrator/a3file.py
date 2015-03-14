import os
from datetime import datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from .models import *
from .a3user import *

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class touch:
  def touchdir(self, to_touch):
    # temp_path = os.path.join(to_touch, extenstion)
    if not os.path.exists(to_touch):
      os.makedirs(to_touch)
    else :
      pass

  def populate(self, userid):
    bp = os.getcwd() + '/files/' + userid
    # file_path = a3file.touchdir(basepath ,'files')
    # file_path = a3file.touchdir(file_path ,userid)
    # csv_path = a3file.touchdir(file_path, 'csv' )
    # img_path = a3file.touchdir(file_path, 'img')
    # pickle_path = a3file.touchdir(file_path, 'pickle')
    paths = [bp+'/csv', bp+'/img', bp+'/pickle']
    for x in paths:
      self.touchdir(x)
    return paths

# functions to handle udf
def delete_file(u3id, stamp):
  print DBSession.delete(DBSession.query(Udf).filter(Udf.stamp==stamp, Udf.u3id==u3id).first())
  return {'status':'success'}

def recreate_pickel_for(u3id, stamp):
  pass
