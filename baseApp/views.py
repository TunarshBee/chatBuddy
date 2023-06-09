from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Room, Topic, User
from .form import RoomForm, UserForm, RegistrationForm
# Create your views here.


def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(Q(topic__name__icontains=query) | Q(name__icontains=query) | Q(host__username__icontains=query) | Q(description__icontains=query))
    fullTopics = Topic.objects.all()
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    
    activityMsg = Message.objects.filter(Q(room__topic__name__icontains = query))
    for index, topic in enumerate(fullTopics):
        if topic.room_set.count() == 0:
            ftopic = Topic.objects.get(id = topic.id)
            topicRoom = ftopic.room_set.all()
            ftopic.delete()
            topicRoom.delete()
        
    context = {"rooms":rooms, "topics":topics,"room_count":room_count, "activeityMessages":activityMsg}
    return render(request, "base/home.html", context)


def room(request, idParam):
    room = Room.objects.get(id=idParam)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    context = {"room": room, 'room_messages':room_messages, "participants":participants}

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            msgBody = request.POST.get('msgBody')
        )
        room.participants.add(request.user)
        
        return redirect('room', idParam = room.id)
    if room.participants.count() == 0:
        room.participants.add(room.host.id)
    return render(request, "base/room.html", context)


def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    activeityMessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user":user, "rooms":rooms, "topics":topics, "activeityMessages":activeityMessages}
    return render(request, "base/profile.html", context)
    
def topics(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=query)
    return render(request, 'base/topics.html', {"topics":topics})


def activity(request):
    room_messages = Message.objects.all()

    return render(request, 'base/activity.html', {"room_messages":room_messages})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = email)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "email or password is incorrect, please try again")
    context = {}
    return render(request, "base/login.html",  context)


def registerUser(request):
    form = RegistrationForm()
    room = Room.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Error creating user, please try again later')

    return render(request, 'base/register.html', {'form':form})


def logoutUser(request):
    logout(request)
    return redirect('home')



@login_required(login_url="login")
def createRoom (request):
    form = RoomForm()
    topics = Topic.objects.all()

   
            
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room = Room.objects.create(
            host = request.user,
            name = request.POST.get('name'),
            topic = topic,
            description = request.POST.get('description') 
        )
        room.participants.add(room.host.id)
        return redirect('home')
    print("data", form)
    context = {"form":form, 'topics': topics}
    return render(request, "base/create_room.html", context )

@login_required(login_url="login")
def updateRoom(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance=room )
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed to perform this operation")
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name =  topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description= request.POST.get('description')
        room.save()
        return redirect("home")
    context ={"form":form, "topics":topics}
    return render(request, "base/create_room.html", context)

@login_required(login_url="login")
def deleteRoom(request, id):
    
    room = Room.objects.get(id = id)
    if request.user != room.host:
        return HttpResponse("You are not allowed to perform this operation")
    if request.method == 'POST':

        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":room})


@login_required(login_url="login")
def deleteMsg(request, id):
    message = Message.objects.get(id = id)
    if request.user != message.user:
        return HttpResponse("You are not allowed to perform this operation")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":message})


@login_required(login_url="login")
def editMsg(request, id):
    room = Room.objects.get(id=id)
    message = Message.objects.get(id = id)
    if request.user != message.user:
        return HttpResponse("You are not allowed to perform this operation")
    if request.method == "POST":
          message.msgBody = request.POST.get('msgBody')
          message.save()
          return redirect('room', idParam = room.id)
    return render(request, 'base/edit.html', {"obj":message})

@login_required(login_url="login")
def editUser(request):    
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', id = user.id)
    return render(request, 'base/editProfile.html', {"form":form})

# @login_required(login_url='login')
# def like(request, id):
#     message = get_object_or_404(Message, id = request.POST.get('id'))
#     message.likes.add(request.user)
#     return HttpResponseRedirect(reverse('home'), args=[str(id)])

# @login_required(login_url='login')
# def unLike(request, id):
#     if request.method == "GET":
#         message = get_object_or_404(Message, id = request.GET.get('unlike_id'))
#         if message.likes.count(request.user) == 1:
#             message.likes.remove(request.user)
#         message.unLikes.add(request.user)
    
#     return HttpResponseRedirect(reverse('home'), args=[str(id)])

# @login_required(login_url='login')
# def saveMsg(request, id):
#     if request.method == "PATCH":
#         message = get_object_or_404(Message, id = request.PATCH.get('save_id'))
#         return message.saveMsg.add(request.user)
        
#     return HttpResponseRedirect(reverse('home'), args=[str(id)])