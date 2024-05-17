from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

#TODO: если пользователь не авторизован, то при любой попытке зайти на любую другую страницу сайта должно перекидывать на login форму
urlpatterns = [
    path('', views.main, name='main'),
    path('chapter_detail/<int:pk>', views.chapter_detail, name='chapter_detail'),
    path('topic_detail/<int:pk>', views.topic_detail, name='topic_detail'),
    path('question_detail/<int:pk>', views.question_detail, name='question_detail'),
    # path('delete_message/<int:pk_mess>/<int:pk_ques>', views.delete_message, name='delete_message'),

    #Регистрация
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration'),
    # path('update_profile', views.update_profile, name='update_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)