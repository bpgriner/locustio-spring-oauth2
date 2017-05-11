from locust import HttpLocust, TaskSet, task, web
from bs4 import BeautifulSoup
from rauth import OAuth2Service
from flask import request
import json

yourservice = OAuth2Service(
    name='locust',
    client_id='locust-loadtesting',
    client_secret='', # Spring OAuth2 requires client_id:client_secret to be passed into the
                      # headers (base64 encoded) when retrieving the access token, so it's not needed here.
                      # http://stackoverflow.com/questions/26881296/spring-security-oauth2-full-authentication-is-required-to-access-this-resource
    authorize_url='http://localhost:8080/yourservice/oauth/authorize',
    access_token_url='http://localhost:8080/yourservice/oauth/token',
    base_url='http://localhost:8080/')

redirect_uri = 'http://localhost:8089/callback'
params = {'scope': 'read', 'response_type': 'code', 'redirect_uri': redirect_uri}

access_token = None

@web.app.route('/callback')
def callback():
    global access_token

    code = request.args.get('code')
    options = {'code' : code, 'redirect_uri' : redirect_uri, 'grant_type' : 'authorization_code'}

    # 'locust-loadtesting:secret' base64 encoded -> bG9jdXN0LWxvYWR0ZXN0aW5nOnNlY3JldA==
    # 'locust-loadtesting' needs to match the OAuth Client's Client ID stored in the host applications datastore 
    # 'secret' needs to match the Oauth Client's Client Secret hash value in the datastore (BCrypt Hash)
    response = yourservice.get_raw_access_token(data=options, headers={'Authorization' : 'Basic bG9jdXN0LWxvYWR0ZXN0aW5nOnNlY3JldA=='})
    
    # Since the user is logged in at this point, the access token is not needed.  Grab and print anyway.
    response = json.loads(response.content)
    access_token = response['access_token']
    print '[callback] access_token: %s' % access_token

    return 'You successfully hit the callback page!'

class UserBehavior(TaskSet):
    def on_start(self):
        url = yourservice.get_authorize_url(**params)
        response = self.client.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf'}).get('value')
        print '[on_start] CSRF token found: %s' % csrf_token

        self.client.post('/yourservice/login', {'username': 'youruser', 'password': 'youruserspassword', '_csrf': csrf_token})

    # Example functions to call REST endpoints located at /yourservice/api/v1.0/documents/active and /yourservice/api/v1.0/documents
    # These functions will need to be modified to match the REST endpoints you have available
    @task
    def get_user_documents_by_status_active(self):
        # The OAuth endpoints can be hit once a user is logged in (OAuth2ConfigHolder class), so
        # adding the token to the request is not necessary.
        #self.client.headers['Authorization'] = 'bearer ' + access_token
        
        response = self.client.get('/yourservice/api/v1.0/documents/active')
        #print 'response code: %s' % response.status_code
        #print 'response content: %s' % response.content

    @task
    def get_user_documents(self):
        self.client.get('/yourservice/api/v1.0/documents')

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = 'http://localhost:8080' # yourservice REST endpoints
    min_wait = 5000
    max_wait = 9000
