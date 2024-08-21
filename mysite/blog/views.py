from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.http import require_POST
from django.db.models import Count

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag

# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                  'blog\post\list.html', 
                  {'posts': posts,
                   'tags': tag})

def post_detail(request, year, month, day, post):
    """try:
        post = Post.publish.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.") 
        
    instead of doing this we can go this way"""

    

    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)    
    
    comments =  post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 
                  'blog\post\detail.html', 
                  {'post': post,
                   'comments': comments,
                   'form': form})

# using class based view
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # retrive post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # form was submitted
        form =  EmailPostForm(request.POST) #
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
            f"{cd['name']} \'s comments: {cd['comment']}"
            # send_mail(subject, message, 'ayobamioduola13@gmail.com',
            #           [cd['to']])
            email = EmailMessage(subject, message, 'ayobamioduola13@gmail.com', [cd['to']])
            email.send()
            sent = True
            
    else:
        form = EmailPostForm()


    return render (request, 'blog/post/share.html', {'form': form,
                                                     'post': post})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html', 
                  {'post': post,
                   'form': form,
                   'comment': comment})
