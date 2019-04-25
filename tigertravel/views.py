from django.shortcuts import render
from .models import Request, Group
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib import messages
import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
import django.utils
from django.utils import timezone
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class RequestCreateView(CreateView):
	model = Request
	fields = ['origin', 'destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/mainpage.html'

	def form_valid(self, form):

		for request in Request.objects.all():
			if self.request.user == request.person and form.instance.date == request.date:
				messages.error(self.request, 'You cannot have two trip requests for the same date!')
				return redirect('tigertravel-home')

		if form.instance.origin == form.instance.destination:
			messages.error(self.request, 'Origin and Destination cannot be the same!')
			return redirect('tigertravel-home')


		if form.instance.date.year > datetime.datetime.now(pytz.timezone('US/Eastern')).year:
			form.instance.person = self.request.user
			form.instance.name = self.request.user.profile.get_display_id()
			return super().form_valid(form)

		elif form.instance.date.year == datetime.datetime.now(pytz.timezone('US/Eastern')).year:
			if form.instance.date.month > datetime.datetime.now(pytz.timezone('US/Eastern')).month:
				form.instance.person = self.request.user
				form.instance.name = self.request.user.profile.get_display_id()
				return super().form_valid(form)

			elif form.instance.date.month == datetime.datetime.now(pytz.timezone('US/Eastern')).month:
				if form.instance.date.day > datetime.datetime.now(pytz.timezone('US/Eastern')).day:
					form.instance.person = self.request.user
					form.instance.name = self.request.user.profile.get_display_id()
					return super().form_valid(form)

				elif form.instance.date.day == datetime.datetime.now().day:
					if form.instance.start_time > datetime.datetime.now(pytz.timezone('US/Eastern')).time():
						form.instance.person = self.request.user
						form.instance.name = self.request.user.profile.get_display_id()
						return super().form_valid(form)

					else:
						messages.error(self.request, 'You cannot schedule a trip in the past (Time)!')
						return redirect('tigertravel-home')



				else:
					messages.error(self.request, 'You cannot schedule a trip in the past (Day)!')
					return redirect('tigertravel-home')

			else:
				messages.error(self.request, 'You cannot schedule a trip in the past! (Month)')
				return redirect('tigertravel-home')

		else:	
			messages.error(self.request, 'You cannot schedule a trip in the past! (Year)')
			return redirect('tigertravel-home')

	def get_success_url(self):
		for group in Group.objects.all():
			if group.date < datetime.datetime.now(pytz.timezone('US/Eastern')).date():
				group.delete()

			elif group.date == datetime.datetime.now(pytz.timezone('US/Eastern')).date():
				if group.start_time < datetime.datetime.now(pytz.timezone('US/Eastern')).time():
					group.delete()

		changed = False
		for group in Group.objects.all():
			if (group.date == self.object.date and group.destination == self.object.destination) and group.origin == self.object.origin:
				if self.object.end_time > group.start_time and self.object.start_time < group.end_time:
					if len(group.members.all()) < 6:

						changed = True
						# updates time range
						if self.object.start_time > group.start_time:
							group.start_time = self.object.start_time
						if self.object.end_time < group.end_time:
							group.end_time = self.object.end_time
						# adds member

						#CHANGED
						group.members.add(self.object)
						group.save()
						email_list = []

						for member in group.members.all():
							email_list.append(member.person.email)

						message = 'Your group has been changed! ' + self.request.user.profile.get_display_id() + ' has joined your trip from ' + group.origin + 'to ' + group.destination + ' on ' + group.date.strftime("%A %d, %B %Y") + '!\nDeparture is scheduled between ' + group.start_time.strftime('%I:%M %p') + ' and ' + group.end_time.strftime('%I:%M %p')

						gmailUser = 'tigertravel333@gmail.com'
						gmailPassword = '3Tiger3Travel3'
						recipient = email_list
						msg = MIMEMultipart()
						msg['From'] = gmailUser
						msg['To'] = recipient
						msg['Subject'] = "New Group"
						msg.attach(MIMEText(message))

						mailServer = smtplib.SMTP('smtp.gmail.com', 587)
						mailServer.ehlo()
						mailServer.starttls()
						mailServer.ehlo()
						mailServer.login(gmailUser, gmailPassword)
						mailServer.sendmail(gmailUser, recipient, msg.as_string())
						mailServer.close()
						break

		# if no group intersects, create new one
		if changed == False:
			new_group = Group.objects.create(origin=self.object.origin, destination=self.object.destination, 
				date=self.object.date, start_time=self.object.start_time,
				end_time=self.object.end_time)

			#CHANGED
			new_group.members.add(self.object)
			new_group.save()

			gmailUser = 'tigertravel333@gmail.com'
			gmailPassword = '3Tiger3Travel3'
			recipient = 'shauryag@princeton.edu'
			print(self.object.person.email)
			msg = MIMEMultipart()
			msg['From'] = gmailUser
			msg['To'] = recipient
			msg['Subject'] = "New Group"
			message = 'You have created a new group! You will be emailed when other people join!\nYour trip is scheduled from ' + new_group.origin + 'to' + new_group.destination + ' on ' + new_group.date.strftime("%A %d, %B %Y") + '.\n' + 'Departure is scheduled between ' + new_group.start_time.strftime('%I:%M %p') + ' and ' + new_group.end_time.strftime('%I:%M %p')
			msg.attach(MIMEText(message))

			mailServer = smtplib.SMTP('smtp.gmail.com', 587)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(gmailUser, gmailPassword)
			mailServer.sendmail(gmailUser, recipient, msg.as_string())
			mailServer.close()

		return super().get_success_url()

class RequestListView(ListView):
	model = Request
	context_object_name = 'posts'
	ordering = ['date']


class GroupListView(ListView):
	model = Group
	ordering = ['date']

	def get_context_data(self):
		for group in Group.objects.all():
			if group.date == datetime.datetime.now(pytz.timezone('US/Eastern')).date() and group.start_time < datetime.datetime.now(pytz.timezone('US/Eastern')).time():
					for request in group.members.all():
						request.delete()
					group.delete()

		return super().get_context_data()

class GroupDetailView(DetailView):
	model = Group

class RequestDeleteView(DeleteView):
	model = Request
	success_url = reverse_lazy('tigertravel-listings')

	def delete(self, *args, **kwargs):
		group = self.get_object().group_set.first()

		if (group.members.first() == self.get_object()):
			max = group.members.last().start_time

		else:
			max = group.members.first().start_time

		for i in group.members.all():
			if i.start_time > max and i != self.get_object():
				max = i.start_time
		group.start_time = max
		group.save()


		if (group.members.first() == self.get_object()):
			min = group.members.last().end_time

		else:
			min = group.members.first().end_time

		for i in group.members.all():
			if i.end_time < min and i != self.get_object():
				min = i.end_time
		group.end_time = min
		group.save()

		email_list = []

		for member in group.members.all():
			if member != self.get_object():
				email_list.append(member.person.email)

		message = 'Your group has been changed! ' + self.request.user.profile.get_display_id() + ' has left your trip from ' + group.origin + 'to' + group.destination + ' on ' + group.date.strftime("%A %d, %B %Y") + '!\nDeparture is now scheduled between ' + group.start_time.strftime('%I:%M %p') + ' and ' + group.end_time.strftime('%I:%M %p')

		send_mail(

		'Your TigerTravel Group', 

		message, 

		'tigertravel333@gmail.com',

		email_list,

		fail_silently=False,

		)

		if len(group.members.all()) == 1:
			group.delete()

		return super(RequestDeleteView, self).delete(*args, **kwargs)












		