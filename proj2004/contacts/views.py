from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth.models import User

from .forms import ProfileForm


def index(request):
    return render(request, 'contacts/index.html')

def profile(request, username):
    code = request.GET.get('code', '')
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if code != profile.verification_code:
        return HttpResponseForbidden('Invalid verification code')
    form = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(profile.get_absolute_url() + f'?code={profile.verification_code}')
    if form is None:
        form = ProfileForm(instance=profile)
    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'contacts/profile.html', context)
