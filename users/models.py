from django.db import models
from django.contrib.auth.models import User
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
import random
from base64 import b64encode
from datetime import datetime

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
	name = models.CharField(max_length=50, default='Firstname Lastname')
	college = models.CharField(max_length=50, default='RoMa')
	email = models.CharField(max_length=50, default='example@princeton.edu')

	def __str__(self):
		return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
    	'''URL = "https://tigerbook.herokuapp.com/api/v1/getkey"
    	data = requests.get(URL)

    	URL2 = "https://https://tigerbook.herokuapp.com/api/v1/undergraudates/" + instance.profile.get_display_id()
    	created2 = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    	nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
    	username = instance.profile.get_display_id()
    	password = data.content

    	byteToString = hashlib.sha256(nonce + created2 + password).digest()
    	newString = byteToString.decode("utf-8")
    	generated_digest = b64encode(newString)

    	headers = {
    		'Authorization': 'WSSE profile="UsernameToken"',
    		'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, b64encode(nonce), created2)
    	}
    	
    	r = requests.get(URL2, headers = headers)

    	data2 = r.json()

    	print(data2)'''

    	instance.email = instance.profile.get_display_id() +'@princeton.edu'
    	Profile.objects.create(user=instance, email=instance.profile.get_display_id() +'@princeton.edu')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()