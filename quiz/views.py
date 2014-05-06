from django.shortcuts import render

def home(request):
    return render(request, 'quiz/quiz.html')
    
