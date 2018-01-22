from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Profile, Extra


class LocationWidget(forms.widgets.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.TextInput(attrs=attrs),
            forms.widgets.TextInput(attrs=attrs),
            forms.widgets.TextInput(attrs=attrs),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            values = value.split('|')
        else:
            values = ['', '', '']
        return values

    class Media:
        js = (
            'js/location.js',
        )


class LocationField(forms.MultiValueField):

    def __init__(self, **kwargs):
        # XXX: MultiValueField doesn't need max_length
        del kwargs['max_length']
        error_messages = {}
        fields = (
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        super().__init__(error_messages=error_messages, fields=fields, require_all_fields=False, widget=LocationWidget, **kwargs)

    def compress(self, data_list):
        return '|'.join(data_list)


class ProfileForm(forms.ModelForm):
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
        field_classes = {
            'location': LocationField,
        }


class ExtraForm(forms.ModelForm):

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
