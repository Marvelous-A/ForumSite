from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView
from .forms import *
from .models import *

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
# from urllib import self.request

class Main(LoginRequiredMixin, ListView):
    model = Chapter #????????????????
    template_name = 'card/main.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        chapters = Chapter.objects.all()
        context_data['chapters'] = chapters
        return context_data

class ChapterDetail(LoginRequiredMixin, ListView):
    model = Chapter
    template_name = 'card/chapter_detail.html'
    # context_object_name = 'chapter'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, pk=self.kwargs['pk'])
        topics = Topic.objects.filter(chapter=chapter)
        context_data['chapter'] = chapter
        context_data['topics'] = topics
        return context_data
    
    def get_queryset(self):
        chapter = Chapter.objects.filter(pk=self.kwargs['pk'])
        return chapter
    
class TopicDetail(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'card/topic_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        users = Profile.objects.all()
        users_admin = []
        for user in users:
            if user.admin == True:
                users_admin.append(f"{user.user}")
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        questions = Chat.objects.filter(topic=topic)
        
        search_query = self.request.GET.get('search_query', self.request.session.get('search_query', ''))

        if search_query:
            questions = questions.filter(text_question__icontains=search_query)

        chapter = topic.chapter.all()[0]
        questions_names = []
        for question in questions:
            questions_names.append(question.text_question)
        context_data['topic'] = topic
        context_data['questions'] = questions
        context_data['users_admin'] = users_admin
        context_data['chapter'] = chapter
        context_data['questions_names'] = questions_names
        context_data['search_query'] = search_query
        return context_data
    
class QuestionDetail(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'card/question_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        question = get_object_or_404(Chat, pk=self.kwargs['pk'])
        messages = Message.objects.filter(question=question)

        if self.request.method == 'POST':
            message_form = MessageForm(data=self.request.POST, files=self.request.FILES)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.author = self.request.user  # Автоматически устанавливаем автора
                message.question = question         # и тему
                message.save()
                redirect('question_detail', pk=self.kwargs['pk'])
            else:
                print(message_form.errors)
        else: 
            message_form = MessageForm()
        
        topic = question.topic.all()[0]
        chapter = topic.chapter.all()[0]
        print(chapter)
        context_data['chapter'] = chapter
        context_data['topic'] = topic
        context_data['question'] = question
        context_data['form'] = message_form
        context_data['messages'] = messages
        return context_data
    
#РЕНИСТРАЦИЯ

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('forum:main')  # Перенаправление на главную страницу
        else:
            # Возвращение сообщения об ошибке
            return render(request, 'auth/login.html', {'error': 'Неверное имя пользователя или пароль'})
    else:
        return render(request, 'auth/login.html')
    
# @login_required(login_url='login')
def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html', {})

# class Login(ListView):
#     model = Profile
#     template_name = 'auth/login.html'

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['error'] = 'Неверное имя пользователя или пароль'
#         if self.request.method == 'POST':
#             username = self.request.POST['username']
#             password = self.request.POST['password']
#             user = authenticate(self.request, username=username, password=password)
#             if user is not None:
#                 login(self.request, user)
#                 return redirect('main')  # Перенаправление на главную страницу
#             else:
#                 # Возвращение сообщения об ошибке
#                 return context_data
#         else:
#             print("qqqqqqqqqqqqqqqqqqqqqq")
#             return redirect('main')
        
# class Logout(ListView):
#     model = Profile
#     template_name = 'auth/logout.html'

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         logout(self.request)
#         return context_data