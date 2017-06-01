from django.shortcuts import render, redirect
from django.contrib import messages
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
            "users": User.objects.exclude(id=user_id)
        }
        # created context for appointments for today_schedule << used in html
        # create context for appointments in the future_schedule <<used in html
    return render(request, 'appointments/appointments.html', context)


def show(request, id):
    pass


def add_new(request):
    pass


def delete(request, id):
    pass


def update(request, id):
    pass
