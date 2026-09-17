from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = News.Status.Published)
class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = News.Status.Draft)

class Category(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class News(models.Model):

    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to="media/news/images")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices= Status.choices, default= Status.Draft)
    created_time = models.DateTimeField(auto_now_add=True)
    published_time = models.DateTimeField(default= timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()

    class Meta:
        ordering = ["-published_time"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('single_page', args=[self.slug])

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email