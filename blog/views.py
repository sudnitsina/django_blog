from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils import timezone

from .models import Post
from .forms import PostForm


def post_list(request, tag_slug=None):
    if request.user.is_authenticated():
        list_ = Post.objects.order_by('-created_date')
    else:
        list_ = Post.objects.filter(published_date__lte=timezone.now()
                                    ).order_by('-published_date')
    if tag_slug is not None:
        list_ = list_.filter(tags__slug=tag_slug)
    search_query = ''
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        list_ = Post.objects.filter(
            Q(title__contains=search_query) | Q(text__contains=search_query)
        ).order_by('-published_date')
    paginator = Paginator(list_, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render_to_response('blog/post_list.html',
                              {'posts': posts, 'search_query': search_query})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = post.tags.names()
    if request.POST.get('action') == 'delete':
        if request.user.is_authenticated():
            post.delete()
            return redirect('/')
        else:
            return redirect('/admin/login/?next=/post/' + pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'tags': tags})


@login_required(login_url="/admin/login/?next=/")
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                form.save_m2m()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url="/admin/login/?next=/")
def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                form.save_m2m()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
