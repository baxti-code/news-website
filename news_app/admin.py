from django.contrib import admin
from .models import News, Category, Contact, Comments
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
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'active', 'created_time']
    list_filter = ['created_time', 'active']
    search_fields = ['user', 'body']
    
    actions = ['disable_comments', 'activate_comments']
    
    def disable_comments(self, request, queryset):
         queryset.update(active=False)
        
    def activate_comments(self, request, queryset):
        queryset.update(active=True)