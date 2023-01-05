from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # 'photo', 'is_published')  # список полей,которые хотим видеть
    list_display_links = ('id', 'title')  # поля,на которые можем кликнуть и перейти
    search_fields = ('title', 'content')  # по каким полям можем производить поиск
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

    prepopulated_fields = {'slug': ('title',)}

    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')  # поля и их порядок для редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # поля НЕредактируемые

    def get_html_photo(self, object):  # для отображения миниатюр в админке
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")  # марк-сэйф указывает НЕ экранировать тэги

    get_html_photo.short_description = "Миниатюра "


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта об известных женщинах'
