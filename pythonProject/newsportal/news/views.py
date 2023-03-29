from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Author, Post, Category, Comment, PostCategory
from .filters import PostFilter
from django_filters.views import FilterView


class PostList(ListView):
    model = Post
    ordering = '-creationDate'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 20


class PostDetail(DetailView):
    model = Post
    template_name = 'firstnews.html'
    context_object_name = 'firstnews'

