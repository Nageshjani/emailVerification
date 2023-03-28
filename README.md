```bash

signup/
├── signup/
│   ├── settings.py
│   ├── urls.py
|
├── myapp/
│   └── views.py
│   └── models.py
│   └── admin.py
|
├── templates/
│       ├── myapp/
│            ├── base.html
│            ├── signup.html
│            ├── email_sent.html
│            ├── success.html
│            ├── failed.html
└── manage.py



```

```bash
django-admin startproject signup
```

```bash
cd signup
```

```bash
python manage.py startapp myapp
```
## settings.py

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'host_email'
EMAIL_HOST_PASSWORD = ''


INSTALLED_APPS = [
    'myapp'
]


import os
TEMPLATES = [
    {
        
        'DIRS': [os.path.join(BASE_DIR,'templates')],        
    },
]

AUTH_USER_MODEL = 'myapp.User'

```








```bash
mkdir templates
cd templates
mkdir myapp
cd myapp
```


```bash
type nul > base.html
type nul > signUp.html
type nul > email_sent.html
type nul > suceess.html
type nul > failed.html
```


#templates/myapp


## base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>

    {% block content %}
    {% endblock %}
    
</body>
</html>

```

## signUp.html

```html

{% extends 'myapp/base.html' %}

{% block content %}

   <h2>Sign Up</h2>
   <form method="post">
       {% csrf_token %}
       <div>
           <label for="username">Username:</label>
           <input type="text" id="username" name="username" required>
       </div>
       <div>
           <label for="email">Email:</label>
           <input type="email" id="email" name="email" required>
       </div>
       <div>
           <label for="password">Password:</label>
           <input type="password" id="password" name="password" required>
       </div>
       <button type="submit">Sign Up</button>
   </form>
{% endblock %}

```

## email_sent.html
```html
{% extends 'myapp/base.html' %}

{% block content %}

   <h2>Verification Email Sent</h2>
   <p>An email has been sent to your email address. Please follow the instructions in the email to verify your account.</p>
{% endblock %}

```

## failed.html
```html

{% extends 'myapp/base.html' %}

{% block content %}

   <h2>Verification Failed</h2>
   <p>The verification link is invalid. Please check the link or contact support.</p>
{% endblock %}

```
## success.html

```html

{% extends 'myapp/base.html' %}

{% block content %}

   <h2>Sign Up Successful</h2>
   <p>Your account has been verified and you are now signed in. Welcome!</p>
{% endblock %}

```






















## signin/urls
```python 
from django.contrib import admin
from django.urls import path
from myapp.views import signupView,verify_email,signup_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signupView,name='signup'),
    path('verify_email/<str:username>/<str:token>/', verify_email, name='verify_email'),
    path('signup_success/', signup_success, name='signup_success'),


]

```

```bash
python manage.py runserver
```

![Screenshot (553)](https://user-images.githubusercontent.com/34247973/228314600-06cf59d8-4a1b-4ab5-a019-fc8652b3e55d.png)


## myapp/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class User(AbstractUser):
    auth_token = models.CharField(max_length=50, blank=True, default='')
    email_varified=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.auth_token:
            self.auth_token = get_random_string(length=20)
        return super(User, self).save(*args, **kwargs)

```
## myapp/admin.pyy
```python
from django.contrib import admin
from .models import User

admin.site.register(User)
```

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
## -------------------------------------------------------------------------------------
## If Error
```python
```
settings.py
# comment out below
INSTALLED_APPS = [
   ...
   #'django.contrib.admin',
   ...
]

```python
urls.py
 #path('admin/', admin.site.urls) 
```
## Run this now
```bash
python manage.py migrate
```
## Finally Uncomment all 
## -------------------------------------------------------------------------------------




```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver
```

![Screenshot (555)](https://user-images.githubusercontent.com/34247973/228314735-98893424-596d-43b7-a042-525df534e084.jpg)






```python
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


```

![Screenshot (556)](https://user-images.githubusercontent.com/34247973/228314803-3dffc746-8d43-427a-aa01-bca411127df8.png)
![Screenshot (558)](https://user-images.githubusercontent.com/34247973/228314842-e256eea6-5a33-436d-a345-93a45e0be603.png)
![Screenshot (559)](https://user-images.githubusercontent.com/34247973/228314870-471823d1-6fdb-427d-9deb-508d103b3ec6.jpg)
![Screenshot (561)](https://user-images.githubusercontent.com/34247973/228314916-a86ff69c-d3c1-46c4-aec6-4770b2c677fc.png)
![Screenshot (562)](https://user-images.githubusercontent.com/34247973/228314958-e2544b8f-3121-4d36-9d7c-cf5c48ff76e8.png)


```bash
http://localhost:8000/verify_email/nse/SnzdAZDrEKTzVEiBUBhg/

```

![Screenshot (563)](https://user-images.githubusercontent.com/34247973/228315076-ea444393-6713-4b21-b2fe-7e424db228b4.png)
![Screenshot (565)](https://user-images.githubusercontent.com/34247973/228315121-5992aa4a-78c3-4162-98f0-66c8f3129e67.jpg)

```bash
'email varified True'
```


## Important

```bash

'Click again that given link, but this time it will fail'
'why?'
'user.save()'
'because first time varifying link, we will save user'
'And every time user is saved save() function in model genertae differnt token in User.auth_token'
'Cool isnt it?'
```


```bash
'token': user.auth_token

user = User.objects.create_user(username=username, email=email, password=password)
user.save()

models.py
def save(self, *args, **kwargs):
        if not self.auth_token:
            self.auth_token = get_random_string(length=20)



verify_url = reverse('verify_email', kwargs={'username': user.username, 'token': user.auth_token})
verification_link = request.build_absolute_uri(verify_url)
def verify_email(request, username, token):

         

```
