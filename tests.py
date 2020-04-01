import unittest
import json
import sys, os.path

dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(dir_path)

from appv1 import *

class TestAppV1(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_Hello_World(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World !', response.data) # b pasa el string a bytes

    def test_v1_24(self):
        response = self.app.get('/servicio/v1/prediccion/24horas/')
        self.assertEqual(response.status_code, 200)

    def test_v1_48(self):
        response = self.app.get('/servicio/v1/prediccion/48horas/')
        self.assertEqual(response.status_code, 200)

    def test_v1_72(self):
        response = self.app.get('/servicio/v1/prediccion/72horas/')
        self.assertEqual(response.status_code, 200)
