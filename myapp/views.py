from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from .models import Designer
from django.conf import settings
from django.core.mail import send_mail
import random
import time
from django.db import IntegrityError

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

def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            messages.error(request,"User already exists !")
            return render(request,'sign-up.html')
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                u_type = request.POST.get('usertype')
                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    contact = request.POST['contact'],
                    usertype = u_type

                )
                messages.success(request, "sign-up Successful !")
                return redirect ('login')
            else:
                messages.error(request, "Password and Confirm Password do not match !")
                return render(request, 'sign-up.html')
    else:
        return render (request,'sign-up.html')
    

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['usertype'] = user.usertype
                if user.uprofile:
                    request.session['profile'] = user.uprofile.url
                else:
                    request.session['profile'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnSSxXHLqu5lsHYkFlZkvXuo2ZamNvdqLiCg&s"
        
                messages.success(request,"Login Successful !")
                return redirect('home')
            else:
                messages.error(request, "Incorrect Credentials !")
                return render (request,'login.html')
        except User.DoesNotExist:
            messages.error(request,"Account Does not Exists !")
            return render(request,'login.html')
    else:
        return render (request,'login.html')

def logout(request):
    request.session.flush()
    messages.success(request,"Logout Successful !")
    return redirect('login')

def fpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            subject = 'OTP for Forgotten-Password !'
            otp = random.randint(111111,999999)
            msg = 'Hi ' + user.name + ', Your OTP is : ' + str(otp) + '.' 
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.email]
            send_mail(subject,msg,email_from,recepient_list)

            request.session['resetpass_email'] = user.email
            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()

            messages.success(request,'OTP sent successfully !')
            return redirect ('otp')
        except User.DoesNotExist:
            messages.error(request,'Email does not exist !')
            return render(request,'forgot-password.html')
    else:
        return render(request,'forgot-password.html')


def otp(request):

    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first !")
        return redirect('fpass')
    
    created_time = request.session.get('otp_timestamp', 0)
    current_time = time.time()
    elapsed_time = int(current_time - created_time)
    seconds_left = max(0, 60 - elapsed_time) 

    if request.method == "POST":
        try:
            saved_otp = request.session.get('otp')
            user_otp = request.POST.get('uotp') 

            if seconds_left <= 0:
                messages.error(request, "OTP Expired !")
                return render(request, 'otp.html', {'seconds_left': 0}) 
            
            if saved_otp and user_otp and int(saved_otp) == int(user_otp):
                del request.session['otp'] 
                messages.success(request, "OTP Verified!")
                return redirect('newpass')
            
            else:
                messages.error(request, 'Invalid OTP !')
                return render(request, 'otp.html', {'seconds_left': seconds_left})
        
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid number !')
            return render(request, 'otp.html', {'seconds_left': seconds_left})

    return render(request, 'otp.html', {'seconds_left': seconds_left})

def resend_otp(request):
    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first !")
        return redirect('fpass')
    
    email = request.session.get('resetpass_email')
    
    if email:
        try:
            user = User.objects.get(email=email)
            new_otp = random.randint(111111, 999999)
            request.session['otp'] = new_otp
            request.session['otp_timestamp'] = time.time() # Reset the 60s timer

            subject = 'New OTP for Forgotten-Password!'
            msg = f'Hi {user.name}, Your NEW OTP is : {new_otp}.'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, msg, email_from, [user.email])
            
            messages.success(request, "A new OTP has been sent !")
            return redirect('otp')
            
        except User.DoesNotExist:
            messages.error(request, "User account error !")
            return redirect('fpass')
    else:
        messages.error(request, "Session expired. Please enter your email again !")
        return redirect('fpass')

def newpass(request):
    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first!")
        return redirect('fpass')
    
    if request.method == "POST":
        np = request.POST.get('npass')
        cnp = request.POST.get('cnpass')
        
        if np == cnp:
            try:
                user = User.objects.get(email=request.session['resetpass_email'])
                user.password = np  
                user.save()

                request.session.flush() 
                
                messages.success(request, "Password reset successful! Please login.")
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, "User not found. Please try again.")
                return redirect('fpass')
        else:
            messages.error(request, "Passwords do not match!")
            return render(request, 'new-password.html')

    return render(request, 'new-password.html')

def uprofile(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == "POST":
        user.name = request.POST['name']
        user.contact = request.POST['mobile']

        if 'uprofile' in request.FILES:
            user.uprofile = request.FILES['uprofile']
            user.save() 
            request.session['profile'] = user.uprofile.url

        elif request.POST.get('remove_image_flag') == "true":

            if user.uprofile:
                user.uprofile.delete(save=False)
                
            user.uprofile = None
            request.session['profile'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnSSxXHLqu5lsHYkFlZkvXuo2ZamNvdqLiCg&s"

        user.save()
        messages.success(request, "Profile Updated Successfully!")
        return redirect('uprofile')
    else:   
        return render(request, 'uprofile.html', {'user': user}) 
    
def changepass(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == "POST":
        try:
            if user.password == request.POST['opass']:
                if request.POST['npass'] == request.POST['cnpass']:
                    user.password = request.POST['npass']
                    user.save()
                    messages.success(request,"Password Updated Successfully !")
                    return redirect("uprofile")
                else:
                    messages.error(request,"New Password and Confirm New Password does not match ! ")
                    return render(request, 'changepass.html')
            else:
                messages.error(request,"Old Password is Incorrect !")
                return render(request, 'changepass.html')
        except:
            pass
    else:
        return render(request, 'changepass.html')
    

def add_design(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == "POST":
        try:
            Designer.objects.create(
                user=user,
                dname=request.POST['dname'],
                dcategory=request.POST['dcategory'],
                dstartprice=request.POST['dprice'],
                dsummary=request.POST['dsummary'],
                dimage=request.FILES['dimage'],
                dimage2=request.FILES.get('dimage2'), 
                dimage3=request.FILES.get('dimage3')
            )
            messages.success(request, "Design added successfully !")
            return redirect('manage_design')
        
        except IntegrityError:
            messages.error(request,f"You already have a design named '{request.POST['dname']}'. Please use a unique name !")
            return render(request, 'add_design.html') 
            
    return render(request, 'add_design.html')

def manage_design(request):
    user = User.objects.get(email = request.session['email'])
    designer = Designer.objects.filter(user = user)

    return render(request,'manage_design.html',{'designer' : designer})

def edit_design(request,pk):
    try:
        user = User.objects.get(email=request.session['email'])
        design = Designer.objects.get(id=pk, user=user) 
    except (User.DoesNotExist, Designer.DoesNotExist):
        messages.error(request, "Design not found !")
        return redirect('manage_design')

    if request.method == "POST":
        design.dname = request.POST['dname']
        design.dstartprice = request.POST['dprice']
        design.dsummary = request.POST['dsummary']
        if request.FILES.get('dimage'):
            design.dimage = request.FILES.get('dimage')
        if request.FILES.get('dimage2'):
            design.dimage2 = request.FILES.get('dimage2')
        if request.FILES.get('dimage3'):
            design.dimage3 = request.FILES.get('dimage3')

        design.save()
        
        messages.success(request, "Design Updated Successfully !")
        return redirect('edit_design',pk=design.id) 
    
    else:   
        return render(request, 'edit_design.html', {'design': design})
    
def delete_design(request, pk):
    try:
        user = User.objects.get(email=request.session['email'])
        design = Designer.objects.get(id=pk, user=user) 
        design.delete()
        
        messages.success(request, "Design Deleted Successfully !")
        return redirect('manage_design') 
        
    except (User.DoesNotExist, Designer.DoesNotExist):
        messages.error(request, "Design not found !")
        return redirect('manage_design')
    
def home(request):
    context = {}
    context['all_designs'] = Designer.objects.all().order_by('-id')[:6] 
    
    user_design_count = 0
    if 'email' in request.session:
        try:
            user = User.objects.get(email=request.session['email'])
            context['user'] = user
            user_design_count = Designer.objects.filter(user=user).count()
            total_design_count = Designer.objects.count()
            design = Designer.objects.all()
        except User.DoesNotExist:
            pass
    context['my_count'] = user_design_count
    context['total_count'] = total_design_count
    context['design'] = design

    return render(request, 'home.html', context)

def design_info(request):
    return render(request , 'design_info.html')







                    




            

    
            

