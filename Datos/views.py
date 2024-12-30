from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def ver_datos(request):
    return render(request, 'ver_mas.html')