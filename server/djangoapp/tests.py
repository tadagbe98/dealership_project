from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
from .models import CarMake, CarModel


class CarMakeModelTest(TestCase):
    def setUp(self):
        self.make = CarMake.objects.create(
            name='Toyota',
            description='Japanese manufacturer',
            country_of_origin='Japan',
            founded_year=1937
        )

    def test_car_make_str(self):
        self.assertEqual(str(self.make), 'Toyota')

    def test_car_make_creation(self):
        self.assertEqual(self.make.name, 'Toyota')
        self.assertEqual(self.make.country_of_origin, 'Japan')


class CarModelTest(TestCase):
    def setUp(self):
        self.make = CarMake.objects.create(name='Toyota')
        self.model = CarModel.objects.create(
            car_make=self.make,
            name='Camry',
            car_type='SEDAN',
            year=2023
        )

    def test_car_model_str(self):
        self.assertIn('Toyota', str(self.model))
        self.assertIn('Camry', str(self.model))

    def test_car_model_creation(self):
        self.assertEqual(self.model.name, 'Camry')
        self.assertEqual(self.model.year, 2023)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )

    def test_login_valid(self):
        response = self.client.post(
            '/djangoapp/login',
            data=json.dumps({'userName': 'testuser', 'password': 'testpass123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'Authenticated')
        self.assertEqual(data['userName'], 'testuser')

    def test_login_invalid(self):
        response = self.client.post(
            '/djangoapp/login',
            data=json.dumps({'userName': 'testuser', 'password': 'wrongpass'}),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'Failed')

    def test_registration(self):
        response = self.client.post(
            '/djangoapp/register',
            data=json.dumps({
                'userName': 'newuser',
                'firstName': 'New',
                'lastName': 'User',
                'email': 'new@example.com',
                'password': 'newpass123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'Authenticated')

    def test_registration_duplicate(self):
        response = self.client.post(
            '/djangoapp/register',
            data=json.dumps({
                'userName': 'testuser',
                'password': 'anypass'
            }),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(data.get('error'), 'Already Registered')

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/djangoapp/logout')
        self.assertEqual(response.status_code, 200)


class DealerViewsTest(TestCase):
    def test_get_dealerships(self):
        response = self.client.get('/djangoapp/get_dealers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('dealers', data)

    def test_get_dealerships_by_state(self):
        response = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('dealers', data)

    def test_get_cars(self):
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('CarModels', data)

    def test_analyze_review(self):
        response = self.client.get('/djangoapp/analyze_review?text=Fantastic services')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('sentiment', data)
        self.assertEqual(data['sentiment'], 'positive')

    def test_analyze_review_no_text(self):
        response = self.client.get('/djangoapp/analyze_review')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 400)
