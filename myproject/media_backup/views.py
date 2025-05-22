from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout

from  users.models import User
from .forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('home')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)


        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'users/login.html')
    return render(request, 'users/login.html')

def logout_user(request):
    auth.logout(request)
    messages.success(request, "You have been logged out, see you soon!")
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered!')
        return redirect('home')
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            """
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            return redirect('registerUser')
            """
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, phone_number=phone_number,email=email, password=password)

            user.save()

            """
            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            """
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('home')
            
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)
