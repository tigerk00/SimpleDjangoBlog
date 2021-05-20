from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))

	class Meta:
		model = User
		fields = ["username","email","password1","password2"]

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label="Username",widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(label="Username",widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))

	class Meta:
		model = User
		fields = ["username","email"]

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ["avatar"]

class CommentForm(forms.ModelForm):
	name = forms.CharField(label="Имя",widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
	body = forms.CharField(label="Текст комментария", help_text="До 500 символов", widget=forms.Textarea(attrs={"class": "form-control", "autocomplete":"off", "rows":5}))

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['post'].disabled = True
		self.fields['name'].disabled = True

	class Meta:
		model = Comment
		fields = ("post",'name','body')





