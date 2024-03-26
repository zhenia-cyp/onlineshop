from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Category


def index(request):

    categories = Category.objects.all()
    return render(request, 'main/index.html', {'categories': categories})


def about(request):

    return render(request, 'main/about.html', {'about': "we are a good company"})
