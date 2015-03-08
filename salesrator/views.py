import os, uuid, time
from datetime import datetime
import shutil
from .a3db import *
from .reader import *
from .janitor import *
from pyramid.response import Response
import cPickle as pickle
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
  view_config,
  forbidden_view_config,
  )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    User,
    Udf,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .a3 import cleanup_dict
from .a3file import touch
from .a3user import *
from .doctor import *



@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'tutorial'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tutorial_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

# View for HTML, JS, CSS 
@view_config(route_name='app', renderer='templates/app.pt', permission='public')
def load_app(request):
  return {'title':'Salesrator - Analyze your data'}

#list of all the operations
@view_config(route_name='operations', renderer='json', permission='auth')
def operation_list(request):
  return cleanup_dict.operations

@view_config(route_name='cleanup', renderer='json', permission='auth')
def cleanup_api(request):
  # print request.body
  userid = str(request.authenticated_userid)
  data= dict(request.json_body)
  t = touch()
  paths = t.populate(userid)
  id = int(data['id'])
  para = dict(data['para'])
  d = cleanup_dict()
  a3db = A3_lib()
  op = d.operations
  lastest_file = sorted(os.listdir(paths[0]))
  file_path = os.path.join(paths[0],lastest_file[0])
  # print lastest_file,file_path
  c = readcsv(file_path,0)
  # appending frame to the dict
  para.update({'frame':c})
  # formatting the column name for example 'Q1'-> 'c.Q1'
  if 'col' in para.keys():
  	col = '%s.%s'%(c,para['col'])
  	para.update({'col':col})
  if 'cols' in para.keys():
  	temp=[]
  	for x in para['cols']:
  		x = '%s.%s'%(c,x)
  		temp.append(x)
  	para.update({'cols':temp})
  # print file_path
  if str(data['operation']) == op[id % 100]['operation'] :
    res = globals()[data['operation']](**para)
    # res1 = res.to_json()
    # print res1
  return res

@view_config(route_name='fileupload', renderer='templates/app.pt', permission='auth')
def handle_file(request):
  userid = str(request.authenticated_userid)
  t = touch()
  a3db = A3_lib()
  paths = t.populate(userid)
  filename = request.POST['csv'].filename
  input_file = request.POST['csv'].file
  filename = str(time.time())
  # print str(paths[2])
  file_path = os.path.join(paths[0], '%s.csv' % filename)
  temp_file_path = file_path + '~'
  input_file.seek(0)
  with open(temp_file_path, 'wb') as output_file:
    shutil.copyfileobj(input_file, output_file)
  os.rename(temp_file_path, file_path)
  c = readcsv(file_path)
  pickle_path = os.path.join(paths[2], '%s.pickel' %filename)
  pickle.dump(c,open(pickle_path ,"wb"))
  udf = Udf(stamp=filename, u3id=userid, updated_at=datetime.utcnow(), created_at=datetime.utcnow())
  DBSession.add(udf)
  print DBSession.query(Udf)
  return HTTPFound(location=request.route_url('app'))

# login, logout, signup
@view_config(route_name='login', renderer='json', permission='public')
def try_login(request):
  data = dict(request.json_body)
  for x in ['passwd', 'email']:
    if not x in data:
      return {'status':'error', 'message':'Insufficient Data'}
  if not auth_user(data['email'], data['passwd']) == False:
    headers = remember(request, get_user(email=data['email']).u3id)
    print "LOGIN SUCCESS"
    return HTTPFound(location=request.route_url('loginsuccess'), headers=headers)
  return {'status': 'error', 'message':'Wrong Credentials'}

@view_config(route_name='loginsuccess', renderer='json', permission='auth')
def echo_success(request):
  return {'status':'success'}

@view_config(route_name='logout', renderer='templates/app.pt', permission='auth')
def logout(request):
  headers = forget(request)
  return HTTPFound(location=request.route_url('app'), headers=headers)

@view_config(route_name='signup', renderer='json', permission='public')
def signup_new_user(request):
  data = dict(request.json_body)
  for x in ['passwd', 'email', 'name']:
    if not x in data:
      return {'status':'error', 'message':'Insufficient Data'}
  return {
    'status':'success', 
    'u3id':add_user(data['email'], data['passwd'], data['name'])
    }
