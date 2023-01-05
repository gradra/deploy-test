from django.db import models
from django.urls import reverse


class Women(models.Model):
    # pole id uje v Models
    title = models.CharField(max_length=255, verbose_name="Заголовок")

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)  # , null=True) при добавлении слагов удаляем все миграции т.к. требуется заполнение уникального поля

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:  # вложенный класс
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'  # mnojestven chislo
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")  # , related_name='get_posts' для получения связанных постов из модели women (по умол-ю ?.women_set.all())
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})  # {'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'  # mnojestven chislo
        ordering = ['id']
