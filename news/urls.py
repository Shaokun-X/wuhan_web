from django.urls import path
from .views import user_login, index, detail, delete


app_name = 'news'
urlpatterns = [
    path('', index, name='default'),
    path('login/', user_login, name='login'),
    path('index/', index, name='index'),
    path('report/<int:pk>', detail, name='detail'),
    path('report/<int:pk>/delete', delete, name='delete'),
]
