from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SubPod, Brigad, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']


class SubPodForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = SubPod
        fields = ['name']


class BrigadForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Brigad
        fields = ['name', 'sub_pod']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']
