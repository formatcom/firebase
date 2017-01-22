import requests
import sys
import urlparse #for urlparse and urljoin
import os #for os.path.dirname
import json #for dumps
from time import sleep

class Firebase:
    ROOT_URL = '' #no trailing slash
    DEBUG    = False
    ERROR_500_RETRY = False
    ERROR_500_DELAY = 10

    def __init__(self, root_url, auth_token=None, debug=False, error_500_retry=False, error_500_delay=10):
        self.ROOT_URL = root_url.rstrip('/')
        self.auth_token = auth_token
        self.DEBUG = debug
        self.ERROR_500_RETRY = error_500_retry
        self.ERROR_500_DELAY = error_500_delay

    #These methods are intended to mimic Firebase API calls.

    def child(self, path):
       root_url = '%s/' % self.ROOT_URL
       url = urlparse.urljoin(root_url, path.lstrip('/'))
       return Firebase(url, self.auth_token, self.DEBUG)

    def parent(self):
       url = os.path.dirname(self.ROOT_URL)
       #If url is the root of your Firebase, return None
       up = urlparse.urlparse(url)
       if up.path == '':
          return None #maybe throw exception here?
       return Firebase(url, self.auth_token, self.DEBUG)

    def name(self):
        return os.path.basename(self.ROOT_URL)

    def toString(self):
        return self.__str__()
    def __str__(self):
        return self.ROOT_URL

    def set(self, value):
        return self.put(value)

    def push(self, data):
        return self.post(data)

    def update(self, data):
        return self.patch(data)

    def remove(self):
        return self.delete()


    #These mirror REST API functionality

    def put(self, data):
        return self.__request('put', data = data)

    def patch(self, data):
        return self.__request('patch', data = data)

    def get(self, query = None):
       self.QUERY = query
       return self.__request('get')

    #POST differs from PUT in that it is equivalent to doing a 'push()' in
    #Firebase where a new child location with unique name is generated and
    #returned
    def post(self, data):
        return self.__request('post', data = data)

    def delete(self):
        return self.__request('delete')


    #Private

    def __request(self, method, **kwargs):
        #Firebase API does not accept form-encoded PUT/POST data. It needs to
        #be JSON encoded.

        _kwargs = kwargs

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        params = {}
        if self.auth_token:
            if 'params' in kwargs:
                params = kwargs['params']
                del kwargs['params']
            params.update({'auth': self.auth_token})

        response = requests.request(method, self.__url(), params=params, **kwargs)
        
        if response.status_code == 200:
            return response.json()
        elif self.ERROR_500_RETRY and response.status_code == 500:
            if self.DEBUG:
                sys.stderr.write('[ ERROR 500 RETRY ]\n')
                sys.stderr.flush()
            sleep(self.ERROR_500_DELAY)
            return self.__request(method)
        else:
            response.raise_for_status() #throw exception if error

    def __url(self):
       #We append .json to end of ROOT_URL for REST API.
       _query = '%s.json?%s' % (self.ROOT_URL, self.QUERY)
       if self.DEBUG:
           sys.stdout.write('%s\n' % _query)
           sys.stdout.flush()
       return _query
