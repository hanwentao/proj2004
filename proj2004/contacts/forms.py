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
        if cleaned_data.get('email_prefix', ''):
            cleaned_data['email_prefix'] = cleaned_data['email_prefix'].lower()
        return cleaned_data

    class Meta:
        model = Extra
        fields = [
            'attend',
            'email_prefix',
            'photo',
        ]
        error_messages = {
            'email_prefix': {
                'unique': '该邮箱用户名前缀已经被其他用户登记使用。',
            }
        }
