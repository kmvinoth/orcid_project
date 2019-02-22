from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from .views import home, contact, member_api_invitation_link_view
from .models import Employees, OrcidInvitation

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


# class MemberApiInvitationTests(TestCase):
# Django bug: https://code.djangoproject.com/ticket/29177
#
#     def setUp(self):
#         employee_instance = Employees.objects.create(uid='mohanakv', first_name='vinothkumar',
#                                                      last_name='mohanakrishnan',
#                                                      mail='vinothkumar.mohanakrishnan@charite.de')
#         OrcidInvitation.objects.create(id=1, employee_uid=employee_instance, token='14ed5c5c106a43a996ab9a054dd14d22',
#                                        link='localhost:9000/invitation_link/14ed5c5c106a43a996ab9a054dd14d22')
#
#     def test_member_api_inivtation_view_status_code(self):
#         url = reverse('member_api_invitation_link', kwargs={'token':'14ed5c5c106a43a996ab9a054dd14d22'})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)