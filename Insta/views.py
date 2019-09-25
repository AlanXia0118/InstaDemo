from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from Insta.models import Post
from django.contrib.auth.forms import UserCreationForm


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

class HomeView(TemplateView):
    template_name = 'home.html'

class PostCreateView(CreateView):
    """ Return form """
    model = Post
    # the page creation will be operated
    template_name = "post_create.html"
    # tell user the field they need provide (e.g. titile, image)
    fields = "__all__"

class PostUpdateView(UpdateView):
    model = Post
    template_name = "post_update.html"
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    # Delete model as well as every field of the model
    template_name = "post_delete.html"
    # success_url = reverse("posts")
    # reverse_lay allows simultaneously do (1)delete (2)render html
    # allows delete at backend and render html to show
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    # when create user, tell the view which model/form to use
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")
