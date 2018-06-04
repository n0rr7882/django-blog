from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from mistune import markdown
import re

import mysite.settings as settings


def markdown_to_plaintext_in_post(post):

    post.content = re.sub(r'<.*?>', '', markdown(post.content))
    return post


def tagstring_to_taglist_in_post(post):

    post.tags = map(lambda tag: tag.strip(), post.tags.split(','))
    return post


def post_list(request):

    page = int(request.GET['page']) if 'page' in request.GET.keys() else 1
    tag = request.GET['tag'] if 'tag' in request.GET.keys() else ''

    posts = Post.objects.order_by('-created_at')
    posts = posts.filter(tags__contains=tag) if tag else posts
    posts = posts[(page - 1) * 10:page * 10]

    posts = list(map(markdown_to_plaintext_in_post, posts))
    posts = list(map(tagstring_to_taglist_in_post, posts))

    return render(request, 'blog/post_list.html', {
        'constants': settings,
        'posts': posts,
        'page': page,
        'tag': tag
    })


def post_detail(request, idx):

    post = get_object_or_404(Post, idx=int(idx))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', idx=idx)

    post = tagstring_to_taglist_in_post(post)
    post.content = markdown(post.content)

    form = CommentForm()
    comments = Comment.objects.filter(post=post.idx).order_by('-created_at')

    return render(request, 'blog/post_detail.html', {
        'constants': settings,
        'post': post,
        'comments': comments,
        'form': form
    })
