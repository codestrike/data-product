import os, uuid
import shutil
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
  view_config,
  forbidden_view_config,
  )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .a3 import cleanup_dict
from .a3file import touch
from .a3user import *




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

#list of all the oprations
@view_config(route_name='oprations', renderer='json', permission='auth')
def operation_list(request):
  # print cleanup_dict.oprations
  return cleanup_dict.oprations

@view_config(route_name='cleanup', renderer='json', permission='auth')
def cleanup_api(request):
  # print request.body
  data= dict(request.json_body)
  id = data['id']
  para = data['para']
  print  id,para
  return  id,para

@view_config(route_name='fileupload', renderer='string', permission='auth')
def handle_file(request):
  userid = str(uuid.uuid3(uuid.NAMESPACE_URL, 'ash'))
  t = touch()
  paths = t.populate(userid)
  filename = request.POST['csv'].filename
  input_file = request.POST['csv'].file
  file_path = os.path.join(paths[0], '%s.csv' % userid)
  temp_file_path = file_path + '~'
  input_file.seek(0)
  with open(temp_file_path, 'wb') as output_file:
    shutil.copyfileobj(input_file, output_file)
  os.rename(temp_file_path, file_path)
  return Response('OK')

# login, logout, signup
@view_config(route_name='login', renderer='json', permission='public')
def try_login(request):
  data = dict(request.json_body)
  for x in ['passwd', 'email']:
    if not x in data:
      return {'status':'error', 'message':'Insufficient Data'}
  if not auth_user(data['email'], data['passwd']) == False:
    headers = remember(request, data['email'])
    print "LOGIN SUCCESS"
    return HTTPFound(location=request.route_url('loginsuccess'), headers=headers)
  return {'status': 'error', 'message':'Wrong Credentials'}

@view_config(route_name='loginsuccess', renderer='json', permission='auth')
def echo_success(request):
  return {'status':'success'}

@view_config(route_name='logout', renderer='json', permission='auth')
def logout(request):
  headers = forget(request)
  return HTTPFound(location=request.route_url('app'), headers=headers)

@view_config(route_name='signup', renderer='json', permission='public')
def signup_new_user(request):
  for x in ['passwd', 'email', 'name']:
    if not x in request.POST:
      return {'status':'error', 'message':'Insufficient Data'}
  return {
    'status':'success', 
    'u3id':add_user(request.POST['email'], request.POST['passwd'], request.POST['name'])
    }
