from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserInformation
from django.contrib.auth.views import LoginView
from accounts.utils import COUNTRIES, UndergraduateDegreeChoice, CampusChoice

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.', 
        max_length=152,
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Username', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
    )

    email = forms.CharField(
        label="Correo electrónico",
        max_length=254, 
        required=True, 
        widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': 'info@example.com', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Confirma Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password Confirmation', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
        help_text="Ingrese la misma contraseña para verificación.",
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(LoginView):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=152,
        required=True, 
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Username', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password', 'style': 'background-color: rgba(73, 80, 87, 0.1)'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class EditUserDataForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Primer Nombre', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Primer Nombre', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu nombre.'},
    )

    middle_name = forms.CharField(
        label='Segundo Nombre', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Segundo Nombre', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu segundo nombre.'},
    )

    last_name = forms.CharField(
        label='Apellido', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Apellido', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu apellido.'},
    )

    age = forms.IntegerField(
        label='Edad', 
        required=True,
        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': '18', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu edad.'},
        min_value=18,
        max_value=105,
    )

    mobile = forms.CharField(
        label='Número de Teléfono', 
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': '581234567890', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu número telefónico.'},
        help_text="Ingresa tu número de teléfono sin guiones (-) ni más (+)",
    )

    birthdate = forms.DateField(
        label='Fecha de Nacimiento', 
        required=True,
        widget=forms.DateInput(attrs={'class': "form-control ",'type':'date', 'placeholder': '581234567890', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu fecha de nacimiento.'},
        help_text="Utilice la ventana desplegable para seleccionar su fecha.",
    )

    mailing_city = forms.CharField(
        label='Ciudad', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Ciudad', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu ciudad de envío de correo.'},
    )

    mailing_state = forms.CharField(
        label='Estado', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Estado', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu estado de envío de correo.'},
    )

    mailing_country = forms.ChoiceField(
        label='País', 
        required=True,
        widget=forms.Select(attrs={'class': "form-control dropdown", 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu país de envío de correo.'},
        choices=COUNTRIES,
    )

    usb_alumn = forms.BooleanField(
        label='Estudiante de la USB', 
        required=True,
        error_messages={'required': 'Por favor ingresa si eres o no estudiantes de la USB.'},
    )

    cohorte = forms.IntegerField(
        label='Cohorte', 
        required=True,
        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': '00', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu cohorte.'},
        min_value=0,
        max_value=99,
        help_text="Por ingrese solamente el número de su cohorte (sin carnet).",
    )

    carnet = forms.IntegerField(
        label='Carnet', 
        required=True,
        widget=forms.NumberInput(attrs={'class': "form-control", 'placeholder': '10000', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu carnet.'},
        min_value=10000,
        max_value=15000,
        help_text="Por ingrese solamente el número de su carnet (sin cohorte).",
    )

    undergrad_degree = forms.ChoiceField(
        label='Pregrado', 
        required=True,
        widget=forms.Select(attrs={'class': "form-control dropdown", 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu título de pregrado.'},
        choices=[(tag.name, tag.value) for tag in UndergraduateDegreeChoice],
    )

    usb_undergrad_campus = forms.ChoiceField(
        label='Campus Pregrado USB', 
        required=True,
        widget=forms.Select(attrs={'class': "form-control dropdown", 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa el campus de la universidad de tu pregrado.'},
        choices=[(tag.name, tag.value) for tag in CampusChoice],
    )

    graduate_degree = forms.CharField(
        label='Maestría', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Maestría', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa tu título de maestría, si no tienes puedes colocar "None".'},
    )

    graduate_campus = forms.CharField(
        label='Campus Maestría', 
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Campus Maestría', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
        error_messages={'required': 'Por favor ingresa el campus de la universidad de maestría, si no tienes puedes colocar "None".'},
    )

    workplace = forms.CharField(
        label='Lugar de Trabajo', 
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Boston', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
    )

    work_email = forms.CharField(
        label="Correo electrónico de trabajo",
        max_length=60, 
        required=False, 
        widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': 'info@example.com', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
    )

    donor = forms.BooleanField(
        label='Donante recurrente', 
        required=True,
        error_messages={'required': 'Por favor ingresa si eres o no donante recurrent en AlumnUSB.'},
    )

    social_networks = forms.CharField(
        label='Redes sociales', 
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': '@MiRedSocial', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
    )

    twitter_account = forms.CharField(
        label='Twitter', 
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': '@MiRedSocial', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
    )

    instagram_account = forms.CharField(
        label='Instagram', 
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': '@MiRedSocial', 'style': 'background-color: rgba(233, 229, 200, 0.5)'}),
    )

    class Meta:
        model = UserInformation
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'age',
            'mobile',
            'birthdate',
            'mailing_city',
            'mailing_state',
            'mailing_country',
            'usb_alumn',
            'cohorte',
            'carnet',
            'undergrad_degree',
            'usb_undergrad_campus',
            'graduate_degree',
            'graduate_campus',
            'workplace',
            'work_email',
            'donor',
            'social_networks',
            'twitter_account',
            'instagram_account'
        )


class getUserDataForm(forms.ModelForm):#UserChangeForm):
    """docstring for EditUserData"""
    #message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = UserInformation
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'mailing_city',
            'mailing_state',
            'usb_alumn',
            #'Codigo_Alumn_USB',
            'mailing_country',
            #'Email',
            'mobile',
            'cohorte',
            'birthdate',
            'age',
            'undergrad_degree',
            'graduate_degree',
            'carnet',
            'usb_undergrad_campus',
            'graduate_campus',
            'work_email',
            'workplace',
            'donor',
            'social_networks',
            'twitter_account',
            'instagram_account'
        )

class pictureId(forms.Form):
    Pic_id = forms.IntegerField()