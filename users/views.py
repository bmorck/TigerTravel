from django.shortcuts import render
from uniauth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
@login_required
def profile(request):
	return render(request, 'users/profile.html')
	

	