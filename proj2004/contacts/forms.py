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

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['email_prefix'] = cleaned_data['email_prefix'].lower()
        return cleaned_data

    class Meta:
        model = Extra
        fields = [
            'attend',
            'email_prefix',
            'photo',
        ]
