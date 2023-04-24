from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import Http404
from django.shortcuts import render, redirect, reverse

from apps.authentication.forms import RegisterUserForm, LoginUserForm, PasswordResetForm
from apps.authentication.utils.send_gmail import send_gmail
from apps.authentication.utils.tokens import base36_to_int, generate_one_time_link, validate_one_time_link


def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        user = User.objects.get(email=email)
        user_id, token, token_created = generate_one_time_link(user).split('-')
        link = f"http://127.0.0.1:8000/auth/reset-password/{user_id}/{token_created}-{token}"
        send_gmail('Account Recovery', user.username, email, link)
    return render(request, 'authentication/forgot-password.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('products:homepage'))
    context = {'form': LoginUserForm()}
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Successfully logged in!')
                    return redirect(reverse('products:homepage'))
                else:
                    messages.error(request, 'email or password Incorrect!')
            except:
                messages.error(request, 'Email or password Incorrect!')
        else:
            messages.error(request, 'Email is invalid!')
    return render(request, 'authentication/login.html', context)


# @login_required(login_url='authentication:login')
def logout_page(request):
    logout(request)
    return render(request, 'authentication/logout.html')


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('products:homepage'))
    context = {'form': RegisterUserForm()}
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('products:homepage'))
        else:
            messages.error(request, 'Invalid data!')
        context['form'] = form
    return render(request, 'authentication/register.html', context)


def reset(request, user_id, token):
    context = {
        'user_id': user_id,
        'token': token
    }
    user_id = base36_to_int(str(user_id))
    User = get_user_model()
    user = User.objects.get(id=user_id)
    created_at, token = token.split('-')[0], token.split('-')[1]
    if request.method == 'POST' and user.used_token is None:
        user.used_token = True
        user.save()
        if not validate_one_time_link(user, token, created_at):
            raise Http404
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.data.get('password1'))
            user.save()
            return redirect(reverse('authentication:login'))
    if not validate_one_time_link(user, token, created_at):
        raise Http404
    user.used_token = None
    user.save()
    return render(request, 'authentication/reset-password.html', context)
