from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validatorfield(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exist'] = "Email ya registrado"
        else:

            if len(postData['first_name'].strip()) < 2 or len(postData['first_name'].strip()) > 30:
                errors['first_name_len'] = "El nombre debe tener entre 2 y 30 caracteres."

            if len(postData['last_name'].strip()) < 2 or len(postData['last_name'].strip()) > 30:
                errors['last_name_len'] = "El apellido debe tener entre 2 y 30 caracteres."
            
            if not JUST_LETTERS.match(postData['first_name']) or not JUST_LETTERS.match(postData['last_name']):
                errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y el apellido."
                
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Formato correo no válido"
            
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido. Debe contener al menos una mayúscula, una minúscula, al menos un dígito y no contener caracteres especiales."

            if len(postData['password']) < 8 or len(postData['password']) > 16:
                errors['password_len'] = "Largo contraseña no válido. Debe tener entre 8 y 16 caracteres" 

            if postData['password'] != postData['password_confirm']:
                errors['password_confirm'] = "Contraseñas no coinciden."

        return errors    


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    rol = models.CharField(max_length=20, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["email"]



    def __repr__(self) -> str:
        return self.first_name + " " + self.last_name
