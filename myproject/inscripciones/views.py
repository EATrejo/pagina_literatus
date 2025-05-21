from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from tertulias.models import Tertulia
from .models import User
from .models import Student
from .forms import TertuliaRegistro
from django.contrib import messages
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode



#@login_required(login_url="/users/login/")
def inscripcion_tertulia(request):
        
        if request.method == 'POST':
           
            form = TertuliaRegistro(request.POST)
            if form.is_valid():

                user = request.user
                first_name = form.cleaned_data['first_name']
                
                last_name = form.cleaned_data['last_name']

                #request.session['last_name'] = last_name
                
                #username = form.cleaned_data['username']
                
                phone_number = form.cleaned_data['phone_number']

                tertulia_name = form.cleaned_data['tertulia_name']
                tertulia_folio_id = form.cleaned_data['tertulia_folio_id']

                

                email = form.cleaned_data['email']


                

                student = Student.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, tertulia_name = tertulia_name, tertulia_folio_id=tertulia_folio_id )
                
                

                student.save()
                print(student)
                print(student.last_name)
                print(user)



                send_verification_email(request, user)
                messages.success(request, 'Te enviamos un correo de verificacion a tu correo electrónico para que puedas continuar con tu proceso de inscripcion!')
                return redirect('home')
            else:
                print('Invalid form')

        else:
            form = TertuliaRegistro()
        context = {
            'form': form,
        }

        return render(request, 'inscripciones/tertulias_registro.html', context)


def activate(request, uidb64, token):
    #Activate the inscription by setting the is_active status to True
    try:
         uid = urlsafe_base64_decode(uidb64).decode()
         user = User._default_manager.get(pk=uid)
         request.session['uid']  = uid
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
         user = None

    if user is not None and default_token_generator.check_token(user, token):
         user.is_active = True
         user.save()
         messages.success(request, 'Felicidades, ya tienes un lugar reservado en la Tertulia.')
         return redirect('inscripciones:welcome_tertulia_page')
    else:
         messages.error(request, 'Invalide activation link')
         return redirect('home')
    

def welcome_tertulia_page(request):
    pk = request.session.get('uid')
    user = User.objects.get(pk=pk)
    user_email = user.email
    
    student = Student.objects.filter(email=user_email).first()


    student_id = student.id
    student_first_name = student.first_name
    student_last_name = student.last_name
    student_tertulia_name = student.tertulia_name
    student_tertulia_folio_id = student.tertulia_folio_id



    tertulia = Tertulia.objects.get(id=student.tertulia_folio_id)
    tertulia_nombre_encargado = tertulia.tertulia_encargado
    tertulia_inicio = tertulia.tertulia_fecha_de_inicio
    tertulia_horario = tertulia.tertulia_horario

    tertulia.tertulia_lugares -= 1
    tertulia.save()

    

    
    
    
    context = {
        'student_id': student_id,
        'student_first_name': student_first_name,
        'student_last_name':  student_last_name,
        'student_tertulia_name': student_tertulia_name,
        'student_tertulia_folio_id': student_tertulia_folio_id,
        'tertulia_inicio': tertulia_inicio,
        'tertulia_horario': tertulia_horario,
        'tertulia_nombre_encargado': tertulia_nombre_encargado,

    }

    return render(request, 'inscripciones/welcome_tertulia_page.html', context)


def no_hay_lugares(request):
     return render(request, 'inscripciones/no_hay_lugares.html')


    


    


         


