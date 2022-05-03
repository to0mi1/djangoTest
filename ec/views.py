import json
import logging

import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from ec import services
from ec.forms import SearchForm, RegisterForm

logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return redirect('ec:index')
        return render(request, 'ec/login.html')
    else:
        return render(request, 'ec/login.html')


def logout(request):
    logout(request)
    return redirect('ec:login')


@login_required
def item_landing(request):
    if request.method == 'POST':
        logger.debug(request.POST)
        request.session['item_name'] = request.POST.get('item_name')
        return redirect('ec:index')
    else:
        if request.session.get('item_name'):
            form = SearchForm(initial={'item_name': request.session['item_name']})
        else:
            form = SearchForm()
        items = services.find_item(request.user.id, request.session.get('item_name'))
        registerForm = RegisterForm()
        return render(request, 'ec/index.html',
                      {'form': form, 'registerForm': registerForm, 'items': json.dumps(items)})


@login_required
def register(request):
    if request.method == 'POST':
        services.create_item(request.POST.get('title'), int(request.POST.get('price')))
        return redirect('ec:index')
