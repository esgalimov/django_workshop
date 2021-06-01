from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import News, Category
from .forms import NewsForm
# Create your views here.


def index(request):
    news = News.objects.all()
    context = {'news': news,
               'title': 'Список новостей'
               }
    return render(request, 'learn_app/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.all()
    context = {'news': news,
               'category': category
               }
    return render(request, 'learn_app/category.html', context)


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'learn_app/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = News.objects.create(**form.cleaned_data)
            return redirect(news)

    else:
        form = NewsForm()
    return render(request, 'learn_app/add_news.html', {'form': form})