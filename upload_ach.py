import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alumnusb_system.settings")

import django
django.setup()

from django.core.files import File
from accounts.models import *

Achievements.objects.all().delete()

ach1 = Achievements(name='Numero donaciones bronce',
					description='Llega a 5 donaciones',
					level=1)
ach1.picture.save('nro_don_bronce.png', File(open('static/img/medals/t2-1.png', 'rb')))

ach2 = Achievements(name='Numero donaciones plata',
					description='Llega a 10 donaciones',
					level=2)
ach2.picture.save('nro_don_plata.png', File(open('static/img/medals/t2-2.png', 'rb')))

ach3 = Achievements(name='Numero donaciones oro',
					description='Llega a 20 donaciones',
					level=3)
ach3.picture.save('nro_don_oro.png', File(open('static/img/medals/t2-3.png', 'rb')))

ach4 = Achievements(name='Numero donaciones platino',
					description='Llega a 50 donaciones',
					level=4)
ach4.picture.save('nro_don_platino.png', File(open('static/img/medals/t2-4.png', 'rb')))

ach5 = Achievements(name='Numero donaciones diamante',
					description='Llega a 100 donaciones',
					level=5)
ach5.picture.save('nro_don_diamante.png', File(open('static/img/medals/t2-6.png', 'rb')))



ach6 = Achievements(name='Total donaciones bronce',
					description='Dona al menos 100 dolares',
					level=1)
ach6.picture.save('total_don_bronce.png', File(open('static/img/medals/t1-1.png', 'rb')))

ach7 = Achievements(name='Total donaciones plata',
					description='Dona al menos 500 dolares',
					level=2)
ach7.picture.save('total_don_plata.png', File(open('static/img/medals/t1-3.png', 'rb')))

ach8 = Achievements(name='Total donaciones oro',
					description='Dona al menos 1500 dolares',
					level=3)
ach8.picture.save('total_don_oro.png', File(open('static/img/medals/t1-5.png', 'rb')))

ach9 = Achievements(name='Total donaciones platino',
					description='Dona al menos 3000 dolares',
					level=4)
ach9.picture.save('total_don_platino.png', File(open('static/img/medals/t1-7.png', 'rb')))

ach10 = Achievements(name='Total donaciones diamante',
					description='Dona al menos 5000 dolares',
					level=5)
ach10.picture.save('total_don_diamante.png', File(open('static/img/medals/t1-8.png', 'rb')))


ach11 = Achievements(name='Donacion estrella bronce',
					description='Realiza una donacion de al menos 5 dolares',
					level=1)
ach11.picture.save('max_don_bronce.png', File(open('static/img/medals/t3-1.png', 'rb')))

ach12 = Achievements(name='Donacion estrella plata',
					description='Realiza una donacion de al menos 20 dolares',
					level=2)
ach12.picture.save('max_don_plata.png', File(open('static/img/medals/t3-2.png', 'rb')))

ach13 = Achievements(name='Donacion estrella oro',
					description='Realiza una donacion de al menos 50 dolares',
					level=3)
ach13.picture.save('max_don_oro.png', File(open('static/img/medals/t3-3.png', 'rb')))

ach14 = Achievements(name='Donacion estrella platino',
					description='Realiza una donacion de al menos 100 dolares',
					level=4)
ach14.picture.save('max_don_platino.png', File(open('static/img/medals/t3-4.png', 'rb')))

ach15 = Achievements(name='Donacion estrella diamante',
					description='Realiza una donacion de al menos 500 dolares',
					level=5)
ach15.picture.save('max_don_diamante.png', File(open('static/img/medals/t3-5.png', 'rb')))

ach16 = Achievements(name='Donante',
					description='Realiza una donacion',
					level=5)
ach16.picture.save('donante.png', File(open('static/img/medals/t5.png', 'rb')))

ach17 = Achievements(name='Donante recurrente',
					description='Realiza una donacion de al menos 1000 dolares',
					level=5)
ach17.picture.save('recurrente.png', File(open('static/img/medals/t4.png', 'rb')))

