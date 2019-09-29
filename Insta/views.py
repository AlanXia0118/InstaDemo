from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from annoying.decorators import ajax_request

# from Insta.models import UserConnection
from Insta.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InstaUser, Post, Like, Comment, UserConnection
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
    success_url = reverse_lazy("home")


class UserProfile(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = "user_profile.html"
    login_url= "login"


class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]


class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'



""" To fix make_post bug."""
from django.http import HttpResponseRedirect
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image')



def create_post(request):
    form = CreatePostForm(request.POST, request.FILES)
    if request.method == "GET":
        print("-------------make post")
        return render(request, "../templates/make_post.html", {'form': form})
    elif request.method == "POST":
        print("-------------upload post")
        if form.is_valid():
            author = request.user
            title = form.cleaned_data.get('title')
            image = form.cleaned_data.get('image')
            # print(type(image))
            post = Post.objects.create(author=author, title=title, image=image)
    return HttpResponseRedirect("/")



# annotation means the function specially responses to ajax operations
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        # save like object to database
        like.save()
        result = 1
    except Exception as e:
        # if the user has liked the post, means cancel -> delete it
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
