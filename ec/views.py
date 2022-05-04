import json
import logging

import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
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
        form = RegisterForm(request.POST)
        services.create_item(form.title, int(form.price))
        return redirect('ec:index')


@login_required
@transaction.atomic
def register_favorite(request):
    """
    お気に入り登録.

    POST された ID 要素を ログインユーザーと紐付け、お気に入り登録済みとする。
    :param request:
    :return: 検索結果ページへのリダイレクト
    """
    if request.POST.get('id') is None:
        return redirect('ec:index')
    item_ids = convert_id_to_list(request.POST.get('id'))
    services.create_favorite_relation(request.user.id, item_ids)
    return redirect('ec:index')


@login_required
@transaction.atomic
def unregister_favorite(request):
    """
    お気に入り削除.

    POST された ID 要素を ログインユーザーと紐付け、お気に入り登録を外す。
    :param request:
    :return: 検索結果ページへのリダイレクト
    """
    if request.POST.get('id') is None:
        return redirect('ec:index')
    item_ids = convert_id_to_list(request.POST.get('id'))
    services.remove_favorite_relation(request.user.id, item_ids)
    return redirect('ec:index')


def convert_id_to_list(ids):
    if type(ids) is str:
        item_ids = [int(ids)]
    else:
        item_ids = [int(item_id) for item_id in ids]
    return item_ids
