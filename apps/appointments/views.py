from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event
from ..log_reg.models import User
from datetime import datetime
# Create your views here.


def appointments(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to continue!")
        return redirect('login: main')
    else:
        user_id = request.session['user_id']
        context = {
            "time": datetime.now().strftime('%B %d, %Y'),
            "user": User.objects.get(id=user_id),
            "users": User.objects.exclude(id=user_id),
            'events': Event.objects.all(),
            'today_schedule': Event.objects.all(),
            'future_schedule': Event.objects.all()
        }
    return render(request, 'appointments/appointments.html', context)


def show(request, id):
    event_id = Event.objects.filter(id=1)
    return render(request, 'appointments/show.html', id=event_id)


def add_new(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            new_event = Event.objects.add_event(request.POST, request.session['user_id'])
            if not new_event['status']:
                messages.add_message(request, messages.INFO, "appointment not added")

    return redirect("schedule:appointments")


def delete(request, id):
    pass


def update(request, id):
    pass
