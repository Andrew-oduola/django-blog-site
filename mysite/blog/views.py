from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog\post\list.html', {'posts': posts})

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
    return render(request, 'blog\post\detail.html', {'post': post})
