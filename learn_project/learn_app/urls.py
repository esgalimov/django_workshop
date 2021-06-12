from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path('', index, name='home'),
    # as_view - для класса
    # cache_page(время) - кеширование на уровне представлений
    path('', cache_page(60)(HomeNews.as_view()), name='home'),
    # path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>', get_category, name='category'),
    path('category/<int:category_id>', NewsByCategories.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add_news/', add_news, name='add_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    path('contact/', contact, name='contact'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout')
]