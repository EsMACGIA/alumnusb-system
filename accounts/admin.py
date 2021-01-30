from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserInformation)
admin.site.register(UserStats)
admin.site.register(Achievements)
admin.site.register(UserAchievements)
admin.site.register(Message)
admin.site.register(ProfilePicture)