from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post
from categories.models import Category
from tags.models import Tag


class PostsListView(ListView):
    """ Displays posts list by specified params """
    model = Post
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects \
        .only('title', 'context', 'posted_date', 'author', 'category', 'tags') \
        .order_by('-posted_date')


class PostDetailView(DetailView):
    """ Displays single post content """
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects\
        .only('title', 'context', 'posted_date', 'author', 'category', 'tags') \
        .order_by('-posted_date')


class PostByCategoryView(ListView):
    """ Displays posts by a single category"""
    model = Post
    template_name = 'posts_by_category.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        """ Extracting category title from url and searching posts by this category"""
        category = get_object_or_404(Category, title=self.kwargs.get('category'))
        return Post.objects.filter(category=category).order_by('-posted_date')


class PostByUserView(ListView):
    """ Displays posts by a particular user """
    model = Post
    template_name = 'posts_by_user.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        """ Extracting category title from url and searching posts by this category"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-posted_date')


class PostByTagView(ListView):
    """ Displays posts by chosen tag"""
    model = Post
    template_name = 'posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        """ Getting posts by specified tag"""
        tag = get_object_or_404(Tag, title='#' + self.kwargs.get('tag'))
        return Post.objects.filter(tags__in=[tag]).order_by('-posted_date')


class PostCreateView(LoginRequiredMixin, CreateView):
    """ Allows authorized users to create a new post """
    model = Post
    fields = ['title', 'context']
    template_name = 'post_cud/post_form.html'

    def form_valid(self, form):
        """ Checks form validation for creating posts and  assigns post author to current user"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Allows current user to update their post """
    model = Post
    fields = ['title', 'context']
    template_name = 'post_cud/post_form.html'

    def form_valid(self, form):
        """ Checks form validation for updating posts and  assigns post author to current user """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """ Checks, whether current user has permissions to update a post """
        current_post = self.get_object()
        if self.request.user == current_post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Allows current user delete their post """
    model = Post
    success_url = '/'
    template_name = 'post_cud/post_delete_form.html'

    # route to redirect user after successful deleting

    def test_func(self):
        """ Checks, whether current user has permissions to delete a post """
        current_post = self.get_object()
        if self.request.user == current_post.author:
            return True
        return False
