from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True)
    job_description = models.CharField(max_length=2000)
    skills = models.CharField(default=False,max_length=2000)
    status = models.CharField(default="NotScored",max_length=10)
class Resume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    email = models.EmailField()
    skills = models.CharField(max_length=1000)
    score = models.DecimalField(default=0 , decimal_places=2 , max_digits=4)
    resume_data = models.CharField(max_length=5000)
    #id = models.AutoField(primary_key=True)