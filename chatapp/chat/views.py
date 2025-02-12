from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Message,Notification
from .forms import SignupForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

@login_required
def home(request):
    return render(request, 'base.html')


@login_required
def chat_view(request, receiver_username=None):
    users = User.objects.exclude(id=request.user.id)
    receiver = None
    messages = []

    if receiver_username:
        receiver = get_object_or_404(User, username=receiver_username)
        messages = Message.objects.filter(
            sender=request.user, receiver=receiver
        ) | Message.objects.filter(
            sender=receiver, receiver=request.user
        )
        messages = messages.order_by('timestamp')

    return render(request, 'chat.html', {
        'users': users,
        'receiver': receiver,
        'messages': messages
    })



@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    data = [{"id": n.id, "message": n.message, "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")} for n in notifications]
    return JsonResponse({"notifications": data})




@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message')

        if receiver_id and message_text:
            receiver = get_object_or_404(User, id=receiver_id)
            message = Message.objects.create(sender=request.user, receiver=receiver, message=message_text)
            
            # Create a notification for the receiver
            Notification.objects.create(user=receiver, message=f"New message from {request.user.username}")

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
