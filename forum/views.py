from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import ProfileForm, UserForm
from .models import *

# Create your views here.
def main(request):
    topics = Topic.objects.all()
    views = Views.objects.all()
    arr = []
    for topic in topics:
        arr.append(topic)
    for view in views:
        arr.append(view.topic)
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
    return render(request, 'card/main.html', {'topics': topics_result, 'views': views})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    views = Views(user=request.user, topic=get_object_or_404(Topic, pk=pk))
    views.save()
    return render(request, 'card/topic_detail.html', {'topic':topic})

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
        return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'card/main.html', {})

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
            print(user_form.error_messages, "qqqqqqq")
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