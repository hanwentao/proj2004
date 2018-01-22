from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Profile, Extra

INDUSTRY_CHOICES = (
    '农、林、牧、渔业',
    '采矿业',
    '制造业',
    '电力、热力、燃气及水生产和供应业',
    '建筑业',
    '批发和零售业',
    '交通运输、仓储和邮政业',
    '住宿和餐饮业',
    '信息传输、软件和信息技术服务业',
    '金融业',
    '房地产业',
    '租赁和商务服务业',
    '科学研究和技术服务业',
    '水利、环境和公共设施管理业',
    '居民服务、修理和其他服务业',
    '教育',
    '卫生和社会工作',
    '文化、体育和娱乐业',
    '公共管理、社会保障和社会组织',
    '国际组织',
)


class IndustryWidget(forms.widgets.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.TextInput(attrs=attrs),
            forms.widgets.TextInput(attrs=attrs),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value in INDUSTRY_CHOICES:
            return [value, '']
        elif value:
            if value != '其他':
                return ['其他', value]
            else:
                return ['其他', '']
        else:
            return ['', '']

    class Media:
        js = (
            'js/industry-data.js',
            'js/industry.js',
        )


class IndustryField(forms.MultiValueField):

    def __init__(self, **kwargs):
        del kwargs['max_length']
        error_messages = {}
        fields = (
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        super().__init__(error_messages=error_messages, fields=fields, require_all_fields=False, widget=IndustryWidget, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] != '其他':
                return data_list[0]
            elif len(data_list) > 1 and data_list[1]:
                return data_list[1]
            else:
                return '其他'
        else:
            return ''


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
            'js/location-data.js',
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

        field_classes = {
            'industry': IndustryField,
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
