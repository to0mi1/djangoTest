import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return redirect('index')
        return render(request, 'ec/login.html')
    else:
        return render(request, 'ec/login.html')


def logout(request):
    logout(request)
    return redirect('login')


@login_required
def item_landing(request):
    if request.method == 'GET':
        return render(request, 'ec/index.html')
    return HttpResponse(status=405)
