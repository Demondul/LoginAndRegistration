from django.shortcuts import render,redirect,HttpResponse
from . models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
    return render(request,'loginRegApp/index.html')

def success(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=request.session['ID'])
        }
        return render(request,'loginRegApp/success.html',context)
    else:
        return redirect('/')

def register(request):
    if request.method=='POST':
        errors=Users.objects.registration_validator(request.POST)
        if len(Users.objects.filter(email_address=request.POST['txtEmail']))>0:
            errors['dupEmail']="duplicate email detected."
        
        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)
                print(key)
            return redirect('/')
        else:
            password=request.POST['txtPWord']
            pwHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            print(pwHash)
            Users.objects.create(first_name=request.POST['txtFirst'],last_name=request.POST['txtLast'],email_address=request.POST['txtEmail'],password=pwHash)

            user=Users.objects.get(email_address=request.POST['txtEmail'])
            request.session['ID']=user.id

    return redirect('/success')

def login(request):
    users=Users.objects.filter(email_address=request.POST['txtUMail'])

    if len(users)>0:
        for user in users:
            if bcrypt.checkpw(request.POST['txtUPWord'].encode(),user.password.encode()):
                request.session['ID']=user.id
                return redirect('/success')

    errors={
        'loginErr':"eMail and password did not match."
    }

    for key,value in errors.items():
        messages.error(request,value)
        print(key)

    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')