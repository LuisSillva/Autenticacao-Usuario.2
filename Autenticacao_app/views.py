from django.shortcuts import render, redirect
from django.http import HttpResponse
# from autenticacao_app.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config


def user_cadastro(request):

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email já cadastrado!')
            return redirect('cadastro')

        if User.objects.filter(username=username):
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')

        if len(username)>10:
            messages.error(request, 'O seu nome de usuário deve ter no máximo 10 caracteres.')
            return redirect('cadastro')
        
        if username.isnumeric():
            messages.error(request, 'O nome de usuário não pode conter apenas números.')
            return redirect('cadastro')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Cadastro concluído com sucesso.')
        return redirect('login')
        
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciais incorretas')
            return redirect('/auth/login')

def user_signout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully.')
    return redirect('login')

@login_required(login_url='/auth/login')
def home(request):
    return render(request, 'home.html')

@login_required
def password_change(request):
    user = request.user
    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {form: form})

@login_required
def envia_email(request):
    user = request.user
    user_email = user.email
    send_mail('Assunto', 
            'Mensagem', 
            config('EMAIL_HOST_USER'),
            [user_email],
            
        )
    return HttpResponse(f'Seu email é: {user_email}')