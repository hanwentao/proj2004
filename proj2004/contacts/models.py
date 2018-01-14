import hashlib

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

INDUSTRY_LIST = (
    ('A', '农、林、牧、渔业'),
    ('B', '采矿业'),
    ('C', '制造业'),
    ('D', '电力、热力、燃气及水生产和供应业'),
    ('E', '建筑业'),
    ('F', '批发和零售业'),
    ('G', '交通运输、仓储和邮政业'),
    ('H', '住宿和餐饮业'),
    ('I', '信息传输、软件和信息技术服务业'),
    ('J', '金融业'),
    ('K', '房地产业'),
    ('L', '租赁和商务服务业'),
    ('M', '科学研究和技术服务业'),
    ('N', '水利、环境和公共设施管理业'),
    ('O', '居民服务、修理和其他服务业'),
    ('P', '教育'),
    ('Q', '卫生和社会工作'),
    ('R', '文化、体育和娱乐业'),
    ('S', '公共管理、社会保障和社会组织'),
    ('T', '国际组织'),
    ('X', '其他'),
)


class Profile(models.Model):
    INDUSTRY_CHOICES = tuple((x[1], x[1]) for x in INDUSTRY_LIST)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField('学号', max_length=10)
    name = models.CharField('姓名', max_length=100)
    enroll_year = models.IntegerField('入学年份', default=2004)
    graduate_year = models.IntegerField('毕业年份', default=2008)
    department = models.CharField('院系', max_length=100)
    major = models.CharField('专业', max_length=100)
    clazz = models.CharField('班级', max_length=100)
    industry = models.CharField('所在行业', max_length=100, choices=INDUSTRY_CHOICES, blank=True)
    organization = models.CharField('工作单位', max_length=100, blank=True)
    position = models.CharField('职务', max_length=100, blank=True)
    title = models.CharField('职称', max_length=100, blank=True)
    mobile = models.CharField('手机', max_length=100, blank=True)
    email = models.EmailField('电子邮箱', blank=True)
    wechat = models.CharField('微信号', max_length=100, blank=True)
    telephone = models.CharField('固定电话', max_length=100, blank=True)
    location = models.CharField('所在地区', max_length=100, blank=True)
    address = models.CharField('通讯地址', max_length=100, blank=True)
    postcode = models.CharField('邮编', max_length=100, blank=True)

    @property
    def verification_code(self):
        m = hashlib.md5()
        m.update(self.student_id.encode())
        m.update(self.name.encode())
        m.update('salt'.encode())
        return m.hexdigest()[:6]

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    def __str__(self):
        return f'{self.student_id} {self.name} {self.clazz}'

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'
        ordering = ['student_id']
