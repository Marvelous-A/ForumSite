from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import *
from .models import *

# Create your views here.
@login_required(login_url='login')
def main(request):
    topics = Topic.objects.all()
    views = Views.objects.all()
    arr = []
    for topic in topics:
        arr.append(topic)
    for view in views:
        arr.append(view.question)
    # Создание словаря для подсчета повторений элементов
    counts = {}
    for item in arr:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    # Преобразование словаря в список кортежей
    topics_result = [[key, value] for key, value in counts.items()]
    topics_result = sorted(topics_result, key=lambda x: x[1], reverse=True)
    topics_result = [i[0] for i in topics_result]
    # return render(request, 'card/main.html', {'topics': topics_result, 'views': views})
    chapters = Chapter.objects.all()
    return render(request, 'card/main.html', {'chapters': chapters})

@login_required(login_url='login')
def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    topics = Topic.objects.filter(chapter=chapter)
    return render(request, 'card/chapter_detail.html', {'chapter': chapter, 'topics': topics})

@login_required(login_url='login')
def topic_detail(request, pk):
    users = Profile.objects.all()
    users_admin = []
    for user in users:
        if user.admin == True:
            users_admin.append(f"{user.user}")
    topic = get_object_or_404(Topic, pk=pk)
    questions = Chat.objects.filter(topic=topic)

    search_query = request.GET.get('search_query', request.session.get('search_query', ''))

    if search_query:
        questions = questions.filter(text_question__icontains=search_query)

    chapter = topic.chapter.all()[0]
    questions_names = []
    for question in questions:
        questions_names.append(question.text_question)
    return render(request, 'card/topic_detail.html', {'search_query': search_query, 'chapter': chapter, 'questions_names': questions_names, 'questions': questions, 'topic': topic, 'users_admin': users_admin})
    # return render(request, 'card/topic_detail.html', {'topic':topic, 'form': message_form, 'messages': messages})

@never_cache
@login_required(login_url='login')
def question_detail(request, pk):
    user = request.user
    # topic = get_object_or_404(Topic, pk=pk)
    question = get_object_or_404(Chat, pk=pk)
    messages = Message.objects.filter(question=question)
    # views = Views(user=request.user, question=get_object_or_404(Question, pk=pk))
    # views.save()
    if request.method == 'POST':
        message_form = MessageForm(data=request.POST, files=request.FILES)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.author = request.user  # Автоматически устанавливаем автора
            message.question = question         # и тему
            message.save()
            redirect('question_detail', pk=pk)
        else:
            print(message_form.errors)
    else: 
        message_form = MessageForm()
    # return render(request, 'card/question_detail.html', {})
    topic = question.topic.all()[0]
    chapter = topic.chapter.all()[0]
    print(chapter)
    return render(request, 'card/question_detail.html', {'chapter': chapter, 'topic': topic, 'question':question, 'form': message_form, 'messages': messages})

# def delete_message(request, pk_mess, pk_ques):
    # message = get_object_or_404(Message, pk=pk_mess)
    # question = get_object_or_404(Question, pk=pk_ques)
    # message.delete()
    # return redirect("{% url 'question_detail' pk=question.pk %}")
    # return render(request, "{% url 'card/question_detail.html' pk=question.pk %}", {})

#Регистрация
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Перенаправление на главную страницу
        else:
            # Возвращение сообщения об ошибке
            return render(request, 'auth/login.html', {'error': 'Неверное имя пользователя или пароль'})
    else:
        return render(request, 'auth/login.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html', {})

def profile(request):
    return render(request, 'auth/profile.html', {})

def registration(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Сохранение данных пользователя
            profile = user.profile
            for field in profile_form.cleaned_data:
                setattr(profile, field, profile_form.cleaned_data[field])
            profile.save()  # то же самое что instance.profile.save() в сигналах

            login(request, user)
            return redirect('main')
        else:
            print(user_form.error_messages)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    context = {
        user_form: user_form,
        profile_form: profile_form
    }
    return render(request, 'auth/registration.html', {})

# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if profile_form.is_valid() and user_form.is_valid():  # Нужно вводить все параметры включая пороль
#             user_form.save()
#             profile_form.save()
#             # messages.success(request, _('Your profile was successfully updated!'))
#             print('Your profile was successfully updated!')
#             return redirect('main_list')
#         else:
#             # messages.error(request, _('Please correct the error below.'))
#             print('Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'auth/update_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })