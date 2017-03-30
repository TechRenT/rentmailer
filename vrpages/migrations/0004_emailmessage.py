# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 07:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vrpages', '0003_messagetemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message_body', models.TextField()),
                ('message_type', models.CharField(max_length=10)),
                ('polished_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vrpages.PolishedUrl')),
            ],
        ),
    ]