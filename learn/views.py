from django.shortcuts import render
from .models import Topic, Entry, Article, Tag
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'home.html')

def game(request):
    return render(request, 'game.html')

def animate(request):
    return render(request, 'animate.html')

def resume(request):
    return  render(request, 'resume.html')

def blog(request):
    articles = Article.objects.all().order_by('-created_time')
    tagGroup = Tag.objects.all()
    archive_list = Article.objects.distinct_date()  # 文章归档 获取到的列表格式为： xxx年/xxx月 存档
    paginator = Paginator(articles, 5)  # 每页显示5条纪录
    page = request.GET.get('page')  # 获取客户端请求传来的页码
    try:
        articles = paginator.page(page)  # 返回用户请求的页码对象
    except PageNotAnInteger:
        # 如果请求中的page不是数字,也就是为空的情况下
        articles = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
        articles = paginator.page(paginator.num_pages)
    context = {'articles': articles, 'tagGroup': tagGroup, 'archive_list': archive_list}
    return render(request, 'blog.html', context)

def blog_main(request, article_id):
    article = Article.objects.get(id = article_id)
    articles = Article.objects.all().order_by('-created_time')
    tagGroup = Tag.objects.all()
    previous_blog = Article.objects.filter(created_time__gt = article.created_time).first()
    next_blog = Article.objects.filter(created_time__lt = article.created_time).last()
    context = {'article' : article, 'tagGroup' : tagGroup, 'articles': articles, 'previous_blog': previous_blog,'next_blog': next_blog}
    return render(request, 'blog_main.html', context)

def blog_tags(request):
    articles = Article.objects.all().order_by('created_time')
    tagGroup = Tag.objects.all()
    context = {'articles': articles, 'tagGroup': tagGroup}
    return render(request, 'blog_tags.html', context)

def blog_archive(request):
    tagGroup = Tag.objects.all()
    archive_list = Article.objects.distinct_date()
    # 取出两个参数 year,month
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    # 根据参数year,month进行过滤， 字段名+__icontains表大小写不敏感的包含匹配
    article_list = Article.objects.filter(created_time__icontains=year + '-' + month)
    context = {'tagGroup': tagGroup, 'archive_list': archive_list, 'article_list': article_list}
    return render(request, 'blog_archive.html', context)

def blog_about(request):
    tagGroup = Tag.objects.all()
    archive_list = Article.objects.distinct_date()
    context = {'tagGroup': tagGroup, 'archive_list': archive_list}
    return render(request, 'blog_about.html', context)

@login_required
def topics(request):
    '''显示所有主题'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''在特定主题添加新条目'''
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''编辑既有条目'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'edit_entry.html', context)