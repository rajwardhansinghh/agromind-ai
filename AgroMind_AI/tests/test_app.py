import json
import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from app import Handler, MODEL
from model import validate, recommend

SAMPLE=dict(N=90,P=42,K=43,temperature=20.87974371,humidity=82.00274423,ph=6.502985292,rainfall=202.9355362,state='Madhya Pradesh',city='Indore',season='Kharif')

class ModelTests(unittest.TestCase):
    def test_dataset(self):
        self.assertEqual(len(MODEL.rows),2200)
        self.assertEqual(len(MODEL.profiles),22)
    def test_rice(self):
        self.assertEqual(recommend(MODEL,SAMPLE)['recommendations'][0]['crop'],'rice')
    def test_chickpea(self):
        x,label=next(row for row in MODEL.rows if row[1]=='chickpea')
        p=dict(zip(['N','P','K','temperature','humidity','ph','rainfall'],x))
        p.update(season='Rabi',state='Madhya Pradesh')
        self.assertEqual(recommend(MODEL,p)['recommendations'][0]['crop'],label)
    def test_validation(self):
        for patch in [{'ph':15},{'N':-1},{'humidity':101},{'temperature':float('nan')},{'K':True},{'N':'90'},{'season':'Winter'},{'city':3}]:
            with self.subTest(patch=patch),self.assertRaises(ValueError):validate({**SAMPLE,**patch})
        with self.assertRaises(ValueError):validate([])
        with self.assertRaises(ValueError):validate({})
    def test_context_rules_are_visible(self):
        data=recommend(MODEL,{**SAMPLE,'season':'Rabi'})
        self.assertFalse(data['recommendations'][0]['season_match'])
        self.assertTrue(any('season mismatch' in s for s in data['warnings']))
    def test_scores_finite(self):
        result=recommend(MODEL,{**SAMPLE,'N':0,'P':0,'K':0,'temperature':0,'humidity':0,'ph':0,'rainfall':0})
        self.assertTrue(result['warnings'])
        for row in result['recommendations']:self.assertTrue(0<=row['score']<=100)

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_static(self):
        for path in ['/','/style.css','/app.js','/api/health']:
            with urllib.request.urlopen(self.url+path) as response:self.assertEqual(response.status,200)
    def test_post(self):
        req=urllib.request.Request(self.url+'/api/recommend',json.dumps(SAMPLE).encode(),{'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as response:self.assertEqual(json.load(response)['recommendations'][0]['crop'],'rice')
    def test_bad_json(self):
        req=urllib.request.Request(self.url+'/api/recommend',b'{bad')
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
        self.assertEqual(e.exception.code,400)
    def test_missing_route(self):
        with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(self.url+'/model.py')
        self.assertEqual(e.exception.code,404)

if __name__=='__main__':unittest.main()
