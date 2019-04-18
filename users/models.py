from django.db import models
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
	name = models.CharField(max_length=50, default='yes')
	
	def __str__(self):
		return f'{self.user.username} Profile'