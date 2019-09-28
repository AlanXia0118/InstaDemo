from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# from Insta.models import UserConnection
from Insta.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InstaUser, Post, Like, Comment
from django import forms


"""
Create your views here.
"""

class IndexView(ListView):
    """ For people doesn't login """
    # 需要@Override的属性
    model = Post
    template_name = "index.html"

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"
    login_url = "login"

class PostDetailView(DetailView):
# class PostDetailView(LoginRequiredMixin, DetailView):
    """ Return object """
    model = Post
    template_name = "post_detail.html"
    # login_url = "login"

class PostCreateView(LoginRequiredMixin, CreateView):
    """ Return form """
    model = Post
    # the page creation will be operated
    template_name = "make_post.html"
    # tell user the field they need provide (e.g. titile, image)
    fields = "__all__"
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    # Delete model as well as every field of the model
    template_name = "post_delete.html"
    # success_url = reverse("posts")
    # reverse_lay allows simultaneously do (1)delete (2)render html
    # allows delete at backend and render html to show
    success_url = reverse_lazy("home")

class SignUp(CreateView):
    # when create user, tell the view which model/form to use
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")


class UserProfile(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = "user_profile.html"
    login_url= "login"



""" To fix make_post bug."""
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image')


from django.http import HttpResponseRedirect
def create_post(request):
    form = CreatePostForm(request.POST, request.FILES)
    if form.is_valid():
        author = request.user
        title = form.cleaned_data.get('title')
        image = form.cleaned_data.get('image')
        # print(type(image))
        if image is not None:
            post = Post.objects.create(author=author, title=title, image=image)
            return HttpResponseRedirect("/")
    return render(request, '../templates/make_post.html', {'form': form})