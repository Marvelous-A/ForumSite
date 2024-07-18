from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from forum import views

from forum.apps import ForumConfig
from forum.views import *

app_name = ForumConfig.name

#TODO: если пользователь не авторизован, то при любой попытке зайти на любую другую страницу сайта должно перекидывать на login форму
urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('chapter_detail/<int:pk>', ChapterDetail.as_view(), name='chapter_detail'),
    path('topic_detail/<int:pk>', TopicDetail.as_view(), name='topic_detail'),
    path('question_detail/<int:pk>', QuestionDetail.as_view(), name='question_detail'),
    # path('delete_message/<int:pk_mess>/<int:pk_ques>', views.delete_message, name='delete_message'),

    # #Регистрация
    # path('', include('django.contrib.auth.urls')),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    # path('profile', views.profile, name='profile'),
    # path('registration', views.registration, name='registration'),
    # path('update_profile', views.update_profile, name='update_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)