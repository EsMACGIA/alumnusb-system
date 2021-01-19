# Generated by Django 3.0.3 on 2020-03-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_merge_20200317_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_information',
            name='Donor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_information',
            name='USB_alumn',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user_information',
            name='Undergrad_degree',
            field=models.CharField(choices=[('IE', 'Ingeniería Eléctrica'), ('IM', 'Ingeniería Mecánica'), ('IQ', 'Ingeniería Química'), ('IEl', 'Ingeniería Electrónica'), ('IMa', 'Ingeniería de Materiales'), ('IC', 'Ingeniería de la Computación'), ('IG', 'Ingeniería Geofísica'), ('IP', 'Ingeniería de Producción'), ('IMn', 'Ingeniería de Mantenimiento'), ('IT', 'Ingeniería de Telecomunicaciones'), ('AR', 'Arquitectura'), ('UR', 'Urbanismo'), ('LQ', 'Licenciatura en Química'), ('LM', 'Licenciatura en Matemáticas'), ('LF', 'Licenciatura en Física'), ('LB', 'Licenciatura en Biología'), ('LCI', 'Licenciatura en Comercio Internacional'), ('LGH', 'Licenciatura en Gestión de la Hospitalidad'), ('EL', 'Licenciatura en Estudios y Artes Liberales'), ('EC', 'Economía'), ('OT', 'Otro')], max_length=3),
        ),
    ]