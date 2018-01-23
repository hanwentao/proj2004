from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import (
    ProfileForm,
    ExtraForm,
    SetPasswordForm,
)


def home(request):
    context = {
        'page': 'home',
    }
    return render(request, 'contacts/home.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    password_set = user.has_usable_password()
    profile = user.profile
    if not request.user.is_superuser:
        if password_set:
            if not request.user.is_authenticated:
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            if username != request.user.username:
                print(username, repr(request.user.username))
                return HttpResponseForbidden('你不能访问其他人的个人信息。')
        else:
            code = request.GET.get('code', '')
            if code != profile.verification_code:
                return HttpResponseForbidden('验证码错误，请与贵班联系人确认网址信息。')
    extra = user.extra
    profile_form = None
    extra_form = None
    set_password_form = None
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        extra_form = ExtraForm(request.POST, request.FILES, instance=extra)
        if not request.user.is_superuser and not password_set:
            set_password_form = SetPasswordForm(user, request.POST)
        if (profile_form.is_valid() and extra_form.is_valid() and
            (request.user.is_superuser or password_set or set_password_form.is_valid())):
            profile_form.save()
            extra_form.save()
            if not request.user.is_superuser and not password_set:
                set_password_form.save()
                login(request, user)
            return redirect(profile)
    if profile_form is None:
        profile_form = ProfileForm(instance=profile)
    if extra_form is None:
        extra_form = ExtraForm(instance=extra)
    if not request.user.is_superuser and set_password_form is None:
        set_password_form = SetPasswordForm(user)
    context = {
        'page': 'profile',
        'profile': profile,
        'extra': extra,
        'profile_form': profile_form,
        'extra_form': extra_form,
        'set_password_form': set_password_form,
    }
    return render(request, 'contacts/profile.html', context)
