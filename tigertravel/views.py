from django.shortcuts import render
from .models import Request, Group
from django.views.generic import CreateView, ListView
from django.contrib import messages

class RequestCreateView(CreateView):
	model = Request
	fields = ['destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/mainpage.html'

	def form_valid(self, form):
		form.instance.person = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		changed = False
		for group in Group.objects.all():
			if group.date == self.object.date and group.destination == self.object.destination:
				if self.object.end_time > group.start_time and self.object.start_time < group.end_time:
					#work on max group number
					changed = True
					if self.object.start_time > group.start_time:
						group.start_time = self.object.start_time
					if self.object.end_time < group.end_time:
						group.end_time = self.object.end_time
					#add member name
					group.save()
					break

		if changed == False:
			new_group = Group(destination=self.object.destination, 
				date=self.object.date, start_time=self.object.start_time,
				end_time=self.object.end_time)
			new_group.save()
		return super().get_success_url()

class RequestListView(ListView):
	model = Request
	template_name = 'tigertravel/about.html'
	context_object_name = 'posts'
	ordering = ['date']

class GroupListView(ListView):
	model = Group
	ordering = ['date']


		