from django import forms

from .models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'content')
