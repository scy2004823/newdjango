from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class PostListView(ListView):
    model = Post
    template_name = 'blog/scoreboard.html'
    context_object_name = 'posts'
    ordering = ['-score']
    paginate_by = 15

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user-posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        posts = Post.objects.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['score']
    # template_name = 'blog/home.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'post_pic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

def add_score(request):
    if request.method == 'POST':
        score = request.POST['score']

        Post.objects.create(
            score = score
        )

        # return HttpResponse('')

class PostAddAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]
    # permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # url_ = post.get_absolute_url()
        # if request.method == 'POST':
            # score = request.POST['score']

        Post.objects.create(
            score = request.POST['score'],
            author_id = self.request.user.id,
            # score = score
        )
        return HttpResponse('')

class HomeView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/home.html'
    fields = ['score']
    # template_name = 'blog/home.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
