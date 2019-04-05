from django.shortcuts import render
from .models import Request
from django.views.generic import CreateView, ListView
from django.contrib import messages


def home(request):
	if request.method == 'POST':
		messages.success(request, f'Success! Trip submited!')

	return render(request, 'tigertravel/mainpage.html')

class RequestCreateView(CreateView):
	model = Request
	fields = ['destination', 'date', 'start_time', 'end_time']
	template_name = 'tigertravel/mainpage.html'

	def form_valid(self, form):
		form.instance.person = self.request.user
		return super().form_valid(form)

def about(request):
	context = {
		'posts': Request.objects.all(),
		'title': 'About'
	}
	return render(request, 'tigertravel/about.html', context)

class RequestListView(ListView):
	model = Request
	template_name = 'tigertravel/about.html'
	context_object_name = 'posts'
	ordering = ['-date']


		