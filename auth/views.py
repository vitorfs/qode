from django.shortcuts import render

def login(request):
    return render(request, 'auth/login.html')

def facebook(request):
    return render(request, 'auth/facebook.html')