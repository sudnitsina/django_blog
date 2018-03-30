# -*- coding: utf-8 -*-

from django import forms
from .models import Post
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags',)
