from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User

# Create your models here.


class EventManager(models.Manager):
    def add_event(self, postData, user_id):
        errors = []

        # validation errors! can't be empty
        if len(postData['task']) < 1:
            errors.append("Need to have a name for your task!")
        if len(postData['date']) < 1:
            errors.append("Need to have a date!")
        if len(postData['time']) < 1:
            errors.append("Need to have a time!")
        # if date and time are not in the future_schedule return errors

        # if there is another event during the same date and time return conflict

        if len(errors):
            return{
                'status': False,
                'errors': errors
            }
        else:
            return{
                'status': True,
                'new_event': self.create(task=postData['task'], date=postData['date'], time=postData['time'], user=User.objects.get(id=user_id))
            }

    def delete_event(self, id, user_id):
        errors = []
        response = {}
        event = Event.objects.filter(id=id)
        if event:
            event[0].delete()
            response['status'] = True
        else:
            errors.append("product wasn't found")
            response['status'] = False
        return response

    def update_event(self, id, user_id):
        pass


class Event(models.Model):
    task = models.CharField(max_length=45)
    date = models.DateField(auto_now=False)
    time = models.TimeField(auto_now=False)
    status = models.CharField(max_length=45, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, related_name="user_added_event")

    objects = EventManager()
