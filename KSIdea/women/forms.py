from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):  # .Form):
    # title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255)
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    # is_published = forms.BooleanField(label="Опубликовать", initial=True, required=False)  # необязательное поле
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women
        # fields = '__all__'  # нужно показывать все поля, кроме тех, что заполняются автомати-ки
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 18}),
        }

    def clean_title(self):  # своя валидация данных, конкретно title. Всегда начинается с clean_
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина статьи превышает 200 символов')
        return title


class RegisterUserForm(UserCreationForm):
    #username = forms.CharField(label='Догин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))  # поэтому переопределяем их
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'})  # для полей паролей стили не работают...(
        # }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='картинка')
