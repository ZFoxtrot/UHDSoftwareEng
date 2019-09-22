from django.shortcuts import render


def home(request):
    return render(request, 'HomePage/home.html')  # displays HTML file in templates/HomePage/home.html
