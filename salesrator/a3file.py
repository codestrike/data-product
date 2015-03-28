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

class touch(object):
  def touchdir(self, to_touch):
    # temp_path = os.path.join(to_touch, extenstion)
    if not os.path.exists(to_touch):
      os.makedirs(to_touch)
    else :
      pass

  def populate(self, userid):
    basepath = os.getcwd() + '/files/' + userid
    paths = [basepath+'/csv', basepath+'/img', basepath+'/pickle']
    for x in paths:
      self.touchdir(x)
    return paths

# functions to handle udf
def delete_udf(u3id, stamp):
  auto_correct_stamp_for(u3id, stamp_of_deleted_udf=stamp)
  basepath = os.getcwd() + '/files/' + u3id
  csvfile = basepath + '/csv/' + stamp + '.csv'
  picklefile = basepath + '/pickle/' + stamp + '.pickle'
  modified_csv = basepath + '/pickle/' + stamp + '.csv'
  if os.path.isfile(csvfile):
    os.remove(csvfile)
  if os.path.isfile(picklefile):
    os.remove(picklefile)
  if os.path.isfile(modified_csv):
    os.remove(modified_csv)
  DBSession.delete(DBSession.query(Udf).filter(Udf.stamp==stamp, Udf.u3id==u3id).first())
  return {'status':'success'}

def recreate_pickel_for(u3id, stamp):
  pass

def get_udf_data(u3id, to_dict=False):
  result = DBSession.query(Udf).filter(Udf.u3id==u3id).all()
  return result if not to_dict else [x.to_dict() for x in result if len(result)>0]