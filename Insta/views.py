from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from Insta.models import Post
"""
Create your views here.
"""

class PostView(ListView):
    """ Return object_list """
    # 需要@Override的属性
    model = Post
    template_name = "index.html"

class PostDetailView(DetailView):
    """ Return object """
    model = Post
    template_name = "post_detail.html"

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostCreateView(CreateView):
    """ Return form """
    model = Post
    # the page creation will be operated
    template_name = "post_create.html"
    # tell user the field they need provide (e.g. titile, image)
    fields = "__all__"