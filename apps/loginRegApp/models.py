from __future__ import unicode_literals
from django.db import models

import re 

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[a-zA-Z\s]$')

class RegistrationManager(models.Manager):
    def registration_validator(self,postData):
        errors={}
        if len(postData['txtFirst'])<1 or NAME_REGEX.match(postData['txtFirst']):
            errors['fName']="First name should be letters only."
        if len(postData['txtLast'])<1 or NAME_REGEX.match(postData['txtLast']):
            errors['lName']="Last name should be letters only."
        if not EMAIL_REGEX.match(postData['txtEmail']):
            errors['eMail']="Invalid eMail address."
        if len(postData['txtPWord'])<8 and len(postData['txtPWord'])>25:
            errors['pwLen']="Password should be atleast 8 and not more than 25 characters."
        if postData['txtPWord'] != postData['txtConWord']:
            errors['pwMatch']="Passwords did not match."
        return errors

class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=255)
    password=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=RegistrationManager()