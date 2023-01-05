from .models import *
from django.db.models.aggregates import Count
# from django.core.cache import cache  # для испол-я APIнизкого ур-ня для кэширования

menu = [{'title': "О сайте", 'url_name': "about"},
        {'title': "Добавить статью", 'url_name': "add_page"},
        {'title': "Обратная связь", 'url_name': "contact"},
        ]
#        {'title': "Войти", 'url_name': "login"}]


class DataMixin:
    paginate_by = 30

    def get_user_context(self, **kwargs):
        context = kwargs

#        cats = cache.get('cats')
#        if not cats:
        cats = Category.objects.annotate(Count('women'))
# #       cats = Category.objects.all()
#            cache.set('cats', cats, 60 * 3)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
#        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
