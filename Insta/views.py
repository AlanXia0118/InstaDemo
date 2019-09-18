from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from Insta.models import Post
"""
Create your views here.
"""

class PostView(ListView):
    # 需要@Override的属性
    model = Post
    template_name = "index.html"




class HelloWorld(TemplateView):
    template_name = 'test.html'
