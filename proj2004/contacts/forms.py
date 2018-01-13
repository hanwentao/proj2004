from django.forms import ModelForm

from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'enroll_year', 'graduate_year', 'department', 'major', 'clazz', 'industry', 'organization', 'position', 'title', 'mobile', 'wechat', 'telephone', 'location', 'address', 'postcode']
