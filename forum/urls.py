from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#TODO: если пользователь не авторизован, то при любой попытке зайти на любую другую страницу сайта должно перекидывать на login форму
urlpatterns = [
    path('', views.main, name='main'),
    path('topic_detail/<int:pk>', views.topic_detail, name='topic_detail'),

    #Регистрация
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration'),
    # path('update_profile', views.update_profile, name='update_profile'),
]