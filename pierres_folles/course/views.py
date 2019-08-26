# -*- coding: utf-8 -*-

import base64
from datetime import date, datetime
import json
from OpenSSL import crypto
from urllib.parse import urlencode, quote_plus
import xlwt


from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.dateformat import DateFormat
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View, TemplateView

from coop_cms.utils import dehtml

from balafon.permissions import can_access
from balafon.Crm.models import Contact, Entity, Group, Action, ActionStatus, ActionType
from balafon.Emailing.utils import send_verification_email, EmailSendError

from pierres_folles.course.forms import RunnerForm
from pierres_folles.course.models import Runner, InstantPaymentNotification, Course, Competition, Category


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.items():
        # if isinstance(v, unicode):
        #     v = v.encode('utf8')
        # elif isinstance(v, str):
        #     # Must be encoded in UTF-8
        #     v.decode('utf8')
        out_dict[k] = v
    return out_dict


def send_ipn_confirmation_email(runner):
    """send an email to subscriber for checking his email"""

    if runner.email:

        data = {
            'runner': runner,
            'verification_url': reverse('emailing_email_verification', args=[runner.uuid]),
            'site': Site.objects.get_current(),
        }
        the_template = get_template('Emailing/ipn_confirmation_email.txt')
        content = the_template.render(Context(data))

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')

        email = EmailMessage(
            _(u'Confirmation de votre inscription à la course des Pierres Folles'),
            content,
            from_email,
            [runner.email]
        )
        try:
            email.send()
        except Exception as msg:  # pylint: disable=broad-except
            raise EmailSendError(msg)
        return True
    return False


class InstantPaymentNotificationView(View):
    """ipn view payment"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InstantPaymentNotificationView, self).dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     if settings.DEBUG:
    #         runner = get_object_or_404(Runner, uuid=kwargs['contact_uuid'])
    #         send_ipn_confirmation_email(runner)
    #     return super(InstantPaymentNotificationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        runner = get_object_or_404(Runner, uuid=kwargs['contact_uuid'])
        ipn = InstantPaymentNotification.objects.create(runner=runner)

        signature = ''
        for key, item in request.META.items():
            if key.upper() == 'HTTP_PAYPLUG_SIGNATURE':
                signature = item

        if signature:
            ipn.signature = signature
        else:
            ipn.signature = request.META.items()
        ipn.body = request.body
        ipn.save()

        data = json.loads(request.body)

        #openssl_pkey_get_public
        #rsa_key = open(settings.PROJECT_PATH + '/payplug_public.pem', 'r').read()
        #rsa_key = open(settings.PROJECT_PATH + '/payplug_pubkey.pem', 'r').read()
        #cert = crypto.load_pkcs12(crypto.FILETYPE_PEM, rsa_key)
        # crypto.verify(cert, signature, data, 'sha-1')

        # try:
        #     rsa_key = open(settings.PROJECT_PATH + '/payplug_pubkey.pem', 'r').read()
        #     pubkey = rsa.PublicKey.load_pkcs1(rsa_key)
        #     rsa.verify(request.body, signature, pubkey)
        #     ipn.signature_ok = True
        # except Exception, e:
        #     #raise Exception("IPN : RSA Verification failed: {0}".format(data))
        #     pass

        ipn.is_valid = True
        ipn.transaction_id = data['id_transaction']
        ipn.save()

        contact = Contact.objects.get(id=runner.id)

        # update subscription status
        ipn.is_amount_valid = (runner.get_payplug_amount() == data['amount'])
        ipn.is_email_valid = (contact.email == data['email'])
        try:
            ipn.is_contact_valid = (contact.id == int(data['customer']))
        except ValueError:
            ipn.is_contact_valid = False
        ipn.save()

        paid_group = Group.objects.get_or_create(name='Paiement Ok')[0]
        paid_pb_group = Group.objects.get_or_create(name='Paiement : PROBLEME')[0]

        if all([ipn.is_valid, ipn.is_amount_valid, ipn.is_email_valid, ipn.is_contact_valid]):
            paid_group.contacts.add(contact)
            paid_group.save()
        else:
            paid_pb_group.contacts.add(contact)
            paid_pb_group.save()

        #send validation email
        # send_verification_email(contact)
        send_ipn_confirmation_email(runner)

        return HttpResponse('Ok')


class RunnerView(FormView):
    """subscription form"""

    form_class = RunnerForm
    template_name = 'course/inscription.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        entity = Entity.objects.create(
            type=None,
            is_single_contact=True,
            name=u'?'
        )
        form.instance.entity = entity

        runner = form.save()
        contact = Contact.objects.get(id=runner.id)
        entity.default_contact.delete()
        entity.name = u"{0} {1}".format(contact.lastname, contact.firstname)
        entity.save()

        notes = runner.notes.strip().split('\n')
        #contact.notes = runner.notes = ''
        contact.phone.strip()
        if contact.phone.find('06') == 0 or contact.phone.find('07') == 0:
            contact.mobile = contact.phone
            contact.phone = ''
        contact.save()

        action_type = ActionType.objects.get_or_create(name=u'Inscription 2017')[0]
        action = Action.objects.create(
            type=action_type,
            planned_date=datetime.now(),
            amount=runner.get_price(),
            subject=notes[0],
            detail='\n'.join(notes[1:])
        )
        action.contacts.add(contact)
        action.save()

        contact_club = runner.club.strip()
        # if not contact_club:
        #     contact_club = u'Sans club'
        # contact.add_to_group(contact_club)

        contact.add_to_group('Participation 2017')

        contact.add_to_group(runner.competition.name)

        contact.set_custom_field('license', runner.license.short_name or runner.license.name)
        contact.set_custom_field('license_number', runner.license_number)
        contact.set_custom_field('club', contact_club)

        contact.set_custom_field('scan', runner.scan.url, is_link=True)

        if settings.DEBUG:
            print(">>>", contact.uuid)

        pay_plug = settings.PAYPLUG_SETTINGS

        url_domain = u'https://{0}'.format(Site.objects.get_current().domain)

        payment_data = {
            'amount': runner.get_payplug_amount(),  # in cents
            'currency': 'EUR',
            'ipn_url': url_domain + reverse('course_instant_payment_notification', args=[runner.uuid]),
            'email': contact.email,
            'first_name': contact.firstname,
            'last_name': contact.lastname,
            'return_url': url_domain + '/merci/',
            'cancel_url': url_domain + '/annulation/',
            'customer': contact.id
        }

        payment_data = encoded_dict(payment_data)

        url_params = urlencode(payment_data)
        encoded_payment_data = quote_plus(url_params)

        rsa_key = open(settings.PROJECT_PATH + '/payplug.pem', 'r').read()
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, rsa_key)
        signed_data = crypto.sign(private_key, url_params, "sha1")

        out_str = base64.b64encode(signed_data)

        encoded_signed_data = quote_plus(out_str)

        payment_url = '{0}?data={1}&sign={2}'.format(
            pay_plug['base_url'],
            encoded_payment_data,
            encoded_signed_data
        )
        runner.payment_url = payment_url
        runner.save()

        if settings.DEBUG:
            print(payment_url)
            #payment_url = '/merci'
        return HttpResponseRedirect(payment_url)


class XlsExportView(View):
    only_staff = True
    doc_name = 'balafon.xls'
    _col_widths = None
    _line_heights = None

    def dispatch(self, *args, **kwargs):
        if self.only_staff and not can_access(self.request.user):
            raise PermissionDenied()
        return super(XlsExportView, self).dispatch(*args, **kwargs)

    def get_default_style(self):
        """

        * Colour index
        8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,
        7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
        20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on... sty

        * Borders
        borders.left, borders.right, borders.top, borders.bottom
        May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED,
        THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED,
        SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 0x00
        borders.right_colour = 0x00
        borders.top_colour = 0x00
        borders.bottom_colour = 0x00
        style.borders = borders

        * Fonts
        style.font = xlwt.Font()
        style.font.height = 8 * 20
        style.font.colour_index = 22

        * Alignment
        style.alignment = xlwt.Alignment()
        style.alignment.horz = xlwt.Alignment.HORZ_LEFT
        style.alignment.vert = xlwt.Alignment.VERT_CENTER

        * Pattern
        May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12

        style.pattern = xlwt.Pattern()
        style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = 23

        """

        style = xlwt.XFStyle()
        return style

    def _calculate_size(self, ws, line, column, value):
        col_widths = [len(value_lines) for value_lines in str(value).split("\n")]
        line_height = (len(col_widths) * 240) if len(col_widths) > 1 else 0
        width = 1500 + max(col_widths) * 220

        if width > self._col_widths.get(column, 0):
            self._col_widths[column] = width
            ws.col(column).width = width
        if line_height > self._line_heights.get(line, 0):
            self._line_heights[line] = line_height
            ws.row(line).height_mismatch = True
            ws.row(line).height = line_height

    def get_value(self, value):
        if isinstance(value, date):
            date_format = DateFormat(value)
            return date_format.format("d/m/y").capitalize()
        elif isinstance(value, datetime):
            date_format = DateFormat(value)
            return date_format.format("d/m/y H:M").capitalize()
        return value

    def write_cell(self, sheet, line, column, value, *args, **kwargs):
        value = self.get_value(value)
        style = kwargs.pop('style', None) or self.get_default_style()
        ret = sheet.write(line, column, value, style, *args, **kwargs)
        self._calculate_size(sheet, line, column, value)
        return ret

    def write_merge(self, sheet, line1, line2, column1, column2, value, *args, **kwargs):
        value = self.get_value(value)
        style = kwargs.pop('style', None) or self.get_default_style()
        ret = sheet.write_merge(line1, line2, column1, column2, value, style, *args, **kwargs)
        self._calculate_size(sheet, line1, column1, value)
        return ret

    def do_fill_workbook(self, workbook):
        """implement it in base class"""
        pass

    def get(self, *args, **kwargs):
        workbook = xlwt.Workbook()
        self._col_widths = {}
        self._line_heights = {}
        self.do_fill_workbook(workbook)

        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename={0}'.format(self.doc_name)
        workbook.save(response)
        return response


class InscriptionsXlsView(XlsExportView):
    doc_name = 'inscriptions_course-des-pierres-folles_2017.xls'

    def get_header_style(self):
        style = xlwt.XFStyle()
        style.pattern = xlwt.Pattern()
        style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = 22
        return style

    def get_warning_style(self):
        #style = xlwt.easyxf("protection: cell_locked false;")
        style = xlwt.XFStyle()
        style.pattern = xlwt.Pattern()
        style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = 2  # Red
        return style

    def get_default_style(self):
        #style = xlwt.easyxf("protection: cell_locked false;")
        style = xlwt.XFStyle()
        return style

    def do_fill_workbook(self, workbook):
        """implement it in base class"""

        year = datetime.today().year
        participants_group = get_object_or_404(Group, name=u'Participation {0}'.format(year))
        groups = []
        for competition in Competition.objects.filter(is_archived=False):
            try:
                groups.append(Group.objects.get(name=competition.name))
            except Group.DoesNotExist:
                pass

        # group_18 = Group.objects.get(name=u'18 kilomètres')
        # group_12 = Group.objects.get(name=u'12 kilomètres')
        # group_6 = Group.objects.get(name=u'6 kilomètres')

        groupe_inscription_ok = Group.objects.get(name=u'Inscription Ok')
        groupe_paiement_ok = Group.objects.get(name=u'Paiement Ok')

        columns = [
            u'NUMERO', u'Nom', u'Prénom', u"Téléphone", u'Sexe', u'Naissance', u'License', u'Club', u'Email', u'Ville',
            u'Code postal', u'Inscription Ok', u'Paiement Ok', u'Notes', u'{0}'.format(year)
        ]

        for group in groups:

            sheet = workbook.add_sheet(group.name)
            sheet.protect = True

            warning_style = self.get_warning_style()

            for col, label in enumerate(columns):
                self.write_cell(sheet, 0, col, label, style=self.get_header_style())

            contacts = group.contacts.extra(
                select={'lower_name': 'lower(lastname)'}
            ).order_by('lower_name')
            for line, contact in enumerate(contacts):

                inscription_ok = contact in groupe_inscription_ok.contacts.all()
                paiement_ok = contact in groupe_paiement_ok.contacts.all()
                est_participant = contact in participants_group.contacts.all()

                try:
                    runner = Runner.objects.get(id=contact.id)
                    club = runner.club.strip()
                except Runner.DoesNotExist:
                    club = contact.get_custom_field('club').strip()

                #self.write_cell(sheet, line + 1, 0, contact.id, style=self.get_header_style())
                # self.write_cell(
                #     sheet, line + 1, 1, u'{0.lastname} {0.firstname}'.format(contact),
                #     style=None
                # )
                self.write_cell(
                    sheet, line + 1, 1, u'{0.lastname}'.format(contact),
                    style=warning_style if not (inscription_ok and paiement_ok) else None
                )
                self.write_cell(
                    sheet, line + 1, 2, u'{0.firstname}'.format(contact),
                    style=warning_style if not (inscription_ok and paiement_ok) else None
                )
                self.write_cell(sheet, line + 1, 3, contact.phone or contact.mobile)

                gender = ''
                if contact.gender == Contact.GENDER_MALE:
                    gender = u'H'
                elif contact.gender == Contact.GENDER_FEMALE:
                    gender = u'F'
                self.write_cell(sheet, line + 1, 4, gender)

                if contact.birth_date:
                    self.write_cell(sheet, line + 1, 5, contact.birth_date.year)
                else:
                    self.write_cell(sheet, line + 1, 5, u'??', style=warning_style)

                self.write_cell(sheet, line + 1, 6, contact.get_custom_field('license'))

                self.write_cell(sheet, line + 1, 7, club)

                self.write_cell(sheet, line + 1, 8, contact.email)

                self.write_cell(sheet, line + 1, 9, contact.city.name if contact.city else "?")

                self.write_cell(sheet, line + 1, 10, contact.zip_code)

                self.write_cell(
                    sheet, line + 1, 11, u'Oui' if inscription_ok else u'Non',
                    style=warning_style if not inscription_ok else None
                )

                self.write_cell(
                    sheet, line + 1, 12, u'Oui' if paiement_ok else u'Non',
                    style=warning_style if not paiement_ok else None
                )

                self.write_cell(sheet, line + 1, 13, dehtml(contact.notes))

                self.write_cell(sheet, line + 1, 14, u'X' if est_participant else u'')


class ClassementView(TemplateView):
    template_name = 'course/classement.html'

    def get_context_data(self, **kwargs):
        context = super(ClassementView, self).get_context_data(**kwargs)

        results = []
        award = ['gold', 'silver', 'bronze']

        courses = Course.objects.all()
        for course in courses:
            result = {
                'course': course,
                'scratch': [],
                'categories': [],
            }
            hommes, femmes = [], []
            for inscrit in course.inscrit_set.filter(arrivee__isnull=False).order_by('arrivee'):
                if inscrit.gender == Contact.GENDER_MALE:
                    if len(hommes) < 3:
                        inscrit.award = award[len(hommes)]
                    hommes.append(inscrit)
                    suffix = u'er' if len(hommes) == 1 else u'ème'
                    inscrit.gender_position = u'{0}{1}'.format(len(hommes), suffix)
                else:
                    if len(femmes) < 3:
                        inscrit.award = award[len(femmes)]
                    femmes.append(inscrit)
                    suffix = u'ère' if len(femmes) == 1 else u'ème'
                    inscrit.gender_position = u'{0}{1}'.format(len(femmes), suffix)

                result['scratch'].append(inscrit)

            for cat in Category.objects.all():
                hommes, femmes = [], []
                inscrits = []
                for inscrit in cat.inscrit_set.filter(arrivee__isnull=False, course=course).order_by('arrivee'):

                    if inscrit.gender == Contact.GENDER_MALE:
                        if len(hommes) == 0:
                            inscrit.award = award[0]
                        hommes.append(inscrit)
                        suffix = u'er' if len(hommes) == 1 else u'ème'
                        inscrit.gender_position = u'{0}{1}'.format(len(hommes), suffix)
                    else:
                        if len(femmes) == 0:
                            inscrit.award = award[0]
                        femmes.append(inscrit)
                        suffix = u'ère' if len(femmes) == 1 else u'ème'
                        inscrit.gender_position = u'{0}{1}'.format(len(femmes), suffix)
                    inscrits.append(inscrit)

                result['categories'].append({
                    'name': cat.name,
                    'inscrits': inscrits,
                })
            results.append(result)

        context['results'] = results
        return context






