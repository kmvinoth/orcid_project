from django.db import models

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


class OrcidTable(models.Model):
    access_token = models.CharField(max_length=100)
    token_type = models.CharField(max_length=15)
    refresh_token = models.CharField(max_length=100)
    expires_in = models.CharField(max_length=15)
    scope = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    orcid = models.CharField(max_length=50)

    def __str__(self):
        return "{} - {}".format(self.access_token, self.token_type, self.refresh_token,
                                self.expires_in, self.scope, self.full_name, self.orcid)

    class Meta:
        db_table = 'orcid_table'
        verbose_name_plural = 'orcid_table'