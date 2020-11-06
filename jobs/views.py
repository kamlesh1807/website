from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job , Resume

from django.shortcuts import redirect

from django.core.serializers import serialize
from django.http import JsonResponse
import json
import PyPDF2, re, docx2txt
# Create your views here.


@login_required
def jobs_view(request):
    
    if request.method == "GET":
        jobs = list(Job.objects.filter(user=request.user).values())
        print(jobs)
        return render(request, 'app/jobs.html',{"jobs":jobs})
    
    if request.method == "POST":
        title = request.POST.get("title")
        job_description = request.POST.get("job_description")
        skills = request.POST.get("skills")
        insertObject = Job.objects.create(user=request.user,title=title,job_description=job_description,skills=skills)
        jobs = list(Job.objects.filter(user=request.user).values())
        return render(request, 'app/jobs.html',{"jobs":jobs})

@login_required
def jobDetail(request, pk):
    if request.method == "GET":
        current_job = Job.objects.get(user=request.user,id=pk)
        job = list(Job.objects.filter(user=request.user, id=pk).values())[0]
        resumes = list(Resume.objects.filter(job=current_job).values())
        return render(request, 'app/job.html',{"job": job,"resumes":resumes})
    
    if request.method == "POST":
        current_job = Job.objects.get(user=request.user,id=pk)
        job = list(Job.objects.filter(user=request.user, id=pk).values())[0]
        for f in request.FILES.getlist('files'):
            email, mathcedSkills, data = fetchData(f,job['skills'])
            Resume.objects.create(job=current_job,email=email,skills=mathcedSkills,resume_data=data)
        resumes = list(Resume.objects.filter(job=current_job).values())
        return render(request, 'app/job.html',{"job": job,"resumes":resumes})

    
@login_required
def jobDelete(request, pk):
    Job.objects.filter(id=pk).delete()
    jobs = list(Job.objects.filter(user=request.user).values())
    return redirect('/jobs')
    
    #return render(request, 'app/jobs.html',{"jobs":jobs})


def fetchData(resume, skills):
    
    skills = skills.split(",")
    data = ""
    
    if resume.name[-3:].lower() == "pdf" :
        pdfReader = PyPDF2.PdfFileReader(resume.file)
        number_of_pages = pdfReader.getNumPages()
        for page in range(number_of_pages):
            page = pdfReader.getPage(page)
            data += page.extractText()
        email = re.search(r'[\w\.-]+@[\w\.-]+', data).group(0)
        mathcedSkills = ",".join([skill for skill in skills if skill.lower() in data.lower()])
        
        return email, mathcedSkills, data  

    # if resume.name[-4:].lower() == "docx":
    #     docxReader = docx.Document(resume.file)
    #     print(len(docxReader.paragraphs))
    #     fullText = []
    #     for para in docxReader.paragraphs:
    #         fullText.append(para.text)
    #     print(fullText)
    #     data = '\n'.join(fullText)
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     email = re.search(regex, data)
    #     #email = re.search(r'[\w\.-]+@[\w\.-]+', data).group(0)
    #     mathcedSkills = ",".join([skill for skill in skills if skill.lower() in data.lower()])

    #     return email, mathcedSkills, data

    if resume.name[-4:].lower() == "docx":
        data = docx2txt.process(resume.file)

        email = re.search(r'[\w\.-]+@[\w\.-]+', data).group(0)
        mathcedSkills = ",".join([skill for skill in skills if skill.lower() in data.lower()])
        
        return email, mathcedSkills, data


@login_required
def resumeDelete(request, jid , rid):
    Resume.objects.filter(id=rid).delete()
    return redirect('/job/{}'.format(jid))
    
    #return render(request, 'app/jobs.html',{"jobs":jobs})


       
      
  

