from django import forms

from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'middle_name', 'last_name', 'role']
        
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if CustomUser.get_by_email(email):
            raise forms.ValidationError("User with this email already exists")
        
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        
        password = self.cleaned_data.get('password')
        user.set_password(password)
        
        role = self.cleaned_data.get('role')
        
        if role == 1:
            user.is_staff = True
            user.is_superuser = True
        
        
        if commit:
            user.save()
        
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())