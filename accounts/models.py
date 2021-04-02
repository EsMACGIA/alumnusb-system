from django.db import models
from django.contrib.auth.models import User
from accounts.utils import CountryField
from accounts.utils import CampusChoice
from accounts.utils import UndergraduateDegreeChoice
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError

# Modify django users to admit only unique emails
User._meta.get_field('email')._unique = True

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
		return self.email

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
		return self.email

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

class Contact(models.Model):
	id = models.CharField(max_length=50, primary_key=True)
	email = models.EmailField(max_length=60, unique=True)

class Donation(models.Model):
	id = models.CharField(max_length=50, primary_key=True)
	contact = models.ForeignKey(Contact,on_delete=models.CASCADE,default=None)
	amount = models.FloatField()
	date = models.DateField()

class Friends(models.Model):
	friend_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_b_friends')
	friend_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_a_friends')

	class Meta:
		unique_together = ('friend_a', 'friend_b')

	# Define extra constraints
	def clean(self):

		# Throw a validation error if someone tries to switch friends order and add them again
		try:
			Friends.objects.get(friend_a_id=self.friend_b_id, friend_b_id=self.friend_a_id)
			raise ValidationError('These two users are friends already.')
		except Friends.DoesNotExist:
			pass

		# You cannot be your own friend
		if self.friend_a_id == self.friend_b_id:
			raise ValidationError('You cannot be your own friend.')

class FriendRequest(models.Model):
	requesting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requests')
	requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requested')
	date = models.DateField(default=timezone.now)

	class Meta:
		unique_together = ('requesting', 'requested')

	# Define extra constraints
	def clean(self):

		# Throw a validation error if someone tries to request friendship from a friend
		try:
			Friends.objects.get(friend_a_id=self.requesting_id, friend_b_id=self.requested_id)
			raise ValidationError('These two users are friends already.')
		except Friends.DoesNotExist:
			pass

		try:
			Friends.objects.get(friend_a_id=self.requested_id, friend_b_id=self.requesting_id)
			raise ValidationError('These two users are friends already.')
		except Friends.DoesNotExist:
			pass

		# You cannot be your own friend
		if self.requesting_id == self.requested_id:
			raise ValidationError('You cannot be your own friend.')
		

