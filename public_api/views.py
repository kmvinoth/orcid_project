from django.shortcuts import render, HttpResponse, redirect, reverse, Http404
import requests
from decouple import config
from .models import Employees, OrcidTable, OrcidInvitation
from .forms import OrcidInvitationForm


def home(request):
    """
    home view render's the default Homepage template
    """
    return render(request, 'public_api/home.html')


def contact(request):
    """
    contact view render's the contact page template
    """
    return render(request, 'public_api/contact.html')


def faq_english(request):
    """
    faq_english view render's the faq_en page template
    """
    return render(request, 'public_api/faq_en.html')


def faq_german(request):
    """
    faq_german view render's the faq_de page template
    """
    return render(request, 'public_api/faq_de.html')


def invitation_link_view(request, token):
    """
    This view shows the personalized user page

    :param request

    :param token

    token(kwarg) is a random alphanumeric token with 32 characters long

    link_validated = 0 (user haven't clicked on the invitation link)

    link_validated = 1 (user clicked on the invitation link)
    """
    if len(token) < 32 or len(token) > 32:

        return HttpResponse("Invalid token")

    else:

        # token length == 32 characters

        try:
            orcid_invitation_inst = OrcidInvitation.objects.get(token=token)

            user_uid = orcid_invitation_inst.employee_uid.uid

            user_gender = orcid_invitation_inst.employee_uid.gender

            if user_gender == 'Herr':
                user_gender = 'Mr.'
            else:
                user_gender = 'Ms.'

            user_first_name = orcid_invitation_inst.employee_uid.first_name

            user_last_name = orcid_invitation_inst.employee_uid.last_name

            user_email = orcid_invitation_inst.employee_uid.mail

            base_url = "https://sandbox.orcid.org/oauth/authorize?client_id=APP-U7461O0AG8D66UBJ&response_type=code&scope=/authenticate&redirect_uri=http://localhost:9000/public_api/redirect"

            family_name_url = "&family_names="+user_last_name

            first_name_url = "&given_names="+user_first_name

            email_url = "&email="+user_email

            login_url_false = "&show_login=false"

            login_url_true = "&show_login=true"

            personalized_orcid_url_without_login = base_url+family_name_url+first_name_url+email_url+login_url_false

            # replace spaces in the string by %20 for url encoding
            personalized_orcid_url_without_login = personalized_orcid_url_without_login.replace(" ", "%20")

            orcid_url_with_login = base_url + login_url_true

            orcid_not_interested_form = OrcidInvitationForm()

            orcid_invitation_inst.link_validated = 1

            orcid_invitation_inst.save()

            context = {'first_name': user_first_name, 'last_name': user_last_name, 'email': user_email,
                       'gender': user_gender,
                       'orcid_url_without_login': personalized_orcid_url_without_login,
                       'orcid_url_with_login': orcid_url_with_login, 'form': orcid_not_interested_form,
                       'form_hidden': True
                       }

            if request.GET.get('next') == personalized_orcid_url_without_login:
                print("Clicked Create ORCID")
                orcid_invitation_inst.click_create_orcid = 1

                orcid_invitation_inst.save()

                create_orcid = personalized_orcid_url_without_login

                create_orcid_response = redirect(create_orcid)

                return create_orcid_response

            if request.GET.get('next') == orcid_url_with_login:
                print("Clicked Link ORCID")
                orcid_invitation_inst.click_link_orcid = 1

                orcid_invitation_inst.save()

                link_orcid = orcid_url_with_login

                link_orcid_response = redirect(link_orcid)

                return link_orcid_response

            if request.GET.get('next') == 'not_interested':
                print("Clicked Link Not Interested")
                context['form_hidden'] = False
                context['message'] = False
                orcid_invitation_inst.click_not_interested_orcid = 1
                orcid_invitation_inst.save()

                if request.method == 'POST':

                    orcid_not_interested_form = OrcidInvitationForm(request.POST)

                    if orcid_not_interested_form.is_valid():
                        data = orcid_not_interested_form.cleaned_data
                        orcid_invitation_inst.researcher = data['researcher']
                        orcid_invitation_inst.have_orcid = data['have_orcid']
                        orcid_invitation_inst.message = data['message']
                        orcid_invitation_inst.save()
                        print("DATA = ", data)
                        context['form_hidden'] = True
                        context['message'] = True
                        return render(request, 'public_api/personalized_user_page.html', context)
                    else:
                        print("FORM INVALID")
                        print("DATA = ", orcid_not_interested_form.data)
                        print(orcid_not_interested_form.errors)
                        return render(request, 'public_api/personalized_user_page.html',
                                      {'errors': orcid_not_interested_form.errors})

            return render(request, 'public_api/personalized_user_page.html', context)

        except Exception as e:
            print(e)
            return HttpResponse("Token not in the database")


def reject_orcid_creation_and_linking(request):

    return redirect("https://support.orcid.org/hc/en-us/articles/360006973893-Trusted-organizations")

    # return render(request, 'public_api/user_denied_access.html')


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

            payload = {'client_id': config('CLIENT_ID'),
                       'client_secret': config('CLIENT_SECRET'),
                       'grant_type': 'authorization_code',
                       'code': auth_code, 'redirect_uri': 'http://localhost:9000/public_api/redirect'}

            headers = {'Accept': 'application/json'}

            try:

                response = requests.post(API_ENDPOINT, data=payload, headers=headers)

                status_code = response.status_code

                print("STATUS CODE = ", status_code)

                if response.status_code != 200:
                    print("Error posting data to ORCiD sandbox")

                    print("Message = ", response.text)

                    print("Status code for post data = ", response.status_code)

                if response.status_code == 200:

                    print("Status code for post data = ", response.status_code)

                    # data is of type dict
                    data = response.json()

                    # print("TYPE INFO = ", type(data))
                    #
                    # print("Response data = ", response.json())

                    # data_keys = list(data.keys())

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
                print("ERROR")
    if 'error' in request.GET:

        err = request.GET['error']
        # print("Error = ", err)
        return render(request, 'public_api/user_denied_access.html')

    else:
        return render(request, 'public_api/redirect.html', {'errors': errors})


def member_api_invitation_link_view(request, token):
    """
    This view shows the personalized user page

    :param request

    :param token

    token(kwarg) is a random alphanumeric token with 32 characters long

    link_validated = 0 (user haven't clicked on the invitation link)

    link_validated = 1 (user clicked on the invitation link)
    """
    if len(token) < 32 or len(token) > 32:

        raise Http404("Token length has to be exactly 32 Characters long")

    else:

        # token length == 32 characters

        try:
            orcid_invitation_inst = OrcidInvitation.objects.get(token=token)

            user_uid = orcid_invitation_inst.employee_uid.uid

            user_gender = orcid_invitation_inst.employee_uid.gender

            if user_gender == 'Herr':
                user_gender = 'Mr.'
            else:
                user_gender = 'Ms.'

            user_first_name = orcid_invitation_inst.employee_uid.first_name

            user_last_name = orcid_invitation_inst.employee_uid.last_name

            user_email = orcid_invitation_inst.employee_uid.mail

            base_url = "https://sandbox.orcid.org/oauth/authorize?client_id=APP-8DI6P3MTH4TUOAQI&response_type=code&scope=/read-limited%20/activities/update%20/person/update&redirect_uri="+config('REDIRECT_URI')

            family_name_url = "&family_names="+user_last_name

            first_name_url = "&given_names="+user_first_name

            email_url = "&email="+user_email

            login_url_false = "&show_login=false"

            login_url_true = "&show_login=true"

            personalized_orcid_url_without_login = base_url+family_name_url+first_name_url+email_url+login_url_false

            # replace spaces in the string by %20 for url encoding
            personalized_orcid_url_without_login = personalized_orcid_url_without_login.replace(" ", "%20")

            orcid_url_with_login = base_url + login_url_true

            orcid_not_interested_form = OrcidInvitationForm()

            orcid_invitation_inst.link_validated = 1

            orcid_invitation_inst.save()

            context = {'first_name': user_first_name, 'last_name': user_last_name, 'email': user_email,
                       'gender': user_gender,
                       'orcid_url_without_login': personalized_orcid_url_without_login,
                       'orcid_url_with_login': orcid_url_with_login, 'form': orcid_not_interested_form,
                       'form_hidden': True
                       }

            if request.GET.get('next') == personalized_orcid_url_without_login:
                print("Clicked Create ORCID")
                orcid_invitation_inst.click_create_orcid = 1

                orcid_invitation_inst.save()

                create_orcid = personalized_orcid_url_without_login

                create_orcid_response = redirect(create_orcid)

                return create_orcid_response

            if request.GET.get('next') == orcid_url_with_login:
                print("Clicked Link ORCID")
                orcid_invitation_inst.click_link_orcid = 1

                orcid_invitation_inst.save()

                link_orcid = orcid_url_with_login

                link_orcid_response = redirect(link_orcid)

                return link_orcid_response

            if request.GET.get('next') == 'not_interested':
                print("Clicked Link Not Interested")
                context['form_hidden'] = False
                context['message'] = False
                orcid_invitation_inst.click_not_interested_orcid = 1
                orcid_invitation_inst.save()

                if request.method == 'POST':

                    orcid_not_interested_form = OrcidInvitationForm(request.POST)

                    if orcid_not_interested_form.is_valid():
                        data = orcid_not_interested_form.cleaned_data
                        orcid_invitation_inst.researcher = data['researcher']
                        orcid_invitation_inst.have_orcid = data['have_orcid']
                        orcid_invitation_inst.message = data['message']
                        orcid_invitation_inst.save()
                        print("DATA = ", data)
                        context['form_hidden'] = True
                        context['message'] = True
                        return render(request, 'public_api/member_api_invitation.html', context)
                    else:
                        print("FORM INVALID")
                        print("DATA = ", orcid_not_interested_form.data)
                        print(orcid_not_interested_form.errors)
                        return render(request, 'public_api/member_api_invitation.html',
                                      {'errors': orcid_not_interested_form.errors})

            return render(request, 'public_api/member_api_invitation.html', context)

        except Exception as e:
            print(e)
            error = e
            return render(request, 'public_api/member_api_invitation.html', {'error': error})


def member_api_success(request):
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

            payload = {'client_id': config('MEMBER_CLIENT_ID'),
                       'client_secret': config('MEMBER_CLIENT_SECRET'),
                       'grant_type': 'authorization_code',
                       'code': auth_code, 'redirect_uri': config('REDIRECT_URI')}

            headers = {'Accept': 'application/json'}

            try:

                response = requests.post(API_ENDPOINT, data=payload, headers=headers)

                status_code = response.status_code

                print("STATUS CODE = ", status_code)

                if response.status_code != 200:
                    print("Error posting data to ORCiD sandbox")

                    print("Message = ", response.text)

                    print("Status code for post data = ", response.status_code)

                if response.status_code == 200:

                    print("Status code for post data = ", response.status_code)

                    # data is of type dict
                    data = response.json()

                    # print("TYPE INFO = ", type(data))
                    #
                    # print("Response data = ", response.json())

                    # data_keys = list(data.keys())

                    orcid_inst = OrcidTable(access_token=data['access_token'],
                                            token_type=data['token_type'],
                                            refresh_token=data['refresh_token'],
                                            expires_in=data['expires_in'],
                                            scope=data['scope'],
                                            full_name=data['name'],
                                            orcid=data['orcid'])
                    orcid_inst.save()
                    sandbox_url = "https://sandbox.orcid.org/" + data["orcid"]
                    return render(request, 'public_api/member_api_redirect.html', {'authorization_code': auth_code,
                                                                                   'fullname': data['name'],
                                                                                   "orcid": data['orcid'],
                                                                                   "sandbox_url": sandbox_url})
            except Exception as e:
                print(e)
                print("ERROR")
    if 'error' in request.GET:

        err = request.GET['error']
        # print("Error = ", err)
        return render(request, 'public_api/user_denied_access.html')

    else:
        return render(request, 'public_api/member_api_redirect.html', {'errors': errors})



