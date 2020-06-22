from flask import Flask, render_template, g, jsonify, request, redirect, url_for, session, flash
from flask_cors import CORS, cross_origin
import requests
import requests
import uuid
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
import numpy as np
import config
import sendgrid
import os
from forms import ContactForm
from sendgrid.helpers.mail import *
from dbhelper import DBHelper
from werkzeug.utils import secure_filename
response_object = {'status': 'success'}
from waitress import serve
from flask_sslify import SSLify
from flask_caching import Cache
cache = Cache()
import sqreen
from dateutil.parser import parse
from datetime import datetime, timezone
from flask import Session

par = config.config
sqreen.start()

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

cache_servers = os.environ.get('MEMCACHIER_SERVERS', par['MEMCACHIER_SERVERS'])
cache_servers = None
if cache_servers == None:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or par['MEMCACHIER_USERNAME']
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or par['MEMCACHIER_PASSWORD']
    cache.init_app(app,
    config={'CACHE_TYPE': 'saslmemcached',
                'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                'CACHE_MEMCACHED_USERNAME': cache_user,
                'CACHE_MEMCACHED_PASSWORD': cache_pass,
                'CACHE_OPTIONS': { 'behaviors': {
                    # Faster IO
                    'tcp_nodelay': True,
                    # Keep connection alive
                    'tcp_keepalive': True,
                    # Timeout for set/get requests
                    'connect_timeout': 2000, # ms
                    'send_timeout': 750 * 1000, # us
                    'receive_timeout': 750 * 1000, # us
                    '_poll_timeout': 2000, # ms
                    # Better failover
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30}}})



DB = DBHelper()

BOOKS = DB.acc_list()
project = DB.proj_list()
tasks = DB.tasks()

UPLOAD_FOLDER = os.path.basename('/upload')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#sslify = SSLify(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sg = sendgrid.SendGridAPIClient(apikey=os.getenv('SENDGRID_API_KEY', par['sendgrid']))
app.secret_key = b'_%5#y2L"F4Q8z\n\xec]/'
receipent = os.getenv('SENDGRID', par['send_to'])
CORS(app)
oauth = OAuth(app)
callback_url = os.getenv('AUTH0_CALLBACK_URL','http://localhost:5005/callback')

#SESSION_TYPE = 'null'
#SESSION_PERMANENT = False
#SESSION_USE_SIGNER = True
#PERMANENT_SESSION_LIFETIME = 4200
#app.config.from_object(__name__)
#Session(app)

auth0 = oauth.register(
    'auth0',
    client_id = os.getenv('AUTH0_CLIENT_ID', par['client']),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET', par['client_sec']),
    api_base_url=os.getenv('AUTH0_DOMAIN', par['domain']),
    access_token_url=os.getenv('AUTH0_DOMAIN'+'/oauth/token', par['domain']+'/oauth/token'),
    authorize_url=os.getenv('AUTH0_DOMAIN'+'/authorize', par['domain']+'/authorize'),
    client_kwargs={
        'scope': 'openid profile',
    },
)

def mail(from_who, subjectsend, message):
    from_email = Email(from_who)
    to_email = Email(receipent)
    subject = subjectsend
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if (response.status_code == 202):
        return('sent')
    else:
        return('opps')


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
            # Redirect to Login pa ge here
        return redirect('/login')

    #print(session.get('profile'))
    #profile = session.get('profile')
    #aged = profile['started']
    #age = datetime.now() - aged
    #age = 500
    age = {
        "seconds": 800        
    }

    st = session['profile']['started']
    age = datetime.now() - st
    if age.seconds > 900:  
        return redirect('/logout') 

    session['profile']['started'] = datetime.now()    

    return f(*args, **kwargs)

  return decorated

@app.route('/robots.txt')
def bots():
   return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def map():
    return app.send_static_file('sitemap.xml')    

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'started' : parse(userinfo['updated_at'])
    }
    
    return redirect('/app')

#Upload
@app.route('/api/upload/<id>/<pr_id>', methods=['POST','OPTIONS','GET','DELETE'])
@cross_origin(methods=['*'])
@requires_auth
def upload_file(id,pr_id):
    to_do = list(request.files.keys())
    f_list = []
    for todo in to_do:
        f = request.files[todo]
        st = DB.att(f.read(),f.filename,pr_id,id)
        f_list.append(f.filename)
    return 'file(s) uploaded successfully ' + str(f_list)

@app.route('/api/attachments/<id>/<pr_id>', methods=['POST','OPTIONS','GET','DELETE']) 
@cross_origin(methods=['*'])
@requires_auth
def att(id,pr_id):
    if request.method == 'GET':
        response_object['project'] = DB.att_list(pr_id,id)
        return jsonify(response_object)
    elif request.method == 'DELETE':
        return jsonify(DB.file_del(pr_id,id))
    return jsonify('nothing to do ere')   

@app.route('/api/attachment/<name>', methods=['POST','OPTIONS','GET','DELETE']) 
@cross_origin(methods=['*'])
@requires_auth
def att_single(name):
    if request.method == 'GET':
        if name is not None:
            f = DB.get_file(name)
            r = app.response_class(f, direct_passthrough=True, mimetype='application/octet-stream')
            r.headers.set('Content-Disposition', 'attachment', filename=name)
            return r

        else:
            return 'error'

    elif request.method == 'DELETE':
        return jsonify(DB.file_del('','',name))
    return jsonify('nothing to do ere')  

@app.route('/api/stats',methods=['GET'])
@cross_origin(methods=["*"])
#@requires_auth
def stats():
    return jsonify({"log": DB.get_log()})

@app.route('/api/random')
@cross_origin()
@requires_auth
def random_number():
    response = {
        'randomNumber': np.random.randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/books', methods=['GET', 'POST'])
@cross_origin()
@requires_auth
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        DB.add_acc({
            'LCTRYNUM': post_data.get('LCTRYNUM'),
            'LC': post_data.get('LC'),
            'MAJOR': post_data.get('MAJOR'),
            'MINOR': post_data.get('MINOR'),
            'ID': uuid.uuid4().hex
        })
        response_object['message'] = 'Account updated!'
        cache.delete('all_books')
    else:
        response_object['books'] = cache.get('all_books')
        if response_object['books'] == None:
            response_object['books'] = DB.acc_list()            
            cache.set('all_books', response_object['books'])

    return jsonify(response_object)

@app.route('/api/books/<book_id>',methods=['PUT', 'DELETE'])
@cross_origin(allow_headers=['Content-Type'])
@requires_auth
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        DB.delete('acc', book_id)
        DB.add_acc({
            'LCTRYNUM': post_data.get('LCTRYNUM'),
            'LC': post_data.get('LC'),
            'MAJOR': post_data.get('MAJOR'),
            'MINOR': post_data.get('MINOR'),
            'ID': book_id
        })
        response_object['message'] = 'Account updated!'
    if request.method == 'DELETE':
        DB.delete('acc', book_id)
        response_object['message'] = 'Account removed!'
    cache.delete('all_books')    
    return jsonify(response_object)


@app.route('/api/projects', methods=['GET', 'POST'])
@cross_origin()
@requires_auth
def all_projects():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        DB.add_proj({
            'LCTRYNUM': post_data.get('LCTRYNUM'),
            'LC': post_data.get('LC'),
            'NAME': post_data.get('NAME'),
            'START': post_data.get('START'),
            'END': post_data.get('END'),
            'STATUS': post_data.get('STATUS'),
            'OWNER': post_data.get('OWNER'),
            'DESC': post_data.get('DESC'),
            'ID': uuid.uuid4().hex,
            'FILE2': post_data.get('FILE2')
        })
        response_object['message'] = 'Project updated!'
    else:
        response_object['project'] = DB.proj_list()
    return jsonify(response_object)

@app.route('/api/projects/<book_id>',methods=['PUT', 'DELETE'])
@cross_origin(allow_headers=['Content-Type'])
@requires_auth
def single_project(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        DB.delete('proj', book_id)
        DB.add_proj({
            'LCTRYNUM': post_data.get('LCTRYNUM'),
            'LC': post_data.get('LC'),
            'NAME': post_data.get('NAME'),
            'START': post_data.get('START'),
            'END': post_data.get('END'),
            'STATUS': post_data.get('STATUS'),
            'OWNER': post_data.get('OWNER'),
            'ID': book_id,
            'DESC': post_data.get('DESC'),
            'FILE2': post_data.get('FILE2')
        })
        response_object['message'] = 'Project updated!'
    if request.method == 'DELETE':
        DB.delete('proj', book_id, '','delete')
        response_object['message'] = 'Project removed!'
    return jsonify(response_object)


@app.route('/api/tasks/<pr_id>',methods=['GET','POST'])
@cross_origin(allow_headers=['Content-Type'])
@requires_auth
def single_proj(pr_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object['message'] = 'Tasks provided'
        response_object['tasks'] = get_tasks(pr_id)
    if request.method == 'POST':
        post_data = request.get_json()
        DB.add_task({
            'ID': uuid.uuid4().hex,
            'PR_ID': pr_id,
            'NAME': post_data.get('NAME'),
            'START': post_data.get('START'),
            'END': post_data.get('END'),
            'STATUS': post_data.get('STATUS'),
            'OWNER': post_data.get('OWNER'),
            'TDESC': post_data.get('TDESC'),
            'FILET': post_data.get('FILET')
        })
        response_object['message'] = 'Added!'

    return jsonify(response_object)

@app.route('/api/tasks/<id>/<pr_id>',methods=['PUT', 'DELETE'])
@cross_origin(allow_headers=['Content-Type'])
@requires_auth
def single_projSer(id,pr_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        DB.delete('task', pr_id,id)
        DB.add_task({
            'ID': id,
            'PR_ID': pr_id,
            'NAME': post_data.get('NAME'),
            'START': post_data.get('START'),
            'END': post_data.get('END'),
            'STATUS': post_data.get('STATUS'),
            'OWNER': post_data.get('OWNER'),
            'TDESC': post_data.get('TDESC'),
            'FILET': post_data.get('FILET')
        })
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        DB.delete('task', pr_id,id)
        response_object['message'] = 'Task removed!'

    return jsonify(response_object)


def get_tasks(pr_id):
    taskList = []
    tasks = DB.tasks()
    for task in tasks:
        if task['PR_ID'] == pr_id:
            taskList.append(task)

    return taskList

# /server.py

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=callback_url, audience=os.getenv('AUTH0_DOMAIN'+'/userinfo',par['domain']+'/userinfo'))

#@app.route('/app')
@app.route('/app', defaults={'path': ''})
@app.route('/<path:path>')
#@requires_auth
def catch_all(path):
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
def default():
    return render_template("home.html")

@app.route('/about', methods=['GET'])
def who():
    return render_template("about.html")    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    form = ContactForm(request.form)
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      respon = mail(form.email.data, form.subject.data, form.name.data + "sent ==>  " + form.message.data)
      return redirect('/home')
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/privacy', methods=['GET'])
def private():
    return render_template("Privacy.html")   

@app.route('/terms', methods=['GET'])
def terms():
    return render_template("Terms.html")  


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.getenv('AUTH0_CLIENT_ID', par['client'])}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))  

port = os.getenv('PORT', '5005')
if __name__ == "__main__":
	#app.run(host='0.0.0.0', port=int(port),debug=False)
    serve(app, url_scheme='http', threads=4, port=int(port))
