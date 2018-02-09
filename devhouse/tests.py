from rest_framework.test import APIClient
from rest_framework import status
import devhouse.models as models
from django.contrib.auth.models import User
import unittest
import json
from datetime import time


class UserAuthTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_dir_data():
        for element in ['weekday', 'weekend']:
            if not models.DayType.objects.filter(name=element).first():
                models.DayType.objects.create(name=element)

        for element in ['work', 'lunch', 'break']:
            if not models.PeriodType.objects.filter(name=element).first():
                models.PeriodType.objects.create(name=element)

    def auth(self):
        response = self.client.post('/auth/', {"username": "admin", "password": "admin"})
        self.auth_token = response.data['token'] if 'token' in response.data else None
        return response

    def create_user_admin(self, name='admin', pwd='admin'):
        response = User.objects.filter(username=name).first()
        if not response:
            response = self.client.post("/api/user/", {'username': name, 'password': pwd})
        return response

    def test_create_user(self):
        response = self.create_user_admin(name='test_admin')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def create_data(self):
        self.create_user_admin()
        self.auth()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token)
        self.create_dir_data()

    def create_shop(self, name='testshop'):
        response = models.Shop.objects.filter(name=name).first()
        if not response:
            response = self.client.post("/api/shop/", {'name': name})
        return response

    def get_shop(self, name=''):
        response = models.Shop.objects.filter(name=name).first()
        if not response:
            return
        return self.client.get('/api/shop/{}/'.format(response.id))

    def test_create(self, name='testshop'):
        self.create_data()
        response = self.create_shop(name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(name, response.data['name'])

    def test_is_working(self):
        self.create_data()
        name = self.create_shop().name
        shop = self.get_shop(name)
        self.assertTrue(shop.data['result']['is_working'])

    def test_get_shop_schedule(self):
        self.create_data()
        name = self.create_shop().name
        shop = self.get_shop(name)
        shop_id = shop.data['result']['id']
        schedules = self.client.get('/api/schedule/{}/'.format(shop_id))
        response_data = json.loads(schedules.data)
        self.assertTrue(len(response_data or []) > 0)
        for element in response_data:
            self.assertEqual(element['shop'], shop_id)

    def test_update_shop_schedule(self):
        self.create_data()
        name = self.create_shop().name
        shop = self.get_shop(name)
        shop_id = shop.data['result']['id']
        changed_data = {'shop': shop_id, 'daytype': 1, 'periodtype': 1,
                        'period_start': time(9, 0), 'period_end': time(18, 0)}
        schedules = self.client.put('/api/schedule/update/{}/'.format(shop_id), data=changed_data)
        self.assertEqual(schedules.data['period_start'], str(time(9, 0)))
        self.assertEqual(schedules.data['period_end'], str(time(18, 0)))

    def test_shop_closing(self):
        self.create_data()
        name = self.create_shop().name
        shop = self.get_shop(name)
        self.assertTrue(shop.data['result']['is_working'])
        self.client.put('/api/shop/close/', data={'shop': shop.data['result']['id']})
        shop = self.get_shop(name)
        self.assertFalse(shop.data['result']['is_working'])
