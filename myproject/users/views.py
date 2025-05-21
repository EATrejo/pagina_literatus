from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from  users.models import User
from .forms import ContactoForm, SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from .utils import send_password_reset_email



# Create your views here.
@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Bienvenido a Literatus!')
        return redirect('home')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)


        if user is not None:
            auth.login(request, user)
            
        
            if'next' in request.POST:
                messages.success(request, "Bienvenido a Literatus!")
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, "Bienvenido a Literatus!")
                return redirect("home")
                
            
        else:
            messages.error(request, 'Datos invalidos. Favor de registrarse primero.')
            
    return render(request, 'users/login.html')

def logout_user(request):
    auth.logout(request)
    messages.success(request, "¡Acabas de salir de Literatus, nos vemos pronto!")
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, '¡Ya estas registrado!')
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
            messages.success(request, 'Tu cuenta se registró satisfactoriamente!')
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


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Send reset password email
            send_password_reset_email(request, user)

            messages.success(request, 'La contraseña ha sido enviado a tu correo electrónico.')
            return redirect('users:login')
        else:
            messages.error(request, 'Tu cuenta no existe.')
            return redirect('users:forgot_password')
    return render(request, 'users/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Por favor, resetea tu contraseña')
        return redirect('users:reset_password')
    else:
        messages.error(request, 'Este link ya expiró.')
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Contraseña reseteada exitosamente')
            return redirect('users:login')
        else:
            messages.error(request, 'La contraseña no concuerda!')
            return redirect('users:reset_password')
    return render(request, 'users/reset_password.html')



@csrf_exempt
def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            first_name = formulario.cleaned_data['nombre']


            formulario.save()
            
            data["mensaje"] = f"Hola { first_name }, muchas gracias por contactárnos, pronto nos comunicaremos contigo."
            messages.success(request, 'Mensaje enviado')
            return render(request, 'users/contacto.html', data)
        else:
            data["form"] = formulario
            messages.error(request, 'El formulario es incorrecto, por favor de corregirlo')
            return render(request, 'users/contacto.html', data)
    return render(request, 'users/contacto.html', data)





