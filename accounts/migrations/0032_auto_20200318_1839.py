# Generated by Django 3.0.3 on 2020-03-18 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20200318_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_achievements',
            name='Date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
