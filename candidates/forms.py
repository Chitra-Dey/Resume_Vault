from django import forms 
from .models import Candidate
from django.contrib.auth.forms import UserCreationForm
from .models import Cususer, StudentProfile

class candidateforms(forms.ModelForm):
    class Meta:
        model=Candidate
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'Tell about yourself',
                'rows': 4,
                'class': 'form-control'
            }),
            'skills': forms.Textarea(attrs={
                'placeholder': 'List your top 5 skills',
                'rows': 3,
                'class': 'form-control'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class StudentSignupForm(UserCreationForm):
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cususer
        fields = ['username', 'email', 'dob', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            StudentProfile.objects.update_or_create(user=user, defaults={'dob': self.cleaned_data['dob']})
        return user

class RecruiterSignupForm(UserCreationForm):
    class Meta:
        model = Cususer
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        if commit:
            user.save()
        return user




   

    