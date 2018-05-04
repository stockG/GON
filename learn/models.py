from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    topic = models.ForeignKey(Topic)
    text = RichTextUploadingField(null=True, blank=True)
    # text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text[:50] + '...'

# 标签
class Tag(models.Model):
    '''tag(标签)对应的数据库model'''
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.name

# blog
class ArticleManager(models.Manager):
    """
       继承自默认的 Manager ，为其添加一个自定义的 archive 方法
    """
    def distinct_date(self):
        distinct_date_list = [] # 该管理器定义了一个distinct_date方法，目的是找出所有的不同日期
        date_list = self.values('created_time') # 根据文章字段created_time找出所有文章的发布时间
        for date in date_list:
            date = date['created_time'].strftime('%Y/%m')  # 取出一个日期改格式为 ‘xxx年/xxx月 存档’
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

class Article(models.Model):
    '''博文'''
    title = models.CharField('标题', max_length=70)
    sub_title = models.CharField('副标题', max_length=70)
    text = RichTextUploadingField('内容',null=True, blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    objects = ArticleManager()  # 在模型中使用自定义的管理器

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.title
