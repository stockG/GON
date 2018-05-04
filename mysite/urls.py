"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from learn import views as learn_views
from users import views as users_views
from django.contrib.auth.views import login

urlpatterns = [
    # 主页
    url(r'^$', learn_views.home, name='home'),
    # 小游戏lovelive对对碰
    url(r'^game/$', learn_views.game, name='game'),
    # 新番季度动画
    url(r'^animate/$', learn_views.animate, name='animate'),
    # 个人简历
    url(r'^resume/$', learn_views.resume, name='resume'),
    # 博客
    url(r'^blog/$', learn_views.blog, name='blog'),
    # 博客文章内容
    url(r'^blog_main/(?P<article_id>\d+)$', learn_views.blog_main, name='blog_main'),
    # 博客tags
    url(r'^blog/tags$', learn_views.blog_tags, name='tags'),
    # 博客按月分类
    url(r'^archive/$', learn_views.blog_archive, name='archive'),
    # 博客about
    url(r'^blog/about$', learn_views.blog_about, name='blog_about'),
    # 显示所有的主题
    url(r'^topics/$', learn_views.topics, name='topics'),
    # 显示特定主题详细页面
    url(r'^topics/(?P<topic_id>\d+)/$', learn_views.topic, name='topic'),
    # 用于添加新主题的网页
    url(r'^new_topic/$', learn_views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$', learn_views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', learn_views.edit_entry, name='edit_entry'),
    # 登录页面
    url(r'^users/login/$', login, {'template_name': 'login.html'}, name='login'),
    # 注销页面
    url(r'^users/logout/$', users_views.blogLogout, name='logout'),
    # 注册页面
    url(r'^register/$', users_views.register, name='register'),
    url(r'^admin/', admin.site.urls),
    # 富文本编辑器
    url(r'ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
