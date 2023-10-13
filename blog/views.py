from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost


class BlogPostListView(ListView):
    """
    Отображение списка опубликованных блогов, отсортированных по дате создания.
    """
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogs'

    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.filter(is_published=True).order_by('-created_at')

        return query


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    """
    Отображение детальной информации о блоге и учет количества просмотров.
    """
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        self.object.views_count += 1
        self.object.save()

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Создание нового блога с указанием основных полей.
    """
    model = BlogPost
    permission_required = 'blog.add_blog'
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('blog:blogpost_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.object.image:
            self.object.image = 'media/note_image.jpg'
            self.object.save()
        return response


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Обновление существующего блога.
    """
    model = BlogPost
    permission_required = 'blog.change_blog'
    fields = ('title', 'content', 'is_published', 'views_count', 'image')
    success_url = reverse_lazy('blog:blogs')

    def get_success_url(self):
        return reverse('blog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление блога.
    """
    model = BlogPost
    success_url = reverse_lazy('blog:blogpost_list')

    def test_func(self):
        return self.request.user.is_superuser
