from django import forms
from django.contrib.auth.forms import UserCreationForm
from jobs.models import Jobs

class JobsForm():
    title = forms.CharField(
        label='Software Developer',
        max_length=254,
        required=True,
    )

    job_description = forms.TextInput(
        label='',
        max_length=2000,
        min_length=50,
        required=True,
    )

    skills = forms.CharField(
        label='',
        max_length=100,
        min_length=1,
        required=True,
    )
    
    class Meta:
        model = Jobs
        fields = ('title', 'job_description', 'skills', "status")
