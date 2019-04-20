from django.shortcuts import render
from .models import Request, Group
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
import datetime
from django.shortcuts import redirect

class RequestCreateView(CreateView):
	model = Request
	fields = ['destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/mainpage.html'

	def form_valid(self, form):
		if form.instance.date.year > datetime.datetime.now().year:
			form.instance.person = self.request.user
			form.instance.name = self.request.user.profile.get_display_id()
			return super().form_valid(form)

		elif form.instance.date.year == datetime.datetime.now().year:
			if form.instance.date.month > datetime.datetime.now().month:
				form.instance.person = self.request.user
				form.instance.name = self.request.user.profile.get_display_id()
				return super().form_valid(form)

			elif form.instance.date.month == datetime.datetime.now().month:
				if form.instance.date.day >= datetime.datetime.now().day:
					form.instance.person = self.request.user
					form.instance.name = self.request.user.profile.get_display_id()
					return super().form_valid(form)
				else:
					return redirect('tigertravel-home')

			else:
				return redirect('tigertravel-home')

		else:	
			return redirect('tigertravel-home')

	def get_success_url(self):
		changed = False
		for group in Group.objects.all():
			if group.date == self.object.date and group.destination == self.object.destination:
				if self.object.end_time > group.start_time and self.object.start_time < group.end_time:

					# WORK ON MAX NUMBER AND UPDATE LISTING INSTEAD OF ADDING NEW

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
					break
		# if no group intersects, create new one
		if changed == False:
			new_group = Group.objects.create(destination=self.object.destination, 
				date=self.object.date, start_time=self.object.start_time,
				end_time=self.object.end_time)

			#CHANGED
			new_group.members.add(self.object)
			new_group.save()
		return super().get_success_url()

class RequestListView(ListView):
	model = Request
	context_object_name = 'posts'
	ordering = ['date']


class GroupListView(ListView):
	model = Group
	ordering = ['date']

class GroupDetailView(DetailView):
	model = Group




		