from django.contrib import admin

# Register your models here.
from learn.models import Topic, Entry, Article, Tag

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Article)
admin.site.register(Tag)