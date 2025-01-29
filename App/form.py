from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, JobSeeker, Hirer, HirerPost, JobApplication

class JobSeekerSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ['username','first_name', 'last_name', 'email', 'phone_number']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_jobseeker = True
        user.name = self.cleaned_data.get('name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        jobseeker = JobSeeker.objects.create(user=user)
        # jobseeker.location=self.cleaned_data.get('location')
        jobseeker.save()
        return user

class HirerSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hirer = True
        user.name = self.cleaned_data.get('name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        hirer = Hirer.objects.create(user=user)
        # hirer.designation=self.cleaned_data.get('designation')
        hirer.save()
        return user
    



class PostForm(forms.ModelForm):
    # salary = forms.DecimalField(widget=forms.NumberInput(attrs={'type': 'number'}))
    class Meta:
        model = HirerPost
        fields = ['title', 'experience', 'location', 'salary', 'intake', 'role', 'industry_type', 'department', 'employee_type', 'job_highlights', 'job_purpose', 'education', 'skills_requirement']


class ResponseChoice(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['response']
