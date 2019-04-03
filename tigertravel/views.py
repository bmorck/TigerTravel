from django.shortcuts import render

posts = [
	{
		'author': 'me',
		'title': 'one post',
		'content': 'blah blah blah',
		'date_posted': 'March 31, 2019'
	},
	{
		'author': 'you',
		'title': 'two post',
		'content': 'blah blah blah',
		'date_posted': 'April 1, 2019'
	}
]

def home(request):
	return render(request, 'tigertravel/mainpage.html')

def about(request):
	context = {
		'posts': posts,
		'title': 'About'
	}
	return render(request, 'tigertravel/about.html', context)
