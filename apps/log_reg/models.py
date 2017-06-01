from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def register_user(self, postData):
        errors = []
        # 1. run our validations
        if len(postData['name']) < 2:
            errors.append('Name must be 2 characters long!')
        if not len(postData['email']):
            errors.append('Email is required!')
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors.append('Enter a valid email!')
        if len(postData['pword']) < 8:
            errors.append('Password must be 8 characters long!')
        if postData['pword'] != postData['confirm_pword']:
            errors.append('Passwords must match!')
        if self.filter(email=postData['email']):
            errors.append('Email already exists!')

        response_to_views = {}
        # 2. check if validations are true/false
        if not errors:
            # hash postData password
            hashed_password = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
            # if true create user in db
            user = self.create(
                name=postData['name'], email=postData['email'], password=hashed_password, date_birth=postData['date_birth'])
            # created response to views (user, true)
            response_to_views['user'] = user
            response_to_views['status'] = True
            response_to_views['log_or_reg'] = "Thank you for registering!"
            # if false
        else:
            response_to_views['errors'] = errors
            response_to_views['status'] = False
            # created response to views of (errors, false)
        return response_to_views
        # sent response to views (either errors or user and true or false)

    def login_user(self, postData):
        # find user with email for postData
        user = self.filter(email=postData['email'])
        print user
        response_to_views = {}
        # if not User
        if not user:
            # create errors
            response_to_views['status'] = False
            response_to_views['errors'] = 'Email address not found!'
            print response_to_views
            print "**** NOT USER IN THE IF STATEMENT***"
        # else we have a user
        else:
            # validate password from postData & compare to hashed_password from db
            print "**** USER EXISTS CHECKING IF PW MATCHES****"
            print postData
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                # if true send user to views with true
                response_to_views['status'] = True
                response_to_views['user'] = user[0]
                response_to_views['log_or_reg'] = "Thanks for logging in!"
                print response_to_views
            else:
                # if false send errors to views, flase
                response_to_views['status'] = False
                response_to_views['errors'] = 'Password does not match!'
        # send response_to_views
        return response_to_views


class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_birth = models.DateField(auto_now=False)
    objects = UserManager()
