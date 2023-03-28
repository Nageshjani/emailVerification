from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from .models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import login



def signupView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            send_verification_email(request, user)
            return render(request,'myapp/email_sent.html')

    else:
        return render(request,'myapp/signup.html')



def send_verification_email(request, user):
    subject = 'Please verify your email address'
    verify_url = reverse('verify_email', kwargs={'username': user.username, 'token': user.auth_token})
    print(user.auth_token)
    verification_link = request.build_absolute_uri(verify_url)
    message = f'Hi {user.username}, please click this link to verify your email: {verification_link}'
    from_email = 'nsemcxgod@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def verify_email(request, username, token):
    try:
        user = User.objects.get(username=username)
        if user.auth_token != token:
            raise User.DoesNotExist
        user.email_varified = True
        user.auth_token = ''
        user.save()
        login(request, user)
        return redirect('signup_success')
    except User.DoesNotExist:
        return render(request, 'myapp/failed.html')


def signup_success(request):
    return render(request,'myapp/success.html')