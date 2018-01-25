import hashlib

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField('学号', max_length=10)
    name = models.CharField('姓名', max_length=100)
    enroll_year = models.IntegerField('入学年份', default=2004)
    graduate_year = models.IntegerField('毕业年份', default=2008)
    department = models.CharField('院系', max_length=100)
    major = models.CharField('专业', max_length=100)
    clazz = models.CharField('班级', max_length=100)
    industry = models.CharField('所在行业', max_length=100, blank=True)
    organization = models.CharField('工作单位', max_length=100, blank=True, help_text='请填写工作单位的官方全称。')
    position = models.CharField('职务', max_length=100, blank=True)
    title = models.CharField('职称', max_length=100, blank=True)
    mobile = PhoneNumberField('手机', blank=True, help_text='请填写中国大陆格式（固话须带区号）或国际格式（以加号开头）的电话号码，结果将统一为国际格式。')
    email = models.EmailField('电子邮箱', blank=True)
    wechat = models.CharField('微信号', max_length=100, blank=True, help_text='查看微信号的方法：打开微信→我→微信号。')
    telephone = PhoneNumberField('固定电话', blank=True, help_text='请填写中国大陆格式（固话须带区号）或国际格式（以加号开头）的电话号码，结果将统一为国际格式。')
    location = models.CharField('所在地区', max_length=100, blank=True)
    address = models.CharField('通讯地址', max_length=250, blank=True, help_text='请填写完整、规范的通讯地址。如在国外，可使用外文地址。')
    postcode = models.CharField('邮编', max_length=100, blank=True)

    @property
    def verification_code(self):
        m = hashlib.md5()
        m.update(self.student_id.encode())
        m.update(self.name.encode())
        m.update(settings.SECRET_KEY.encode())
        return m.hexdigest()[:6]

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    def __str__(self):
        return f'{self.student_id} {self.name} {self.clazz}'

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'
        ordering = ['student_id']

def get_photo_upload_path(instance, filename):
    profile = instance.user.profile
    return f'uploads/{profile.clazz}/{profile.name}/{filename}'


class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attend = models.NullBooleanField('是否参加秩年校庆活动', help_text='全校秩年校庆活动安排在2018年4月29日。')
    email_prefix = models.CharField('校友邮箱用户名前缀', max_length=32, unique=True, blank=True, null=True,
        validators=[RegexValidator(r'^[A-Za-z][A-Za-z_-]*[A-Za-z]$', '邮箱用户名前缀不合法。')],
        help_text='如果要开通 @tsinghua.org.cn 校友邮箱，请填写想要的用户名前缀。用户名前缀的合法字符包括英文字母、减号和下划线。英文字母不区分大小写，用户名将自动加入 04 作为后缀。')
    photo = models.ImageField('校友卡证件照', blank=True, upload_to=get_photo_upload_path, help_text='如要要办理校友卡，请上传证件照。')

    class Meta:
        verbose_name = '额外信息'
        verbose_name_plural = '额外信息'
