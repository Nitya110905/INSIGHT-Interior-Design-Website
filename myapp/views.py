from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def feature(request):
    return render(request,'feature.html')

def project(request):
    return render(request,'project.html')

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def SignUp(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            messages.error(request,"User already exists!!!")
            return render(request,'Sign-Up.html')
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    contact = request.POST['contact']
                )
                messages.success(request, "Sign-Up Successful !!!")
                return redirect ('login')
            else:
                messages.error(request, "Password and Confirm Password do not match !!!")
                return render(request, 'Sign-Up.html')
    else:
        return render (request,'Sign-Up.html')
    

def Login(request):
    return render(request,'Login.html')
            

