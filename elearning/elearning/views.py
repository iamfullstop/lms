from django.shortcuts import render


def index(request):
    
    return render(request, 'index.html')  # render the index.html template with the categories list
