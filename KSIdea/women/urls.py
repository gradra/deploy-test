from django.urls import path, re_path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),   # index, name='home'),
    #    path('', cache_page(60 * 2)(WomenHome.as_view()), name='home'), кэширование на ур-не классов и ф-ций представлений
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),  # addpage, name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),  # show_post, name='post'),  # 'post/<int:post_id>/',
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),  # <int:cat_id>', show_category, name='category'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('cats/<int:catid>/', categories),  # str:bez /,
    # slug:latiniza i - _, uuid: malie latiniza i -,
    # path: ne pustaia stroka i /
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
