from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # сразу авторизум пользователя
            user = form.save()
            login(request, user)
            # сообщение, доступно через контекст шаблона
            messages.success(request, 'Вы зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()

    return render(request, 'learn_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'learn_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # функция для отправки
            mail = send_mail(form.cleaned_data['subject'],
                      form.cleaned_data['content'],
                      'EMAIL_FROM',
                      ['EMAIL_TO'],
                      fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = ContactForm()
    return render(request, 'learn_app/test.html', {'form': form})


class HomeNews(ListView):
    # модель, с которой работает обработчик
    model = News
    # имя шаблона
    template_name = 'learn_app/home_news_list.html'
    # имя списка данных из бд
    context_object_name = 'news'
    paginate_by = 2

    # для подгрузки всех данных из связанных полей сразу
    # queryset = News.objects.select_related('category')
    # статичные данные, передающиеся в шаблон (способ не очень)
    # extra_context = {'title': 'Главная'}

    # передача данных в шаблон (этот метод отвечает за все, что передается в шаблон)
    def get_context_data(self, *, object_list=None, **kwargs):
        # сохраняем то, что было в родительском классе
        context = super().get_context_data(**kwargs)
        # добавляем свое
        context['title'] = 'Главная страница'
        return context

    # Select полей модели из бд (по умолчанию - все)
    def get_queryset(self):
        # select_related нужно чтобы подгружать данные из связанных полей сразу
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategories(ListView):
    model = News
    template_name = 'learn_app/home_news_list.html'
    context_object_name = 'news'
    # отменить показ, если список пуст или категория не существует
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    # параметры запроса находтся в self.kwargs
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id' - можно так использовать параметр в url запросе
    # или поменять на pk в urls.py и в модели (pk используется по умолчанию)
    # template_name = 'learn_app/news_detail.py'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    # форма
    form_class = NewsForm
    template_name = 'learn_app/add_news.html'
    # после поста происходит редирект (по умолчанию) на страницу созданной новости
    # (в этом помогает функция get_absolute_url в модели)
    success_url = reverse_lazy('home')
    # редирект переопределен на гланую страницу

    login_url = '/admin/'
    # редирект, в случае, если в доступе отказано

    # raise_exception = True
    # если не авторизован, ошибка 403



# def index(request):
#     news = News.objects.all()
#     context = {'news': news,
#                'title': 'Список новостей'
#                }
#     return render(request, 'learn_app/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.all()
#     context = {'news': news,
#                'category': category
#                }
#     return render(request, 'learn_app/category.html', context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'learn_app/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#
#     else:
#         form = NewsForm()
#     return render(request, 'learn_app/add_news.html', {'form': form})
