from django.contrib import admin
from .models import News, Category, Contact
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_time', 'status']
    list_filter = ['published_time', 'status', 'created_time', 'category']
    prepopulated_fields = {'slug' : ('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'published_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')