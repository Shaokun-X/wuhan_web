from django.urls import path
from .views import user_login, index


app_name = 'news'
urlpatterns = [
    path('', user_login, name='login'),
    path('login/', user_login, name='login'),
    path('index/', index, name='index'),
]