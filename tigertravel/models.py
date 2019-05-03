from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import json

class Request(models.Model):
	origin = models.CharField(max_length=50, default='PRINCETON')
	destination = models.CharField(max_length=50)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	person = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, default='person')

	def get_absolute_url(self):
		return reverse('tigertravel-profile')

class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField(default="message")
    

class Group(models.Model):
	origin = models.CharField(max_length=50, default='PRINCETON') 
	destination = models.CharField(max_length=50)
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	members = models.ManyToManyField(Request)
	comments = models.ManyToManyField(Comment)
	size = models.CharField(max_length=50, default="1")
	text = models.TextField(default="message")






