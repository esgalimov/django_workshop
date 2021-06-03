from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm
from django.urls import reverse_lazy
# Create your views here.


class HomeNews(ListView):
    # модель, с которой работает обработчик
    model = News
    # имя шаблона
    template_name = 'learn_app/home_news_list.html'
    # имя списка данных из бд
    context_object_name = 'news'

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
        return News.objects.filter(is_published=True)


class NewsByCategories(ListView):
    model = News
    template_name = 'learn_app/home_news_list.html'
    context_object_name = 'news'
    # отменить показ, если список пуст или категория не существует
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    # параметры запроса находтся в self.kwargs
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id' - можно так использовать параметр в url запросе
    # или поменять на pk в urls.py и в модели (pk используется по умолчанию)
    # template_name = 'learn_app/news_detail.py'
    context_object_name = 'news_item'


class CreateNews(CreateView):
    # форма
    form_class = NewsForm
    template_name = 'learn_app/add_news.html'
    # после поста происходит редирект (по умолчанию) на страницу созданной новости
    # (в этом помогает функция get_absolute_url в модели)
    success_url = reverse_lazy('home')
    # редирект переопределен на гланую страницу


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
