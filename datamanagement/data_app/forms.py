from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Customer

class MakerRegisterForm(UserCreationForm):
    selected_checker = forms.ModelChoiceField(queryset=User.objects.filter(user_type='checker'), required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'user_type', 'selected_checker']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'maker'
        selected_checker = self.cleaned_data.get('selected_checker')
        if selected_checker:
            user.selected_checker = selected_checker
        if commit:
            user.save()
        return user

class CheckerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'user_type']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'checker'
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'photo', 'resume']



