from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset() \
        .filter(status=Post.Status.PUBLISHED)
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               related_name='blog_posts') # This will allow us to access related objects easily from a user object by using the user.blog_posts notation.
    publish = models.DateTimeField(timezone.now)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add update the field when creating the object
    updated = models.DateTimeField(auto_now=True) # auto_now update the field when saving the model
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.DRAFT)
    
    """
    Post.Status.choices to obtain the available choices, Post.Status.labels to obtain
    the human-readable names, and Post.Status.values to obtain the actual values of the choices.
    """

    objects = models.Manager() # default manager
    published = PublishedManager() # Custom Manager


    class Meta:
        ordering = ['-publish'] # ordering from newest to the oldest
        indexes = [models.Index(fields=['-publish'])] # Help improve the querying when using this field
        
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
        
