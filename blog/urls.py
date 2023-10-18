from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache

from blog.apps import BlogConfig
from blog.views import *
from django.conf.urls.static import static

app_name = BlogConfig.name

urlpatterns = [

    path('blog/', cache_page(60)(BlogPostListView.as_view()), name='blogpost_list'),
    path('blog/<int:pk>/', cache_page(60)(BlogPostDetailView.as_view()), name='blogpost_detail'),
    path('blog/create/', never_cache(BlogPostCreateView.as_view()), name='blogpost_form'),
    path('blog/edit/<int:pk>/', never_cache(BlogPostUpdateView.as_view()), name='blogpost_update'),
    path('blog/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)