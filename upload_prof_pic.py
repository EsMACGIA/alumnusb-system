import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alumnusb_system.settings")

import django
django.setup()

from django.core.files import File
from accounts.models import *

ProfilePicture.objects.all().delete()

img1 = ProfilePicture()

img1.picture.save('img1.png', File(open('static/img/profile-pic/1.png', 'rb')))

img2 = ProfilePicture()

img2.picture.save('img2.png', File(open('static/img/profile-pic/2.png', 'rb')))

img3 = ProfilePicture()

img3.picture.save('img3.png', File(open('static/img/profile-pic/3.png', 'rb')))

img4 = ProfilePicture()

img4.picture.save('img4.png', File(open('static/img/profile-pic/4.png', 'rb')))

img5 = ProfilePicture()

img5.picture.save('img5.png', File(open('static/img/profile-pic/5.png', 'rb')))

img6 = ProfilePicture()

img6.picture.save('img6.png', File(open('static/img/profile-pic/6.png', 'rb')))