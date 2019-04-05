from django.shortcuts import render
from .models import Request
from django.views.generic import CreateView, ListView
from django.contrib import messages

class RequestCreateView(CreateView):
	model = Request
	fields = ['destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/mainpage.html'

	def form_valid(self, form):
		form.instance.person = self.request.user
		return super().form_valid(form)

class RequestListView(ListView):
	model = Request
	template_name = 'tigertravel/about.html'
	context_object_name = 'posts'
	ordering = ['date']


		