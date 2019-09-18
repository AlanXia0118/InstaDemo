from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from Insta.models import Post
"""
Create your views here.
"""

class PostView(ListView):
    # 需要@Override的属性
    model = Post
    template_name = "index.html"

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

class HelloWorld(TemplateView):
    template_name = 'test.html'
