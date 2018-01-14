from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User.username is used as student id
    name = models.CharField('姓名', max_length=100)
    enroll_year = models.IntegerField('入学年份', default=2004)
    graduate_year = models.IntegerField('毕业年份', default=2008)
    department = models.CharField('院系', max_length=100)
    major = models.CharField('专业', max_length=100)
    # class is a keyword in Python
    clazz = models.CharField('班级', max_length=100)
    industry = models.CharField('所在行业', max_length=100, blank=True)
    organization = models.CharField('工作单位', max_length=100, blank=True)
    position = models.CharField('职务', max_length=100, blank=True)
    title = models.CharField('职称', max_length=100, blank=True)
    mobile = models.CharField('手机', max_length=100, blank=True)
    # Field email is already in model User
    wechat = models.CharField('微信号', max_length=100, blank=True)
    telephone = models.CharField('固定电话', max_length=100, blank=True)
    location = models.CharField('所在地区', max_length=100, blank=True)
    address = models.CharField('通讯地址', max_length=100, blank=True)
    postcode = models.CharField('邮编', max_length=100, blank=True)

    @property
    def student_id(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.student_id})

    def __str__(self):
        return self.name + ' ' + self.student_id + ' ' + self.clazz

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'
        ordering = ['name']
