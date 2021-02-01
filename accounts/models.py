from django.db import models
from django.contrib.auth.models import User
from accounts.utils import CountryField
from accounts.utils import CampusChoice
from accounts.utils import UndergraduateDegreeChoice
from django.utils import timezone
from datetime import date

class ProfilePicture(models.Model):
	picture = models.ImageField(upload_to='static/prof_img/')

class UserInformation(models.Model):
	first_name = models.CharField(max_length=30, default='-')
	middle_name = models.CharField(max_length=30, default='-')
	last_name = models.CharField(max_length=30, default='-')
	mailing_city = models.CharField(max_length=30, default='-')
	mailing_state = models.CharField(max_length=30, default='-')
	usb_alumn = models.BooleanField(default=False)
	codigo_alumn_usb = models.CharField(max_length=30, default='-')
	mailing_country = CountryField()
	email = models.EmailField(max_length=60, unique=True)
	mobile = models.CharField(max_length=30, default='-')
	cohorte = models.IntegerField(default=0)
	birthdate = models.DateField()
	age = models.IntegerField(default=0)
	undergrad_degree = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in UndergraduateDegreeChoice])
	graduate_degree = models.CharField(max_length=60)
	carnet = models.IntegerField(default=0)
	usb_undergrad_campus = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in CampusChoice])
	graduate_campus = models.CharField(max_length=30, default='-')
	work_email = models.EmailField(max_length=60)
	workplace = models.CharField(max_length=30, default='-')
	donor = models.BooleanField(default=False)
	social_networks = models.CharField(max_length=50, default='-')
	twitter_account = models.CharField(max_length=60,default='-')
	instagram_account = models.CharField(max_length=60, default='-')
	picture = models.ForeignKey(ProfilePicture, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.Email

class UserStats(models.Model):
	email = models.EmailField(max_length=60, unique=True)
	average_gift = models.FloatField()
	largest_gift = models.FloatField()
	smallest_gift = models.FloatField()
	total_gifts = models.FloatField()
	best_gift_year_total = models.FloatField()
	best_gift_year = models.IntegerField(null=True)
	first_gift_date = models.DateField(null=True)
	last_gift_date = models.DateField(null=True)
	total_number_of_gifts = models.IntegerField()

	def __str__(self):
		return self.Email

class Achievements(models.Model):
	name = models.CharField(primary_key=True, max_length=50)
	description = models.CharField(max_length=200)
	picture = models.ImageField(default='static/achiev_img/C.png', upload_to='static/achiev_img/') 
	level = models.IntegerField(default=1)
	

class UserAchievements(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	achievement = models.ForeignKey(Achievements,on_delete=models.CASCADE,default=None)
	date = models.DateField(default=timezone.now)

	# Falta definir un __str__

class Message(models.Model):
	page = models.CharField(max_length=30, primary_key=True)
	title = models.CharField(max_length=50,default=' ')
	txt = models.CharField(max_length=2000,default=' ')
