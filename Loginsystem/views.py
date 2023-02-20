from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import OTP_Data
from email.message import EmailMessage
import ssl
from django.contrib.auth import authenticate, login, logout
import smtplib


def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("email_id")
        password = request.POST.get("password")
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/")
        else:
            messages.warning(request,"Please Enter Valid username and Password")
            return redirect("/login/")
    return render(request,'Loginsystem/Login.html')
    
def RegesterPage(request):
    enable_otp = 0

    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        m_number = request.POST.get("mnumber")
        if User.objects.filter(username=email).exists():
            messages.warning(request,"This user is already exist")
        else:
            otp_generate = random.randrange(1000, 9999)
            OTP_data = OTP_Data(email_id = email,otp = otp_generate)
            OTP_data.save()
    
            email_sender = 'crowdfunding.help.0@gmail.com'
    
            email_password = 'qdxzvwpvwjypgbzr'
            email_receiver = email
    
            subject = "OTP"
            body = """
            Welcome to Crowd Funding 
            Your OTP is - {}""".format(otp_generate)
            em = EmailMessage()
            em['from'] = email_sender
            em['to'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
    
            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            enable_otp = 1
    return render(request,'Loginsystem/regester.html',{"enable_otp":enable_otp})

def PasswordPage(request):
    local_data = 0
    if request.method == "POST":
        email = request.POST.get("mailid")
        otp = request.POST.get("otp")
        mydata = OTP_Data.objects.filter(email_id=email).values()
        otp_field = str(mydata)[-7:-3]
        if otp == otp_field:
            otp_data = OTP_Data.objects.filter(email_id = email)
            otp_data.delete()
            local_data = 1
            return render(request,"Loginsystem/password.html",{"local_data":local_data})
        else:
            enable_otp = 1
            messages.warning(request,"Please Enter Valid OTP")
            return render(request,"Loginsystem/regester.html",{"enable_otp":enable_otp})
    return render(request,"Loginsystem/password.html")

def forgot_otp(request):
    enable_otp = 0
    if request.method == "POST":
        email = request.POST.get("email_id")
        user = User.objects.filter(username = email)
        print(user)
        if user is not None:
            otp_generate = random.randrange(1000, 9999)
            OTP_data = OTP_Data(email_id = email,otp = otp_generate)
            OTP_data.save()
            email_sender = 'crowdfunding.help.0@gmail.com'
            email_password = 'qdxzvwpvwjypgbzr'
            email_receiver = email
            subject = "OTP"
            body = """
            Welcome to Crowd Funding 
            Your OTP is - {}""".format(otp_generate)
            em = EmailMessage()
            em['from'] = email_sender
            em['to'] = email_receiver
            em['subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            enable_otp = 1
            return render(request,'Loginsystem/forgot.html',{"enable_otp":enable_otp})
        else:
            messages.warning(request,"Please Enter Valid username and Password")
    return render(request,'Loginsystem/forgot.html')

def forgot_pass(request):
    if request.method == "POST":
        email = request.POST.get("mail_id")
        print(email)
        otp = request.POST.get("otp")
        mydata = OTP_Data.objects.filter(email_id=email).values()
        print(mydata)
        otp_field = str(mydata)[-7:-3]
        print(otp_field)
        print("DKMD")
        if otp == otp_field:
            otp_data = OTP_Data.objects.filter(email_id = email)
            otp_data.delete()
            print("PASS")
            local_data = 1
            return render(request,"Loginsystem/forgot_pass.html",{"local_data":local_data})
        else:
            enable_otp = 1
            messages.warning(request,"Please Enter Valid OTP")
            return render(request,"Loginsystem/forgot.html",{"enable_otp":enable_otp})
    return render(request,'Loginsystem/forgot.html')

def new_pass(request):
    if request.method == "POST":
        email = request.POST.get("mail_id")
        password = request.POST.get("pass")
        cpassword = request.POST.get("cpass")
        if password == cpassword:
            user = User.objects.get(username = email)
            user.set_password(password)
            user.save()
            messages.success(request,"Your password has been changed")
            return redirect("/")
        else:
            messages.warning(request,"Doesn't match password")
            return render(request,"Loginsystem/forgot_pass.html")
    return redirect("/")