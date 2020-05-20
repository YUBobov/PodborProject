#Библиотека для работы с получением ссылок в адресной строке
from django.urls import path
#Из локального приложение импортируем файл views
from . import views
urlpatterns = [
    #Откртие метода из файла views на главной странице
    #По атрибуту name можно обращаться к данной функции в HTML коде с помощью логики Django
    path('', views.index, name='index'),
    #Просивыается URL-адрес выполнеия шаблона, который передаётся в функции views.kabels
    path('kabels', views.kabels, name='kabels'),
]