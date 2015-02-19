from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def contact(request):
    return render(request, 'contact.html')