from django.test import TestCase
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

import datetime

from .models import Profile
from .forms import ProfileForm


class AccountsModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='Tester',
            password='Tester123',
        )
        self.profile = Profile.objects.filter(user=self.user)

    def test_profile_exists(self):
        self.assertEqual(self.profile.count(), 1)


class SignUpViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='Tester',
            password='Tester123',
        )
        self.url = reverse('accounts:signup')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_data(self):
        data = {'username': 'Bartosz123', 'password1': 'Tester123',
                'password2': 'Tester123', 'bio': 'Hello'}
        response = self.client.post(self.url, data)
        user = self.User.objects.get(username='Bartosz123')
        self.assertEqual(user.profile.bio, 'Hello')


class ProfileFormTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='Tester',
            password='Tester123',
        )

    def test_profile_creation(self):
        date_birth = datetime.date(1993, 5, 23)
        data = {'date_birth': date_birth, 'bio': 'Hello World'}
        form = ProfileForm(
            data,
            instance=self.user.profile
        )
        self.assertTrue(form.is_valid())
        new_profile = form.save()
        self.assertEqual(new_profile.date_birth, date_birth)
        self.assertEqual(new_profile.bio, 'Hello World')

    def test_not_adult(self):
        today = datetime.datetime.now().date()
        form = ProfileForm(
            {'date_birth': today},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        adult_error = 'You are not adult'
        self.assertTrue(adult_error in form.errors)



