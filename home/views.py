from django.shortcuts import render

# Create your views here.
def about_us(request):
    
    return render(request, "about_us.html")

def contact_us(request):
    return render(request, "contact_us.html")

def home(request):
    return render(request,'index.html')