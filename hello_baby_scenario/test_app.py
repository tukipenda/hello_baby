import sys
sys.path.append("/home/tukipenda/mysite")
sys.path.append("/home/cabox/workspace")
from hello_baby import app
import unittest
import json
import time

from flask.testing import FlaskClient
from flask.wrappers import Response

from scenario import Scenario
from preemie_ppv import *

p=PreemiePPVScenario()
p.loadData()


class JSONResponseWrapper(Response):
    """Extends the BaseResponse to add a get_json method.
    This should be used as the response wrapper in the TestClient.
    """

    def get_json(self):
        """Return the json decoded content."""
        return json.loads(self.get_data(as_text=True))


class JSONTestClient(FlaskClient):
    """Extends the FlaskClient request methods by adding json support.
    This should be used like so::
        app.test_client_class = JSONTestClient
        client = app.test_client()
        client.post(url, json=data)
    Note that this class will override any response_wrapper you wish to use.
    """

    def __init__(self, *args, **kwargs):
        """This ensures the response_wrapper is JSONResponseWrapper."""
        super(JSONTestClient, self).__init__(args[0], response_wrapper=JSONResponseWrapper, **kwargs)

    def open(self, *args, **kwargs):
        json_data = kwargs.pop('json', None)
        if json_data is not None:
            if 'data' in kwargs:
                raise ValueError('Use either `json` or `data`, not both.')

            if 'content_type' not in kwargs:
                kwargs['content_type'] = 'application/json'
            kwargs['data'] = json.dumps(json_data)

        return super(JSONTestClient, self).open(*args, **kwargs)

class FlaskTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        app.test_client_class=JSONTestClient
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 
        
        self.assertEqual(result.status_code, 200) 
    
    def test_complicated(self):
        def get_supply_dict(name, size):
            return {"taskName":'fetch', 'kv': {'name':name, 'size':size}}
        self.app.get("/scenario")
        slist=p.supplyMGR.supplyList
        self.app.post('/doTask', json=get_supply_dict("mask", "Infant"))
        for k in [1, 4, 2, 3, 19]:
            supply=slist[k]
            name=supply.name
            if hasattr(supply, "size"):
                size=supply.size
            else:
                size=None
            time.sleep(1)
            self.app.post('/doTask', json=get_supply_dict(name, size))
        
        self.app.post('/doTask', json=get_supply_dict("mask", "Preemie"))
        for k in range(12):
            time.sleep(1)
            self.app.post("/updatedata", json={})
        
    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # assert the response data

f=FlaskTests()
f.setUp()
f.test_home_status_code()
f.test_complicated()