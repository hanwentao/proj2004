from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    Department,
    Class,
    Profile,
    check_permission,
)
from .forms import (
    ProfileForm,
    ExtraForm,
    SetPasswordForm,
    PasswordResetForm,
)

def home(request):
    context = {
        'nav': ('home',),
    }
    return render(request, 'contacts/home.html', context)

@login_required
def profile(request, username):
    obj = get_object_or_404(get_user_model(), username=username)
    user = request.user
    if not check_permission(user, obj):
        return HttpResponseForbidden('无权访问该校友的信息。')
    profile = obj.profile
    extra = obj.extra
    context = {
        'nav': ('profile', username),
        'edit': False,
        'change_button': username == user.username,
        'profile': profile,
        'extra': extra,
    }
    return render(request, 'contacts/profile.html', context)

def profile_edit(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    password_set = user.has_usable_password()
    profile = user.profile
    if not request.user.is_superuser:
        if password_set:
            if not request.user.is_authenticated:
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            if username != request.user.username:
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
        'nav': ('profile', username),
        'edit': True,
        'profile': profile,
        'extra': extra,
        'profile_form': profile_form,
        'extra_form': extra_form,
        'set_password_form': set_password_form,
    }
    return render(request, 'contacts/profile.html', context)

@login_required
def class_detail(request, id_or_name):
    if isinstance(id_or_name, int):
        class_ = get_object_or_404(Class, id=id_or_name)
    else:
        class_ = get_object_or_404(Class, name=id_or_name)
    user = request.user
    if not check_permission(user, class_):
        return HttpResponseForbidden('无权访问该班级页面。')
    profiles = class_.profile_set.filter(user__is_active=True)
    context = {
        'nav': ('class_detail', class_.name),
        'name': class_.name,
        'profiles': profiles,
    }
    return render(request, 'contacts/class_detail.html', context)

@login_required
def department_list(request, id_or_code_or_name):
    if isinstance(id_or_code_or_name, int):
        department = get_object_or_404(Department, id=id_or_code_or_name)
    elif len(id_or_code_or_name) == 3 and id_or_code_or_name.isdigit():
        department = get_object_or_404(Department, code=id_or_code_or_name)
    else:
        department = get_object_or_404(Department, name=id_or_code_or_name)
    user = request.user
    if not check_permission(user, department):
        return HttpResponseForbidden('无权访问该院系页面。')
    classes = department.clazz_set.all()
    profiles = set()
    for class_ in classes:
        profiles.update(class_.profile_set.all())
    profiles = list(profiles)
    profiles.sort(key=lambda p: p.student_id)
    context = {
        'nav': ('list', department.name),
        'name': department.name,
        'profiles': profiles,
    }
    return render(request, 'contacts/list.html', context)

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            user.extra.password_reset = timezone.now()
            user.extra.save()
            return redirect('password_reset_commit')
    else:
        form = PasswordResetForm()
    context = {
        'form': form,
    }
    return render(request, 'contacts/password_reset.html', context)

def password_reset_commit(request):
    return render(request, 'contacts/password_reset_commit.html')

@login_required
def password_reset_approve(request):
    current_user = request.user
    if not current_user.linked_classes:
        return HttpResponseForbidden('无权访问管理页面。')
    User = get_user_model()
    if request.method == 'POST':
        for username_list in request.POST.getlist('approved'):
            for username in username_list.split(','):
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    pass
                else:
                    if check_permission(current_user, user, False):
                        # XXX: Needs transaction here?
                        user.set_unusable_password()
                        user.save()
                        user.extra.password_reset = None
                        user.extra.save()
        for username in request.POST.getlist('canceled'):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                if check_permission(current_user, user, False):
                    user.extra.password_reset = None
                    user.extra.save()
        return redirect('password_reset_approve')
    users = [u for u in User.objects.filter(extra__password_reset__isnull=False)
               if check_permission(current_user, u, False)]
    context = {
        'nav': ('password_reset_approve',),
        'users': users,
    }
    return render(request, 'contacts/password_reset_approve.html', context)

@login_required
def overview(request):
    if not request.user.is_superuser or not request.user.is_staff:
        return HttpResponseForbidden('无权访问管理页面。')
    context = {
        'nav': ('overview',),
        'departments': Department.objects.all(),
    }
    return render(request, 'contacts/overview.html', context)
