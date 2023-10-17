from django import template
from django.conf import settings

register = template.Library()


@register.filter
def mediapath(path):
    """
    Фильтр для Django-шаблона. Принимает относительный путь к медиафайлу
    и возвращает абсолютный URL, добавляя к нему MEDIA_URL из настроек.
    Если путь пуст, возвращает URL для изображения-заглушки.
    """
    if path:
        return f"{settings.MEDIA_URL}{path}"
    else:
        return f"{settings.MEDIA_URL}not_image.jpg"


@register.simple_tag
def mediapath_tag(path):
    """
    Простой тег для Django-шаблона. Функциональность аналогична фильтру mediapath,
    но может быть использован как тег в шаблоне.
    Принимает относительный путь к медиафайлу и возвращает абсолютный URL.
    """
    if path:
        return f"{settings.MEDIA_URL}{path}"
    else:
        return f"{settings.MEDIA_URL}not_image.jpg"
