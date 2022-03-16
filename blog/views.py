from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
# from .forms import ContactForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.views import generic

from blog.forms import CommentForm, ContactForm
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import UserProfile


# Create your views here.

class ContactView(generic.FormView):
    template_name = "blog/contact.html"
    form_class = ContactForm
    success_url = "/contact"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thanks for contacting us!')
        return super().form_valid(form)



# search view
# def post_search(request):
#     form = SearchForm
#     results = []

#     if 'q' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             q = form.cleaned_data['q']

#             results = Post.objects.filter(title__contains=q)

#     return render(request, 'blog/search.html', {'form': form, 'results': results})


class PostList(ListView):
    model = Post, UserProfile
    # paginate_by = 2
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/blog-list.html"

def blog(request, tag_slug=None):
    posts = Post.published.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 9)  # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog-list.html', 
                    {'posts': posts, 
                    'pages': page, 
                    'tag': tag
                    })


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/blog-single.html"

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    current_site = get_current_site(request)

    form = CommentForm(request.POST)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()

    comments = Comment.objects.filter(post=post).order_by('-created_on')
    comments_count = comments.count()

    return render(request, 'blog/blog-single.html',
                    {'domain': current_site,
                    'post': post,
                    'similar_posts': similar_posts,
                    'form': form,
                    'comments': comments,
                    'comments_count': comments_count,
                    })