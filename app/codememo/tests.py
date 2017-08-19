# coding=utf8
import json
from django.test import TestCase
from django.test import Client
from dbmodel.models import CodeMemo

class CodeMemoTestCase(TestCase):
    def setUp(self):
        params = {
            'id': 1,
            'ctype': u'linux',
            'description': u'根据相关文件名终止进程',
            'content': u'ps -ef | grep run.py | awk "{print $2}" | xargs kill -9'
        }
        CodeMemo.objects.create(**params)
        self.client = Client()

    def test_get_codes(self):
        apis = ['/api/codememo/codes/']
        params = {
            'ctype': u'mysql',
            'description': u'删除表语句',
            'content': u'DROP TABLE table_name'
        }
        for api in apis:
            resp = self.client.get(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)
            if len(content['d']) <= 0:
                self.assertRaisesMessage('列表没有数据返回')

    def test_add_code(self):
        apis = ['/api/codememo/new/']
        params = {
            'ctype': u'mysql',
            'description': u'删除表语句',
            'content': u'DROP TABLE table_name'
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/codememo/codes/')
            self.assertContains(resp, params['ctype'])
            self.assertContains(resp, params['content'])

    def test_update_code(self):
        apis = ['/api/codememo/1/update/']
        params = {
            'ctype': u'mysql',
            'description': u'it shows how to delete table from mysql',
            'content': u'DROP TABLE table_name'
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/codememo/codes/')
            self.assertContains(resp, params['ctype'])
            self.assertContains(resp, params['content'])

    def test_delete_code(self):
        apis = ['/api/codememo/1/delete/']
        for api in apis:
            resp = self.client.post(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

    