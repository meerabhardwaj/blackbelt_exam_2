from django.shortcuts import render, redirect, reverse
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
    if not 'user_id' in request.session:
        messages.add_message(request, messages.ERROR, "Please login.")
        return redirect('login:main')
    context = {
        'events': Event.objects.filter(id=id)
    }
    return render(request, 'appointments/show.html', context)


def add_new(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            new_event = Event.objects.add_event(request.POST, request.session['user_id'])
            if not new_event['status']:
                messages.add_message(request, messages.INFO, "appointment not added")

    return redirect("schedule:appointments")


def delete(request, id):
    result = Event.objects.deleteProduct(id=appointment.id)
    if not result['status']:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)
    else:
        messages.add_message(request, messages.SUCCESS, "Say goodbye to that task!")
    return redirect('schedule:appointments')


def update(request, id):
    pass


def catcher(request):
    return redirect(reverse("schedule:appointments"))
