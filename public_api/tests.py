from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from .views import home, contact


class HomeTests(TestCase):

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class ContactTests(TestCase):

    def test_contact_view_status_code(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_url_resolves_home_view(self):
        view = resolve('/public_api/contact')
        self.assertEquals(view.func, contact)
