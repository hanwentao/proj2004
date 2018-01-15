from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth.models import User

from .forms import ProfileForm, ExtraForm


def index(request):
    return render(request, 'contacts/index.html')

def profile(request, username):
    code = request.GET.get('code', '')
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if code != profile.verification_code:
        return HttpResponseForbidden('Invalid verification code')
    extra = user.extra
    profile_form = None
    extra_form = None
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        extra_form = ExtraForm(request.POST, instance=extra)
        if profile_form.is_valid() and extra_form.is_valid():
            profile_form.save()
            extra_form.save()
            return redirect(profile.get_absolute_url() + f'?code={profile.verification_code}')
    if profile_form is None:
        profile_form = ProfileForm(instance=profile)
    if extra_form is None:
        extra_form = ExtraForm(instance=extra)
    context = {
        'user': user,
        'profile': profile,
        'extra': extra,
        'profile_form': profile_form,
        'extra_form': extra_form,
    }
    return render(request, 'contacts/profile.html', context)
