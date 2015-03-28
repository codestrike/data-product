import os, time, json
from datetime import datetime
import shutil
from .a3db import *
from .reader import *
from .janitor import *
from .descriptor import *
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
from .a3file import *
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

@view_config(route_name='userdata', renderer='json', permission='auth')
def userdata(request):
  return {
    'files':get_udf_data,
    'user':get_user
    }[dict(request.json_body)['info']](request.authenticated_userid, to_dict=True)

@view_config(route_name='cleanup', renderer='json', permission='auth')
def cleanup_api(request):
  userid = str(request.authenticated_userid)
  data = dict(request.json_body)
  paths = touch().populate(userid)
  (operation_id, para) = (int(data['id']), dict(data['para']))
  dataframe = readcsv(os.path.join(paths[0],
    get_user(u3id=userid, to_dict=True)['stamp'] + '.csv'),
    0)
  para.update({'frame':dataframe})
  # formatting the column name for example 'Q1'-> 'c.Q1'
  if 'col' in para.keys():
    # col = '%s.%s' % (dataframe, para['col'])
    para.update({'col':para['col']})
  if 'cols' in para.keys():
    temp = []
    for x in para['cols']:
      x = '%s.%s'%(dataframe, x)
      temp.append(x)
    para.update({'cols':temp})
  res = None
  if str(data['operation']) == cleanup_dict().operations[operation_id % 100]['operation']:
    res = globals()[data['operation']](**para)
    print res
  print "\n\n\nGoing To Print Describe All on Data Frame\n\n"
  print describe_all(dataframe)
  return dict(json.loads(describe_all(dataframe).to_json()))

@view_config(route_name='plot', renderer='json', permission='auth')
def plot_api(request):
  userid = str(request.authenticated_userid)
  paths = touch().populate(userid)
  frame = readcsv(os.path.join(paths[0],
    get_user(u3id=userid, to_dict=True)['stamp'] + '.csv'),
    0)
  remove_higher_outlier(frame, 'Tot2014')
  box_plot(frame,'Tot2014','AgeinService','tot_ageinservice.png',(0,100000000))
  return {'url':'0.0.0.0:6543/' + os.getcwd() + 'tot_ageinservice.png'}

@view_config(route_name='fileupload', renderer='templates/app.pt', permission='auth')
def handle_file(request):
  userid = str(request.authenticated_userid)
  paths = touch().populate(userid)
  input_file = request.POST['csv'].file
  filename = str(time.time())
  file_path = os.path.join(paths[0], '%s.csv' % filename)
  # Lets Write Data To Temporary File
  temp_file_path = file_path + '~'
  input_file.seek(0)
  with open(temp_file_path, 'wb') as output_file:
    shutil.copyfileobj(input_file, output_file)
  # Lets Rename Temporary File To Original
  os.rename(temp_file_path, file_path)
  # Lets Create Pickel Of This CSV File
  pickle.dump(readcsv(file_path), 
    open(os.path.join(paths[2], '%s.pickle' % filename), 'wb'))
  # Lets Store filename In Database As stamp
  udf = Udf(stamp=filename, u3id=userid, updated_at=datetime.utcnow(), created_at=datetime.utcnow())
  DBSession.add(udf)
  return HTTPFound(location=request.route_url('app'))

@view_config(route_name='fileupdate', renderer='json')
def update_or_delete_file(request):
  data = dict(request.json_body)
  return {
    #'rename': set_pretty_name,
    'remove': delete_udf,
    'reset': recreate_pickel_for,
    'set': set_working_udf_to
  }[data['operation']](u3id=request.authenticated_userid, stamp=data['stamp'])

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
