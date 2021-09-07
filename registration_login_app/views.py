from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt


# Create your views here.
def home(request):
    return render(request,'registration_login_app/login.html')
    

def register(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        if request.method == 'POST':
            errors = User.objects.validatorfield(request.POST)

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)

                #if there exist errors but recover the data..
                request.session['register_name'] = request.POST['first_name']
                request.session['register_last_name'] = request.POST['last_name']
                request.session['register_email'] = request.POST['email']
            
            else:
                request.session['register_name'] = ""
                request.session['register_last_name'] = ""
                request.session['register_email'] = ""

                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

                obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password_hash)
                messages.success(request, "¡Successful user registration!")

            return redirect('/')
      
        return render(request, 'registration_login_app/login.html')
                
def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        if request.method == 'POST':

            user = User.objects.filter(email=request.POST['email_login'])

            if user :
                registered_user = user[0]

                if bcrypt.checkpw(request.POST['password_login'].encode(), registered_user.password.encode()):
                    usuario = {
                        'id': registered_user.id,
                        'first_name': registered_user.first_name,
                        'last_name': registered_user.last_name,
                        'email': registered_user.email,
                        'rol': registered_user.rol,
                    }

                    request.session['usuario'] = usuario
                    messages.success(request, "Ingreso correcto")
                    return redirect('/success')
            else:
                messages.error(request, "Datos mal ingresados o el usuario no existe")
                return redirect('/')
        else:
            messages.error(request, "Datos mal ingresados o el usuario no existe")
            return redirect('/')

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect('/')

def success(request):
    if 'usuario' not in request.session:
        return redirect('/')
        
    return render(request, 'registration_login_app/success.html')