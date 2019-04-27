from django.db import models
from django.contrib.auth.models import User
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
import random
from base64 import b64encode
import datetime


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

        url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates/' + instance.profile.get_display_id()
        print(url)
        created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
        username = 'shauryag+tigertravel333'
        link = "https://tigerbook.herokuapp.com/api/v1/getkey/tigertravel333"
        password = '16d243926dbcf1b9a087073415f5beac'

        generated_digest = b64encode(hashlib.sha256((nonce + created + password).encode('utf-8')).digest()).decode('utf-8')

        r = requests.get(url, headers = {
            'Authorization': 'WSSE profile="UsernameToken"',
            'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, b64encode(nonce.encode()).decode('utf-8'), created)
        })

        instance.email = instance.profile.get_display_id() + '@princeton.edu'

        Profile.objects.create(user=instance, college = r.json()['res_college'], email=instance.profile.get_display_id()+'@princeton.edu', name=r.json()['first_name'] + ' ' + r.json()['last_name'])



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()