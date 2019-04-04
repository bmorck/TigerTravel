from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# class Group(models.Model):
# 	destination =
# 	date =
# 	start_time =
# 	end_time =
# 	members = models.ManytoMany?

# class Request(models.Model):
# 	destination =
# 	date =
# 	start_time =
# 	end_time =
# 	person = models.ForeignKey(User)

# class User(models.Model):
# 	user =
# 	netid =
# 	email =
# 	photo = ?

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
