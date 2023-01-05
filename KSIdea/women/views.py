from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, FormView  # в ListView встроена пагинация Paginating
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login


# menu = [{'title': "О сайте", 'url_name': "about"},
#         {'title': "Добавить статью", 'url_name': "add_page"},
#         {'title': "Обратная связь", 'url_name': "contact"},
#         {'title': "Войти", 'url_name': "login"}]


class WomenHome(DataMixin, ListView):
    #    paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Glavnayia str'}  # tolko d/statichnih dannih, ne d/spiskov

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная стр')
        context = dict(list(context.items()) + list(c_def.items()))  # return context|c_def
        # context['menu'] = menu
        # context['title'] = 'Главная стр'
        # context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')  # добавили жадную
#                    загрузку связанных данных по внеш. ключу ForeignKey,чтоб уменьшить число SQLзапросов


# def index(request):
#     posts = Women.objects.all()
# #    cats = Category.objects.all()

#     context_dict = {
#         'posts': posts,
#         #        'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context_dict)


# @login_required  # декоратор доступа для фун-ий представлений, класс LoginRequiredMixin - для кл. представлений
def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)  # импортируем из django.core.paginator
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # по умолчанию def get_absolute_url(self):return reverse('post', kwargs={'post_slug': self.slug})
#                                    перекидывает на страницу созданной статьи, но можно указать самим куда переходить
#    login_url = '/admin/'
    raise_exception = True  # доступ запрещен 403

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        # context['menu'] = menu
        # context['title'] = 'Добавление статьи'
        return context | c_def

# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)  # форма с заполненными данными
#         if form.is_valid():
#             # print(form.cleaned_data)  # если корректный ввод, отобразим очищенные данные

#             # try:
#             # Women.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('home')
#             # except:
#             #form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()  # пустая форма
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def contact(request):
#     return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # pk_url_kwarg = 'pk' post_pk
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        # context['menu'] = menu
        # context['title'] = context['post']
        return context | c_def

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)  # ф-ция django

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    #    paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')  # добавили жадную
#                    загрузку связанных данных по внеш. ключу ForeignKey,чтоб уменьшить число SQLзапросов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        # context['menu'] = menu
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        return context | c_def


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)
# #    cats = Category.objects.all()

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         #        'cats': cats,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'women/index.html', context=context)
#     # return HttpResponse(f"Отображение категории с номером id={cat_id}.")


def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Statii po kategoriam</h1><p>{catid}</p>")


def archive(request, year):
    if int(year) > 2020:
        # raise Http404()
        return redirect('home', permanent=True)  # 301 postoiannij, 302 vremennij
    return HttpResponse(f"<h1>Arhiv po godam</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Straniza NE naidena</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # UserCreationForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form):  # этот метод вызыв. при успешн.проверке формы
        user = form.save()  # сами сщхраняем форму в БД
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  # AuthenticationForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def

    # def get_success_url(self): # можно задать переход по умолчанию в settings.py
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
