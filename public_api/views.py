from django.shortcuts import render
import requests
import json


def home(request):
    """
    home view render's the default Homepage template
    """
    return render(request, 'public_api/home.html')


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
            # Exchange the authorization code with ORCID API

            API_ENDPOINT = "https://sandbox.orcid.org/oauth/token"

            payload = {'client_id': 'APP-3KOPX9UB987ZI77S',
                       'client_secret': 'cb2f45f9-2776-4971-9818-9a63d4ef02e0',
                       'grant_type': 'authorization_code',
                       'code': auth_code, 'redirect_uri': 'http://localhost/public_api/redirect'}

            headers = {'Accept': 'application/json'}

            r = requests.post(API_ENDPOINT, data=payload, headers=headers)

            print("Status code for post data = ", r.status_code)

            return render(request, 'public_api/redirect.html', {'authorization_code': auth_code})
    else:
        return render(request, 'public_api/redirect.html', {'errors': errors})
