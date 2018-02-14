import hashlib

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User  # FIXME: Use AUTH_USER_MODEL instead
from django.contrib.auth import get_user_model

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from sortedm2m.fields import SortedManyToManyField

from . import utils


class Department(models.Model):
    code = models.CharField('代码', max_length=3)
    name = models.CharField('名称', max_length=100)
    linkmen = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='召集人')

    def __str__(self):
        return f'{self.code} {self.name}'

    class Meta:
        verbose_name = '院系'
        verbose_name_plural = '院系'
        ordering = ['code']


class Clazz(models.Model):
    name = models.CharField('名称', max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='院系')
    linkmen = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='召集人')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'
        ordering = ['name']


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField('学号', max_length=10)
    name = models.CharField('姓名', max_length=100)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField('出生日期', null=True)
    enroll_year = models.IntegerField('入学年份', default=2004)
    graduate_year = models.IntegerField('毕业年份', default=2008)
    clazzes = SortedManyToManyField(Clazz, verbose_name='班级')
    major = models.CharField('专业', max_length=100)
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
    remark = models.CharField('备注', max_length=250, blank=True, help_text='如果以上内容有特殊情况的，可在备注栏中说明。例如：学籍信息有误；有转系情况；有多个手机号、邮箱；有多个常住地等。')

    @property
    def clazz(self):
        return self.clazzes.first().name

    @property
    def clazz_list(self):
        return [c.name for c in self.clazzes.all()]

    @property
    def department(self):
        return self.clazzes.first().department.name

    @property
    def department_list(self):
        d = [c.department.name for c in self.clazzes.all()]
        return utils.unique(d)

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
    if profile.clazz:
        path = f'uploads/{profile.department}/{profile.clazz}/{profile.student_id}.jpg'
    else:
        path = f'uploads/{profile.department}/{profile.student_id}.jpg'
    return path


class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attend = models.NullBooleanField('是否参加秩年校庆活动', help_text='全校秩年校庆活动安排在2018年4月29日，欢迎各位返校参与。')
    email_prefix = models.CharField('校友邮箱用户名前缀', max_length=32, unique=True, blank=True, null=True,
        validators=[RegexValidator(r'^[A-Za-z][A-Za-z_-]*[A-Za-z]$', '邮箱用户名前缀不合法。')],
        help_text='如果要开通 @tsinghua.org.cn 校友邮箱，请填写想要的用户名前缀。用户名前缀的合法字符包括英文字母、减号和下划线。英文字母不区分大小写，用户名将自动加入 04 作为后缀。')
    photo = ProcessedImageField(
        verbose_name='校友卡证件照', blank=True, upload_to=get_photo_upload_path,
        help_text='如要要办理校友卡，请上传证件照。要求为近期免冠彩色照，白底，竖版。上传后系统将自动把照片调整为400×500的尺寸。',
        processors=[ResizeToFill(400, 500)],
        format='JPEG',
        options={'quality': 95},
    )

    class Meta:
        verbose_name = '额外信息'
        verbose_name_plural = '额外信息'

def check_permission(user, obj):
    if user.is_superuser:
        return True
    if isinstance(obj, Department):
        return obj.linkmen.filter(id=user.id).exists()
    elif isinstance(obj, Clazz):
        return obj.linkmen.filter(id=user.id).exists() or check_permission(user, obj.department)
    elif isinstance(obj, get_user_model()):
        if user.id == obj.id:
            return True
        for class_ in obj.profile.clazzes.all():
            if check_permission(user, class_):
                return True
        return False
    else:
        return False

def get_linked_classes(user):
    if user.is_superuser:
        return Clazz.objects.all()
    classes = set()
    for d in user.department_set.all():
        classes.update(d.clazz_set.all())
    for c in user.clazz_set.all():
        classes.add(c)
    return sorted(classes, key=lambda c: c.name)
