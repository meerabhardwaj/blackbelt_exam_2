from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.


def appointments(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to continue!")
        return redirect('login: main')
    else:
        user_id = request.session['user_id']
        context = {
            "user": User.objects.get(id=user_id),
            "users": User.objects.exclude(id=user_id)
            # created context for appointments for today
            # create context for appointments in the future
        }
    return render(request, 'appointments/appointments.html', context)


def show(request, id):
    pass


def add_new(request):
    pass


def delete(request, id):
    pass


def update(request, id):
    pass
