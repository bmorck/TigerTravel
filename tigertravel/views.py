from django.shortcuts import render
from .models import Post


def home(request):
	return render(request, 'tigertravel/mainpage.html')

def about(request):
	context = {
		'posts': Post.objects.all(),
		'title': 'About'
	}
	return render(request, 'tigertravel/about.html', context)
