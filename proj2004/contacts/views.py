from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import ProfileForm


def index(request):
    return render(request, 'contacts/index.html')

def profile(request, username):
    user = User.objects.get(username=username)
    form = ProfileForm(instance=user.profile)
    return render(request, 'contacts/profile.html', locals())
