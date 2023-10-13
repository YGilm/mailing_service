from django.contrib import admin
from blog.models import *


@admin.register(BlogPost)
class BlogPost(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'views_count']
    list_filter = ['created_at']
    search_fields = ['title', 'content']
