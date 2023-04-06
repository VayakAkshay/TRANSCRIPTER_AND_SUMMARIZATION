from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import speech_recognition as sr
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2
from pathlib import Path
from moviepy.editor import VideoFileClip
from .models import Myfiles,ContactForm
from .forms import FileForm
import os
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import shutil
from threading import Timer
import re

def HandlePassword(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("pass")
        cpass = request.POST.get("cpass")
        if password == cpass:
            myuser = User.objects.create_user(email,mobile,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            full_name = fname + lname
            user = authenticate(username = email,password = password)
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/")
        else:
            messages.warning(request,"Password is not matched ")
            return redirect("/password/")
    return render(request,"Mainpage/index.html")


def Homepage(request):
    form  = FileForm()
    return render(request, "Mainpage/index.html",{"form":form})

def RemoveData():
    shutil.rmtree("media/mydoc/")

def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    if(url):
        return True
    else:
        return False

def UploadFile(request):
    form  = FileForm()
    if request.method == "POST":
        files = Myfiles()
        if len(request.FILES) != 0:
            files.my_file = request.FILES['my_file']
            files.save()
        length = len(Myfiles.objects.all().values())
        file_name = Myfiles.objects.all().values()[length-1]["my_file"]
        file_name = file_name.split("/")[1]
        print("file_name",file_name)
        video = VideoFileClip("media/mydoc/{}".format(file_name))
        num_seconds_video = int(video.duration)
        l = list(range(0, num_seconds_video+1, 60))
        diz = {}
        filedata = Myfiles.objects.filter(my_file = "mydoc/{}".format(file_name)).all().values()
        file_id = filedata[0]["id"]
        parent_dir1 = "media/chunks/"
        parent_dir2 = "media/converted/"
        parent_dir3 = "media/"
        dir_name = "f_{}".format(file_id)
        paths1 = os.path.join(parent_dir1, dir_name)
        paths2 = os.path.join(parent_dir2, dir_name)
        paths3 = os.path.join(parent_dir3, dir_name)
        os.mkdir(paths1)
        os.mkdir(paths2)
        os.mkdir(paths3)
        for i in range(len(l)-1):
            ffmpeg_extract_subclip('media/mydoc/{}'.format(file_name), l[i]-2*(l[i] != 0), l[i+1], targetname="media/chunks/f_{}/cut{}.mp4".format(file_id,i+1))
            clip = mp.VideoFileClip(r"media/chunks/f_{}/cut{}.mp4".format(file_id,i+1))
            clip.audio.write_audiofile(r"media/converted/f_{}/converted{}.wav".format(file_id,i+1))
            r = sr.Recognizer()
            audio = sr.AudioFile("media/converted/f_{}/converted{}.wav".format(file_id,i+1))
            with audio as source:
                r.adjust_for_ambient_noise(source)
                audio_file = r.record(source)
            result = r.recognize_google(audio_file)
            diz['chunk{}'.format(i+1)] = result
            
            l_chunks = [diz['chunk{}'.format(i+1)] for i in range(len(diz))]
            text = '\n'.join(l_chunks)

            with open('media/f_{}/recognized.txt'.format(file_id), mode='w') as file:
                file.write("\n")
                file.write(text)
        text_file = open("media/f_{}/recognized.txt".format(file_id),"r")
        all_text = text_file.readlines()
        result= ""
        for i in all_text:
            result = result + i + ". "
        summarizer = pipeline('summarization')
        summary = ""
        num_iters = int(len(result)/1000)
        summarized_text = []
        for i in range(0, num_iters + 1):
            start = 0
            start = i * 1000
            end = (i + 1) * 1000
            print("input text \n" + result[start:end])
            out = summarizer(result[start:end])
            out = out[0]
            out = out['summary_text']
            print("Summarized text\n"+out)
            summarized_text.append(out)
        data = summarized_text[0]
        r = Timer(3.0, RemoveData)
        r.start()
        datas = {"data": data,
                 "full":result}
        data_list = [datas]
        return render(request, "Mainpage/byfile.html",{"form":form,"data_list":data_list})
    return render(request, "Mainpage/byfile.html",{"form":form})

def LinkScript(request):
    form = FileForm()
    if request.method == "POST":
        link = request.POST.get("link")
        ans = Find(link)
        if(ans):
            video_id = link.split("=")[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            result = ""
            for i in transcript:
                result += ' ' + i["text"]
            summarizer = pipeline('summarization')
            summary = ""
            num_iters = int(len(result)/1000)
            summarized_text = []
            for i in range(0, num_iters + 1):
                start = 0
                start = i * 1000
                end = (i + 1) * 1000
                print("input text \n" + result[start:end])
                out = summarizer(result[start:end])
                out = out[0]
                out = out['summary_text']
                print("Summarized text\n"+out)
                summarized_text.append(out)
            data = summarized_text[0]
            datas = {"data": data,
                    "full":result}
            data_list = [datas]
            return render(request, "Mainpage/bylink.html",{"form":form,"data_list":data_list})
        else:
            messages.warning(request,"Please Enter Valid link")
            return render(request, "Mainpage/bylink.html",{"form":form})
    return render(request,"Mainpage/bylink.html")

def Aboutpage(request):
    return render(request, "Mainpage/about.html")

def ProfilePage(request):
    return render(request,"Mainpage/profile.html")

def EditProfile(request):
    return render(request,"Mainpage/edit_profile.html")

def editpage(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        print(first_name)
        User.objects.filter(username = user).update(first_name = first_name)
        User.objects.filter(username = user).update(last_name = last_name)
        User.objects.filter(username = user).update(email = mobile)
        User.objects.filter(username = user).update(username = email)
        return redirect('/profile/')
    return render(request,'Mainpage/profile')

def Comming_Soon(request):
    return render(request,"Mainpage/comming.html")

def contactPage(request):
    contact = ContactForm()
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        contact.email = email
        contact.message = message
        contact.save()
        messages.success(request,"Your form submitted successfully")
        return redirect("/contact/")
    return render(request,"Mainpage/contact.html")

def logout_page(request):
    logout(request)
    return redirect("/")
