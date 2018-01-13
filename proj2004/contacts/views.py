from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .forms import ProfileForm


def index(request):
    return render(request, 'contacts/index.html')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    form = ProfileForm(instance=user.profile)
    context = {
        'form': form,
    }
    return render(request, 'contacts/profile.html', context)
