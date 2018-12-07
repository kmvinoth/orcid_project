from django.shortcuts import render


# Create your views here.
def home(request):
    """
    home view render's the default Homepage template
    """
    return render(request, 'public_api/home.html')


# Create your views here.
def uri_redirect(request):
    """
    Redirect uri view
    """
    errors = []
    if 'code' in request.GET:
        auth_code = request.GET['code']
        if not auth_code:
            errors.append("Authorization code not present in request.GET dictionary")
        elif len(auth_code) > 6 or len(auth_code) < 6:
            errors.append("Length of the Authorization code is either greater than or less than 6")
        else:
            print("Authorization code = ", auth_code)
            return render(request, 'public_api/redirect.html', {'authorization_code': auth_code})
    else:
        return render(request, 'public_api/redirect.html', {'errors': errors})
