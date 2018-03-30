# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Post
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def post_list(request, page='1', tag_slug=None):
    if tag_slug is None:
        post_list = Post.objects.filter(
            published_date__lte=timezone.now()
            ).order_by('-published_date') #[int(page)*5-5:int(page)*5]
    else:
        post_list = Post.objects.filter(
            tags__slug=tag_slug
            ).order_by('-published_date')
    search_query = ''
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__contains = request.GET.get('search')) | Q(
            text__contains = request.GET.get('search'))
            ).order_by('-published_date')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render_to_response('blog/post_list.html',
                                {'posts': posts, 'search_query': search_query}
                              )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = post.tags.names()
    if request.POST.get('action') == 'delete':
        if request.user.is_authenticated():
            post.delete()
            return redirect('/')
        else:
            return redirect('/admin/login/?next=/post/' + pk)
    return render(request, 'blog/post_detail.html',
                    {'post': post, 'tags': tags}
                  )


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
            form = PostForm(request.POST, instance = post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                form.save_m2m()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
