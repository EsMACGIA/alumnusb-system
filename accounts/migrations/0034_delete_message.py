# Generated by Django 3.0.3 on 2020-03-18 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]