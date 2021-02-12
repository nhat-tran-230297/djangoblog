from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView)
    
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import User
from .models import Post


# Create your views here.

class PostListView(ListView):
    model = Post

    # as default <app>/<model>_<viewtype>.html ~ blog/post_list.html, we can override to change our route
    template_name='blog/home.html'

    # as default: object
    context_object_name = 'posts'

    # date_posted newest to oldest
    ordering = ['-date_posted']

    # pagination
    paginate_by = 5


class UserPostListView(ListView):
    model = Post  

    # as default <app>/<model>_<viewtype>.html ~ blog/post_list.html, we can override to change our route
    template_name='blog/user_posts.html'   
    context_object_name = 'posts'  
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # override the form_valid() method
    # parent form_valid() -> redirect to the supplied URL
    # this form_valid() -> redirect to the supplied URL + assign the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']


    # override the form_valid() method
    # parent form_valid() -> redirect to the supplied URL
    # this form_valid() -> redirect to the supplied URL + assign the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    """ deny user access if return False """
    def test_func(self):
        # get current post
        post = self.get_object()

        # check if the current post's author == the user
        if self.request.user == post.author:
            return True

        # deny the user's access
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    

    def test_func(self):
        # get current post
        post = self.get_object()

        # check if the current post's author == the user
        if self.request.user == post.author:
            return True

        # deny the user's access
        return False


def about(request):
    return render(request, 'blog/about.html')