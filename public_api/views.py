from django.shortcuts import render


# Create your views here.
def home(request):
    """
    home view render's the default Homepage template
    """
    return render(request, 'public_api/home.html')
