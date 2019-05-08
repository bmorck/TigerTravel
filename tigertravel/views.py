from django.shortcuts import render
from .models import Request, Group, Comment
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
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
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.urls import reverse

def login(request):
	return render(request, 'tigertravel/login.html')



class RequestCreateView(CreateView):
	model = Request
	fields = ['origin', 'destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/index.html'

	def form_valid(self, form):

		for request in Request.objects.all():
			if self.request.user == request.person and form.instance.date == request.date:
				messages.info(self.request, 'You cannot have two trip requests for the same date!')
				return redirect('tigertravel-home')

		if form.instance.origin == form.instance.destination:
			messages.info(self.request, 'Origin and Destination cannot be the same!')
			return redirect('tigertravel-home')

		if form.instance.start_time > form.instance.end_time:

			messages.error(self.request, 'Start time cannot be after end time!')

			return redirect('tigertravel-home')



		minInterval = datetime.timedelta(minutes=30)

		reqInterval = datetime.timedelta(hours=form.instance.end_time.hour-form.instance.start_time.hour, minutes=form.instance.end_time.minute-form.instance.start_time.minute)

		if (reqInterval.seconds < minInterval.seconds):

			messages.error(self.request, 'Departure interval must be greater than 30 minutes!')

			return redirect('tigertravel-home')


		if form.instance.date.year > datetime.datetime.now(pytz.timezone('US/Eastern')).year:
			form.instance.person = self.request.user
			form.instance.name = self.request.user.person.name
			return super().form_valid(form)

		elif form.instance.date.year == datetime.datetime.now(pytz.timezone('US/Eastern')).year:
			if form.instance.date.month > datetime.datetime.now(pytz.timezone('US/Eastern')).month:
				form.instance.person = self.request.user
				form.instance.name = self.request.user.person.name
				return super().form_valid(form)

			elif form.instance.date.month == datetime.datetime.now(pytz.timezone('US/Eastern')).month:
				if form.instance.date.day > datetime.datetime.now(pytz.timezone('US/Eastern')).day:
					form.instance.person = self.request.user
					form.instance.name = self.request.user.person.name
					return super().form_valid(form)

				elif form.instance.date.day == datetime.datetime.now(pytz.timezone('US/Eastern')).day:
					if form.instance.start_time > datetime.datetime.now(pytz.timezone('US/Eastern')).time():
						form.instance.person = self.request.user
						form.instance.name = self.request.user.person.name
						return super().form_valid(form)

					else:
						messages.info(self.request, 'You cannot schedule a trip in the past (Time)!')
						return redirect('tigertravel-home')



				else:
					messages.info(self.request, 'You cannot schedule a trip in the past (Day)!')
					return redirect('tigertravel-home')

			else:
				messages.info(self.request, 'You cannot schedule a trip in the past! (Month)')
				return redirect('tigertravel-home')

		else:	
			messages.info(self.request, 'You cannot schedule a trip in the past! (Year)')
			return redirect('tigertravel-home')

	def get_success_url(self):
		for group in Group.objects.all():
			if group.date < datetime.datetime.now(pytz.timezone('US/Eastern')).date():
				for request in group.members.all():
					request.delete()
				group.delete()

			elif group.date == datetime.datetime.now(pytz.timezone('US/Eastern')).date():
				if group.start_time < datetime.datetime.now(pytz.timezone('US/Eastern')).time():
					for request in group.members.all():
						request.delete()
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
						temp = int(group.size) + 1
						group.size = str(temp)
						group.save()
						email_list = []

						for member in group.members.all():
							if member != self.object:
								email_list.append(member.person.profile.get_display_id() + '@princeton.edu')

						email_list1 = [self.object.person.profile.get_display_id() + '@princeton.edu']

						message_self = 'Dear ' + self.request.user.person.name + ',\n\nYou have joined a group! \n\nYour trip is scheduled from ' + group.origin + ' to ' + group.destination + ' on ' + group.date.strftime("%A %B %d, %Y") + '. ' + 'Departure is scheduled between ' + group.start_time.strftime('%I:%M %p') + ' and ' + group.end_time.strftime('%I:%M %p') + '. \n\nYou can access your group page at https://tiger-travel.herokuapp.com/groups/' + str(group.id) + '.\n\nCheers!\n\nTigerTravel'
			
						send_mail('TigerTravel Group for ' + group.date.strftime("%B %d, %Y"), message_self, 'TigerTravel <tigertravel333@gmail.com>', 
							email_list1, fail_silently=False,
						)

						message = 'Dear TigerTraveller, \n\nYour group has been changed! ' + self.request.user.person.name + ' has joined your trip from ' + group.origin + ' to ' + group.destination + ' on ' + group.date.strftime("%A %d, %B %Y") + '. Departure is now scheduled between ' + group.start_time.strftime('%I:%M %p') + ' and ' + group.end_time.strftime('%I:%M %p') + '. \n\nYou can access your group page at https://tiger-travel.herokuapp.com/groups/' + str(group.id) + '.\n\nCheers!\n\nTigerTravel'
						send_mail(
						'TigerTravel Group Update for ' + group.date.strftime("%B %d, %Y"),
						message, 
						'TigerTravel <tigertravel333@gmail.com>',
						email_list,
						fail_silently=False,
						)

						
						
						return reverse('group-detail', kwargs={'pk': group.id})

		# if no group intersects, create new one
		if changed == False:
			new_group = Group.objects.create(origin=self.object.origin, destination=self.object.destination, 
				date=self.object.date, start_time=self.object.start_time,
				end_time=self.object.end_time)

			#CHANGED
			new_group.members.add(self.object)
			new_group.save()

			gmailUser = 'tigertravel333@gmail.com'
			gmailPassword = 'TigerTravelTravelTogether333'
			recipient = self.object.person.profile.get_display_id() + '@princeton.edu'
			msg = MIMEMultipart()
			msg['From'] = 'TigerTravel <' + gmailUser + '>'
			msg['To'] = recipient
			msg['Subject'] = "New TigerTravel Group for " + new_group.date.strftime("%B %d, %Y")
			message = 'Dear ' + self.request.user.person.name + ',\n\nYou have created a new group! You will be emailed when other people join. \n\nYour trip is scheduled from ' + new_group.origin + ' to ' + new_group.destination + ' on ' + new_group.date.strftime("%A %B %d, %Y") + '. ' + 'Departure is scheduled between ' + new_group.start_time.strftime('%I:%M %p') + ' and ' + new_group.end_time.strftime('%I:%M %p') + '. \n\nYou can access your group page at https://tiger-travel.herokuapp.com/groups/' + str(new_group.id) + '.\n\nCheers!\n\nTigerTravel'
			msg.attach(MIMEText(message))

			mailServer = smtplib.SMTP('smtp.gmail.com', 587)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(gmailUser, gmailPassword)
			mailServer.sendmail(gmailUser, recipient, msg.as_string())
			mailServer.close()
			return reverse('group-detail', kwargs={'pk': new_group.id})

		return super().get_success_url()

class RequestListView(ListView):
	model = Request
	context_object_name = 'posts'
	ordering = ['date']
	template_name = 'tigertravel/profile.html'

	#purpose of this was to access groups in html
	def get_context_data(self, **kwargs):
		context = super(RequestListView, self).get_context_data(**kwargs)
		context['groups'] = Group.objects.all()
		return context




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

class GroupDetailView(UpdateView):
	model = Group
	fields = ['text']


	def get_success_url(self):
		new_comment = Comment.objects.create(author=self.request.user.person.name, text=self.object.text, sendtime=datetime.datetime.now(pytz.timezone('US/Eastern')))
		new_comment.save()
		self.object.comments.add(new_comment)
		self.object.save()
		return reverse('group-detail', kwargs={'pk': self.object.id})

	def get_context_data(self, **kwargs):
		context = super(GroupDetailView, self).get_context_data(**kwargs)
		context['comments'] = Comment.objects.all()
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


	


class RequestDeleteView(DeleteView):
	model = Request
	success_url = reverse_lazy('tigertravel-profile')

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
		temp = int(group.size) - 1
		group.size = str(temp)
		group.save()

		email_list = []

		for member in group.members.all():
			if member != self.get_object():
				email_list.append(member.person.profile.get_display_id() + '@princeton.edu')

		message = 'Dear TigerTraveller,\n\nYour group has been changed! ' + self.request.user.person.name + ' has left your trip from ' + group.origin + ' to ' + group.destination + ' on ' + group.date.strftime("%A %d, %B %Y") + '. Departure is now scheduled between ' + group.start_time.strftime('%I:%M %p') + ' and ' + group.end_time.strftime('%I:%M %p') + '. \n\nYou can access your group page at https://tiger-travel.herokuapp.com/groups/' + str(group.id) + '.\n\nCheers!\n\nTigerTravel'

		send_mail(

		'TigerTravel Group Update for ' + group.date.strftime("%B %d, %Y"), 

		message, 

		'TigerTravel <tigertravel333@gmail.com>',

		email_list,

		fail_silently=False,

		)

		if len(group.members.all()) == 1:
			group.delete()

		return super(RequestDeleteView, self).delete(*args, **kwargs)