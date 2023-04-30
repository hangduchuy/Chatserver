from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout, get_user_model

from chat.models import User, Room, Message
from django.shortcuts import render
from chat.securities import rate_limit

user = get_user_model()


def register_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        pass_confirm = request.POST['password_confirm']
        if password == pass_confirm:
            hashed_password = make_password(password)
            if User.objects.filter(username=username):
                context = {'error': "UserName incorrect"}
                return render(request, 'chat/register.html', context)
            else:
                user = User.objects.create(username=username, email=email, password=hashed_password)
                user.save()

                return HttpResponseRedirect(reverse('login'))
        else:
            context = {'error': "Password incorrect"}
            return render(request, 'chat/register.html', context)
    return render(request, 'chat/register.html')


@rate_limit(requests=10, interval=60)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'chat/login.html', context)

    return render(request, 'chat/login.html')


def room_option(request):
    current_user = request.user
    if request.method == 'POST':
        if 'createroom' in request.POST:
            room_name = request.POST['roomname']
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')

            if password == confirmpassword:
                password = make_password(password)
            room = Room.objects.filter(name=room_name).first()

            if room is not None:
                context = {'error': 'Phòng này đã tồn tại'}
                rooms = Room.objects.filter(members=current_user)
                return render(request, 'chat/index.html', {'rooms': rooms, **context})

            else:
                room = Room.objects.create(name=room_name, password=password)
                room.members.add(current_user)
                room.save()
            return redirect('index')

        elif 'searchroom' in request.POST:
            room_name = request.POST['Roomname']
            password = request.POST.get('password')
            room = Room.objects.filter(name=room_name).first()

            if room == None:
                context = {'error': f'Không có phòng tên {room_name} '}
                rooms = Room.objects.filter(members=current_user)
                return render(request, 'chat/index.html', {'rooms': rooms, **context})

            if password:
                 if check_password(password, room.password):
                    return render(request, 'chat/room.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)),
                    'username': mark_safe(json.dumps(current_user.username)),
                    'user_id': mark_safe(json.dumps(current_user.id)), })
                 else:
                     context = {'error':'Sai mật khẩu phòng '}
                     rooms = Room.objects.filter(members=current_user)
                     return render(request, 'chat/index.html', {'rooms': rooms, **context})

            else:
                  return render(request, 'chat/room.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)),
                    'username': mark_safe(json.dumps(current_user.username)),
                    'user_id': mark_safe(json.dumps(current_user.id)), })

        elif 'delete' in request.POST:
            roomname = request.POST['roomname']
            room = Room.objects.filter(name=roomname)
            room.delete()
            return redirect('index')

    rooms = Room.objects.filter(members=current_user)
    return render(request, 'chat/index.html', {'rooms': rooms})


@login_required
def chatroom(request, room_name):
    if request.user.is_authenticated:
        username = request.user.username
        user_id = request.user.id

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(username)),
        'user_id': mark_safe(json.dumps(user_id)),

    })


def logout_view(request):
    print("da logout thanh cong")
    logout(request)
    return HttpResponseRedirect(reverse('login'))
