from django.db import models
from autoslug import AutoSlugField

NULLABLE = {'null': True, 'blank': True}


class BlogPost(models.Model):
    """
    Модель для хранения блогов.
    Содержит заголовок, содержание, изображение и информацию о публикации.
    """
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name='slug')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликован')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('created_at',)
