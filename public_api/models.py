from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.


class Employees(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    gender = models.CharField(max_length=45, blank=True, null=True)
    first_name = models.CharField(db_column='firstName', max_length=245, blank=True,
                                  null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='lastName', max_length=245, blank=True,
                                 null=True)  # Field name made lowercase.
    mail = models.CharField(max_length=245, blank=True, null=True)
    all_mail = models.TextField(db_column='allMail', blank=True, null=True)  # Field name made lowercase.
    complete_name = models.CharField(db_column='completeName', max_length=545, blank=True,
                                     null=True)  # Field name made lowercase.
    role = models.CharField(max_length=445, blank=True, null=True)
    raum = models.CharField(max_length=45, blank=True, null=True)
    telephone = models.CharField(max_length=45, blank=True, null=True)
    address_no = models.CharField(db_column='addressNo', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    haus = models.TextField(blank=True, null=True)
    info_intern = models.CharField(db_column='infoIntern', max_length=245, blank=True,
                                   null=True)  # Field name made lowercase.
    parent_id = models.CharField(db_column='parentID', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    parent_inst = models.TextField(db_column='parentInst', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return "{} - {}".format(self.uid, self.gender, self.first_name, self.last_name, self.mail, self.all_mail,
                                self.complete_name, self.role,
                                self.raum, self.telephone, self.address_no, self.haus, self.info_intern, self.parent_id,
                                self.parent_inst)

    class Meta:
        managed = False
        db_table = 'employees'
        verbose_name_plural = 'employees'
        ordering = ['pk']


class OrcidInvitation(models.Model):

    ORCID_CHOICES = (('yes', 'Yes'), ('no', 'No'))

    id = models.AutoField(primary_key=True)
    employee_uid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='employee_uid', blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    link_validated = models.IntegerField(default=0)
    email_sent = models.IntegerField(blank=True, null=True)
    click_create_orcid = models.IntegerField(blank=True, null=True)
    click_link_orcid = models.IntegerField(blank=True, null=True)
    click_not_interested_orcid = models.IntegerField(blank=True, null=True)
    have_orcid = MultiSelectField(choices=ORCID_CHOICES, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)
    researcher = MultiSelectField(choices=ORCID_CHOICES, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.employee_uid, self.token, self.link, self.link_validated, self.email_sent,
                                self.click_create_orcid, self.click_link_orcid, self.click_not_interested_orcid,
                                self.have_orcid, self.message)

    class Meta:
        managed = False
        db_table = 'orcid_invitation'
        ordering = ['pk']


class OrcidTable(models.Model):
    access_token = models.CharField(max_length=100)
    token_type = models.CharField(max_length=15)
    refresh_token = models.CharField(max_length=100)
    expires_in = models.CharField(max_length=15)
    scope = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    orcid = models.CharField(max_length=50)
    # invitation_id = models.ForeignKey(OrcidInvitation, models.DO_NOTHING, blank=True, null=True)
    # orcid_created = models.IntegerField(blank=True, null=True)
    # orcid_linked = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.access_token, self.token_type, self.refresh_token,
                                self.expires_in, self.scope, self.full_name, self.orcid)

    class Meta:
        managed = False
        db_table = 'orcid_table'
        verbose_name_plural = 'orcid_table'