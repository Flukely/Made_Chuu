from django.shortcuts import render

def index(request):
    # การเรียกหน้า index.html
    return render(request, 'index.html')

