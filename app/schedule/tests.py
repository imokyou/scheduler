# coding=utf8
import json
import pytz
from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.test import Client
from django.utils.encoding import force_text
from dbmodel.models import Schedule, ScheduleConfig

class ScheduleTestCase(TestCase):
    def setUp(self):
        targets = [
            {'content': u'俯卧撑', 'done': 0},
            {'content': u'卷腹', 'done': 0}
        ]
        params = {
            'id': 1,
            'stype': u'keepfit',
            'subject': u'8月增肌计划之胸、腹训练',
            'sdate': timezone.now(),
            'targets': json.dumps(targets)
        }
        Schedule.objects.create(**params)

        cparams = {
            'id': 1,
            'schedule_id': 1,
            'key': 'sendhour',
            'value': 10
        }
        ScheduleConfig.objects.create(**cparams)
        self.client = Client()

    def test_get_schedules(self):
        apis = [
            '/api/schedules/',
            '/api/schedules/?p=1&n=7'
        ]
        for api in apis:
            resp = self.client.get(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)
            if len(content['d']) == 0:
                self.assertRaisesMessage('列表没有数据返回')

    def test_get_schedule(self):
        apis = [ '/api/schedule/1/']
        for api in apis:
            resp = self.client.get(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)
            self.assertEqual(content['d']['id'], 1)

    def test_add_schedule(self):
        apis = [ '/api/schedule/new/']
        targets = [
            {'content': u'俯卧撑', 'done': 0},
            {'content': u'卷腹', 'done': 0}
        ]
        params = {
            'stype': u'study',
            'subject': u'哪里不懂点哪里',
            'sdate': '2017-08-20',
            'targets': json.dumps(targets)
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            id = content['d']['id']
            resp = self.client.get('/api/schedule/%s/' % id)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)
            self.assertEqual(content['d']['stype'], u'study')


    def test_update_schedule(self):
        apis = [ '/api/schedule/1/update/']
        targets = [
            {'content': u'俯卧撑1', 'done': 1},
            {'content': u'卷腹1', 'done': 1}
        ]
        params = {
            'stype': u'keepfits',
            'subject': u'9月增肌计划之腹训练',
            'sdate': u'2017-08-20',
            'targets': json.dumps(targets)
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/schedule/1/')
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)
            self.assertEqual(content['d']['stype'], params['stype'])
            self.assertEqual(content['d']['subject'], params['subject'])
            self.assertEqual(content['d']['sdate'], params['sdate'])
            self.assertJSONEqual(json.dumps(content['d']['targets']), targets)

    def test_delete_schedule(self):
        apis = [ '/api/schedule/1/delete/']
        for api in apis:
            resp = self.client.post(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/schedule/1/')
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], -2000)
            if len(content['d']) >= 1:
                self.assertRaisesMessage('删除失败!')

    def test_get_schedule_configs(self):
        apis = ['/api/schedule/1/configs/']
        for api in apis:
            resp = self.client.get(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            if len(content['d']) <= 0:
                self.assertRaisesMessage('列表没有数据返回!')

    def test_add_schedule_config(self):
        apis = ['/api/schedule/1/config/new/']
        params = {
            'key': 'sendday',
            'value': '10'
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/schedule/1/configs/')
            self.assertContains(resp, 'sendday')
                
    def test_update_schedule_config(self):
        apis = ['/api/schedule/1/config/1/update/']
        params = {
            'key': 'sendddd',
            'value': 12
        }
        for api in apis:
            resp = self.client.post(api, params)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/schedule/1/configs/')
            self.assertContains(resp, params['key'])
            self.assertContains(resp, params['value'])

    def test_delete_schedule_config(self):
        apis = ['/api/schedule/1/config/1/delete/']
        for api in apis:
            resp = self.client.post(api)
            self.assertEqual(resp.status_code, 200)
            content = json.loads(resp.content)
            self.assertEqual(content['c'], 0)

            resp = self.client.get('/api/schedule/1/configs/')
            content = json.loads(resp.content)
            if len(content['d']) >= 1:
                self.assertRaisesMessage('配置删除失败')