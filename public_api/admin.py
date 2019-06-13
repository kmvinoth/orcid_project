from django.contrib import admin
from .models import OrcidInvitation, Employees
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from orcid_project import settings
from decouple import config

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['uid', 'gender', 'first_name', 'last_name', 'complete_name', 'mail', 'role', 'parent_inst']
    list_filter = (('parent_inst'),)
    search_fields = ['first_name', 'last_name', 'complete_name', 'mail', 'parent_inst']


class OrcidInvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee_uid', 'token', 'link_validated', 'email_sent', 'click_create_orcid',
                    'click_link_orcid', 'click_not_interested_orcid', 'have_orcid', 'message']
    list_filter = (('link_validated', admin.BooleanFieldListFilter), ('email_sent', admin.BooleanFieldListFilter),
                   ('click_create_orcid', admin.BooleanFieldListFilter), ('click_link_orcid', admin.BooleanFieldListFilter))
    search_fields = ['employee_uid__first_name', 'employee_uid__last_name', 'employee_uid__parent_inst']
    actions = ['send_email']

    def send_email(self, request, queryset):
        for user in queryset:
            # print(user.employee_uid.first_name)
            # print(user.link)
            first_name = user.employee_uid.first_name
            # from_email = config('CHARITE_USER')
            subject = "Reg: Invitation to Create or Link Orcid to Charite"
            # message = "Hi ," + first_name + ", You have been invited by Charite to Create or link your Orcid. Click on the link to proceed further " + user.link
            sender = "vinothkumar.mohanakrishnan@charite.de"
            receiver = [user.employee_uid.mail]

            try:
                file_path = settings.BASE_DIR + "/public_api/templates/public_api/email_message.txt"
                print("FILE PATH = ", file_path)
                with open(file_path) as f:
                    email_message = f.read()
                    message = EmailMultiAlternatives(subject=subject, body=email_message, from_email=sender, to=receiver)
                    html_template = get_template("public_api/email_message_template.html").render()
                    message.attach_alternative(html_template, "text/html")
                    message.send()
                    # send_mail(subject, message, sender, receiver, fail_silently=False)
                    invitation_inst = OrcidInvitation.objects.get(employee_uid=user.employee_uid.uid)
                    # print("INVITAION_INST = ", invitation_inst)
                    invitation_inst.email_sent = 1
                    # print("EMAIL SENT = ", invitation_inst.email_sent)
                    invitation_inst.save()
            except Exception as e:
                print(e)

admin.site.register(OrcidInvitation, OrcidInvitationAdmin)
admin.site.register(Employees, EmployeesAdmin)

# ['Institut für Physiologie'], ['GB IT - Abteilung Forschung & Lehre']