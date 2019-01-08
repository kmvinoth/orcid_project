from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from .models import OrcidTable

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
                       'code': auth_code, 'redirect_uri': 'https://science-it.charite.de/orcid/public_api/redirect'}

            headers = {'Accept': 'application/json'}

            try:

            	response = requests.post(API_ENDPOINT, data=payload, headers=headers, timeout=5)
            
            	status_code = response.status_code
            
            	print("STATUS CODE = ", status_code)

            	if response.status_code != 200:
                	print("Error posting data to ORCiD sandbox")

                	print("Message = ", response.text)

                	print("Status code for post data = ", response.status_code)

            	if response.status_code == 200:

                	print("Status code for the response from post data = ", response.status_code)

                	# data is of type dict
                	data = response.json()

                	
                	orcid_inst = OrcidTable(access_token=data['access_token'],
                                        	token_type=data['token_type'],
                                        	refresh_token=data['refresh_token'],
                                        	expires_in=data['expires_in'],
                                        	scope=data['scope'],
                                        	full_name=data['name'],
                                        	orcid=data['orcid'])
                	orcid_inst.save()
                	sandbox_url = "https://sandbox.orcid.org/" + data["orcid"]
                
                	return render(request, 'public_api/redirect.html', {'authorization_code': auth_code,
                                                                    'fullname': data['name'],
                                                                    "orcid": data['orcid'],
                                                                    "sandbox_url": sandbox_url})
            except Exception as e:
            	print(e)
            	print("Error send post data")
            
    if 'error' in request.GET:

        err = request.GET['error']
        # print("Error = ", err)
        return render(request, 'public_api/user_denied_access.html')

    else:
        return render(request, 'public_api/redirect.html', {'errors': errors})
