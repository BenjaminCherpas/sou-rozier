# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Crm', '0010_clean_same_as'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('year1', models.IntegerField()),
                ('year2', models.IntegerField()),
            ],
            options={
                'ordering': ('year1',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('price', models.DecimalField(verbose_name='Prix Jour J', max_digits=5, decimal_places=2)),
                ('price_before', models.DecimalField(verbose_name='Prix pr\xe9-inscription', max_digits=5, decimal_places=2)),
                ('before_date', models.DateField(verbose_name='Date limite pr\xe9-inscription')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Competition',
                'verbose_name_plural': 'Competitions',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('heure_depart', models.TimeField(default=datetime.time(16, 0))),
            ],
        ),
        migrations.CreateModel(
            name='Inscrit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=0)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('gender', models.IntegerField(choices=[(1, 'Homme'), (2, 'Femme')])),
                ('birth_date', models.DateField()),
                ('arrivee', models.TimeField(default=None, null=True, blank=True)),
                ('city', models.CharField(default=b'', max_length=100, blank=True)),
                ('zip_code', models.CharField(default=b'', max_length=100, blank=True)),
                ('email', models.EmailField(default=b'', max_length=254, blank=True)),
                ('club', models.CharField(default=b'', max_length=100, blank=True)),
                ('phone', models.CharField(default=b'', max_length=100, blank=True)),
                ('category', models.ForeignKey(default=None, blank=True, to='course.Category', null=True)),
            ],
            options={
                'ordering': ('numero', 'nom', 'prenom', 'arrivee'),
                'verbose_name': 'Inscrit',
                'verbose_name_plural': 'Inscrits',
            },
        ),
        migrations.CreateModel(
            name='InstantPaymentNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('body', models.TextField(default=b'', blank=True)),
                ('signature', models.TextField(default=b'', blank=True)),
                ('is_ssl_valid', models.BooleanField(default=False, verbose_name='SSL message is ok')),
                ('is_amount_valid', models.BooleanField(default=False, verbose_name='received amount is ok')),
                ('is_email_valid', models.BooleanField(default=False, verbose_name='received email is ok')),
                ('is_contact_valid', models.BooleanField(default=False, verbose_name='received customer id is ok')),
                ('transaction_id', models.IntegerField(default=0)),
                ('signature_ok', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nom')),
                ('nb_required', models.BooleanField(default=True, verbose_name='No de license requis')),
                ('short_name', models.CharField(default=b'', max_length=100, verbose_name='Nom court', blank=True)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Licence',
                'verbose_name_plural': 'Licence',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('url', models.URLField(default=b'', verbose_name='URL', blank=True)),
                ('logo', models.ImageField(default=b'', upload_to=b'partners', verbose_name='logo', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Sponsor',
                'verbose_name_plural': 'Sponsors',
            },
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Crm.Contact')),
                ('club', models.CharField(default=b'', max_length=100, verbose_name='Club', blank=True)),
                ('license_number', models.CharField(default=b'', max_length=100, verbose_name='N\xb0 de licence', blank=True)),
                ('scan', models.FileField(help_text='Joindre un scan de la license sportive ou du certificat m\xe9dical. Merci de ne pas d\xe9passer 2Mo comme taille de fichier.', upload_to=b'licenses', verbose_name='Fichier')),
                ('payment_url', models.TextField(default=b'', blank=True)),
                ('competition', models.ForeignKey(verbose_name='Course', to='course.Competition')),
                ('license', models.ForeignKey(default=None, to='course.License', blank=True, help_text="Si vous n'\xeates pas licenci\xe9, s\xe9lectionnez 'Cerificat m\xe9dical'", null=True, verbose_name='Licence')),
            ],
            options={
                'ordering': ('lastname', 'firstname'),
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
            bases=('Crm.contact',),
        ),
        migrations.AddField(
            model_name='instantpaymentnotification',
            name='runner',
            field=models.ForeignKey(to='course.Runner'),
        ),
        migrations.AddField(
            model_name='inscrit',
            name='contact',
            field=models.ForeignKey(default=None, blank=True, to='Crm.Contact', null=True),
        ),
        migrations.AddField(
            model_name='inscrit',
            name='course',
            field=models.ForeignKey(to='course.Course'),
        ),
    ]
