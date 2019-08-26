# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import date, timedelta
from decimal import Decimal

from django.core.urlresolvers import reverse
from coop_cms.tests import MediaBaseTestCase

from model_mommy import mommy
from balafon.Crm.models import Contact, Zone

from .models import Competition, License


class PayPlugTest(MediaBaseTestCase):

    def setUp(self):
        super(PayPlugTest, self).setUp()
        mommy.make(Zone, code="42")

    def test_post_inscription(self):
        url = reverse("course_inscription")

        competition = mommy.make(
            Competition, price=Decimal('10.00'), price_before=Decimal('8.50'), before_date=date.today() + timedelta(1)
        )
        license = mommy.make(License, nb_required=False)

        data = {
            'gender': Contact.GENDER_FEMALE,
            'lastname': u'FAYOLLE',
            'firstname': u'Frédérique',
            'birth_date': '07/07/1980',
            'email': 'fredfayolle1@gmail.com',
            'address': '296 rue Saint Pierre',
            'zip_code': '42810',
            'city': 'Rozier en Donzy',
            #'country': '',
            'phone': '0477280367',
            'competition': competition.id,
            'club': '',
            'license': license.id,
            'license_number': '',
            'scan': self._get_file("unittest1.txt"),
            'accept_rules': True
        }

        response = self.client.post(url, data=data)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content)
            print(soup.select('ul.errorlist li'))
        #else
        #    print(response)

        self.assertEqual(302, response.status_code)
        payment_url = response['Location']
        print(payment_url)

        self.assertTrue('%0A' not in payment_url)
        self.assertTrue('%0a' not in payment_url)

        self.assertEqual(Contact.objects.count(), 1)