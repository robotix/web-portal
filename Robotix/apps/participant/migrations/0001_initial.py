# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 21:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('miscellaneous', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('mobile', models.BigIntegerField(help_text='Do NOT add a 0 or +91', validators=[django.core.validators.RegexValidator('^[789]\\d{9}$', message='Invalid mobile number<br>Do NOT add a 0 or +91')], verbose_name='Mobile Number')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail address')),
                ('year', models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth')], verbose_name='Year of study')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miscellaneous.College')),
            ],
        ),
    ]