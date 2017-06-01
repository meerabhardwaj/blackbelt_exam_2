from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.


def main(request):

    return render(request, 'log_reg/main.html')


def registration(request):
    # invoke method from models and capture response
    response_from_models = User.objects.register_user(request.POST)
    # check to see if response is true
    if response_from_models['status']:
        request.session['user_id'] = response_from_models['user'].id
        # if true save user id in session
        request.session['log_or_reg'] = response_from_models['log_or_reg']
        # access 'log_or_reg' key from response from models database
        return redirect('schedule:appointments')
    # redirect to appointments page in schedule app
    # else
    else:
        # send error messages to client
        for error in response_from_models['errors']:
            messages.error(request, error)
        return redirect('login:main')
    # render redirect to main page


def login(request):
    # invoke method from models & capture the response
    print '*' * 80
    response_from_models = User.objects.login_user(request.POST)

    # access users from database
    print response_from_models
    # check to see if response is true
    if response_from_models['status']:
        request.session['user_id'] = response_from_models['user'].id
        request.session['log_or_reg'] = response_from_models['log_or_reg']
    # if true save user id & whether they logged in or registered in session in session
        return redirect('schedule:appointments')
    # redirect to appointments page
    # else
    else:
        # send error messages to client
        messages.error(request, response_from_models['errors'])
        return redirect('login:main')
    # render redirect to main page
    return redirect('schedule:appointments')
    # redirect to appointments page


def appointments(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to continue!")
        return redirect('login: main')
    else:
        user_id = request.session['user_id']
        context = {
            "user": User.objects.get(id=user_id),
            "users": User.objects.exclude(id=user_id)
        }
    return render(request, 'appointments/appointments.html', context)


def logout(request):
    request.session.clear()
    return redirect('login:main')
