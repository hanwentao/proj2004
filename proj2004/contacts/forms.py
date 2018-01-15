from django.forms import ModelForm

from .models import Profile, Extra


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'industry',
            'organization',
            'position',
            'title',
            'mobile',
            'email',
            'wechat',
            'telephone',
            'location',
            'address',
            'postcode',
        ]


class ExtraForm(ModelForm):
    class Meta:
        model = Extra
        fields = [
            'attend',
        ]
