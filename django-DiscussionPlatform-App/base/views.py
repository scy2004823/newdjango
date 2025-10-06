from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
# from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message,About,User
from .forms import RoomForm,UserForm,AboutForm,MyUserCreationForm
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if (request.method == 'POST'):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            print('BOOM')
            messages.error(request,'User Not Found')
        
        user  = authenticate(request,email = email,password = password)

        if (user is not None):
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password is incorrect')

    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    context = {'page':page,'form':form}
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            About.objects.create(user=user, about="")
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An Error has occurred during registration")

    return render(request,'base/login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) |
        Q(host__username__icontains = q)
    )
    room_count = rooms.__len__
    topics = Topic.objects.all()[0:6]
    room_messages = Message.objects.filter(Q(room__name__icontains=q))


    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    # Getting all the messages related to this room..This is a one to many relationship defined in models.py
    # for that we are using message_set.all() where message is the Model name Message..It will become lower case
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


def userProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    try:
        about = About.objects.get(user=user)
    except About.DoesNotExist:
        about = ""
    context = {'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages,'about':about}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        # Sending all the post data to the form..The RoomForm() knows what fields to extract
        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        room.participants.add(request.user)

        return redirect('home')
    context = {'form':form,"topics":topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    # The RoomForm will get pre - filled with the room values...If the values dont match it wont work
    form = RoomForm(instance = room)
    if request.user != room.host:
        return HttpResponse('Only the creater can edit the room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    up  = True                       
    context = {'form':form,"topics":topics,"up":up,"room":room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('Only the creater can delete the room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('You cannot delete this message.')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)
    if (request.method == 'POST'):
        form = UserForm(request.POST,request.FILES,instance = user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    return render(request,'base/update-user.html',{"form":form})


@login_required(login_url='login')
def updateAbout(request):
    user = request.user
    # Check if user already has an About instance
    try:
        about_instance = About.objects.get(user=user)
    except About.DoesNotExist:
        about_instance = None

    if request.method == 'POST':
        if about_instance:
            form = AboutForm(request.POST, instance=about_instance)
        else:
            form = AboutForm(request.POST)
        
        if form.is_valid():
            # Save the form
            about = form.save(commit=False)
            about.user = user  # Ensure the user is set
            about.save()
            return redirect('profile', pk=user.id)  # Redirect to the profile page
    else:
        # Display the form for GET requests (editing existing 'About' or creating new)
        form = AboutForm(instance=about_instance)
    
    return render(request, 'base/update-about.html', {"form": form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,"base/topics.html",{"topics":topics})

def activitiesPage(request):
    room_messages = Message.objects.all()[0:4]
    return render(request,"base/activity.html",{"room_messages":room_messages})