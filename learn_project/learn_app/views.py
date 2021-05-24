from django.shortcuts import render
from django.http import HttpResponse

from .models import News, Category

# Create your views here.


def index(request):
    news = News.objects.all()
    categories = Category.objects.all()
    context = {'news': news,
               'title': 'Список новостей',
               'categories': categories
               }
    return render(request, 'learn_app/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.all()
    context = {'news': news,
               'categories': categories,
               'category': category
               }
    return render(request, 'learn_app/category.html', context)

