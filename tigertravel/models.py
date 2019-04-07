from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Group(models.Model):
	destination = models.CharField(max_length=50)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	members = models.ManyToManyField(User)

class Request(models.Model):
	destination = models.CharField(max_length=50)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	person = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('tigertravel-listings')

# class User(models.Model):
# 	user = 
# 	netid =
# 	email =
# 	photo = 