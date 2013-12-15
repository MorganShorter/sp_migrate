# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class A:(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    aio_number = models.IntegerField(null=True, db_column='AIO Number', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    company_name = models.CharField(max_length=100, db_column='Company Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    type = models.CharField(max_length=30, db_column='Type', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    contact_first_name = models.CharField(max_length=40, db_column='Contact First Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_last_name = models.CharField(max_length=40, db_column='Contact Last Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_2_first_name = models.CharField(max_length=40, db_column='Contact 2 First Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_2_last_name = models.CharField(max_length=40, db_column='Contact 2 Last Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    suburb = models.CharField(max_length=100, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.CharField(max_length=8, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=100, db_column='State', blank=True) # Field name made lowercase.
    att = models.CharField(max_length=100, db_column='Att', blank=True) # Field name made lowercase.
    del_address_1 = models.CharField(max_length=100, db_column='Del Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_address_2 = models.CharField(max_length=100, db_column='Del Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_suburb = models.CharField(max_length=100, db_column='Del Suburb', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_post_code = models.CharField(max_length=100, db_column='Del Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_state = models.CharField(max_length=8, db_column='Del State', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_order = models.DateTimeField(null=True, db_column='Last Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    next_contact = models.DateTimeField(null=True, db_column='Next Contact', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_o/no = models.FloatField(null=True, db_column='Last O/No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_order_value = models.FloatField(null=True, db_column='Last Order Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'a:'

class Class(models.Model):
    class_field = models.CharField(max_length=100, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    class Meta:
        db_table = u'Class'

class ConversionErrors(models.Model):
    object_type = models.CharField(max_length=510, db_column='Object Type', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    object_name = models.CharField(max_length=510, db_column='Object Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    error_description = models.TextField(db_column='Error Description', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Conversion Errors'

class Maildesc(models.Model):
    description = models.CharField(max_length=100, db_column='Description', blank=True) # Field name made lowercase.
    numb = models.IntegerField(db_column='Numb') # Field name made lowercase.
    class Meta:
        db_table = u'MailDesc'

class Mailhistory(models.Model):
    counter = models.IntegerField(null=True, db_column='Counter', blank=True) # Field name made lowercase.
    desc_code = models.IntegerField(null=True, db_column='Desc Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'MailHistory'

class Mailtable(models.Model):
    counter = models.IntegerField(null=True, db_column='Counter', blank=True) # Field name made lowercase.
    customer = models.CharField(max_length=510, db_column='Customer', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=510, db_column='State', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.IntegerField(null=True, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    national_presort = models.CharField(max_length=510, db_column='National PreSort', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class_field = models.CharField(max_length=510, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    class Meta:
        db_table = u'MailTable'

class Mergedmail(models.Model):
    company = models.CharField(max_length=510, db_column='Company', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=510, db_column='Name', blank=True) # Field name made lowercase.
    address1 = models.CharField(max_length=200, db_column='Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=200, db_column='Address2', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=200, db_column='Suburb', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=100, db_column='State', blank=True) # Field name made lowercase.
    postcode = models.CharField(max_length=8, db_column='PostCode', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=30, db_column='Type', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    numb = models.FloatField(null=True, db_column='Numb', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'MergedMail'

class Newnumbers(models.Model):
    company_id = models.IntegerField(null=True, db_column='company id', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    aio_no = models.IntegerField(null=True, db_column='aio no', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    name = models.CharField(max_length=510, blank=True)
    phone = models.CharField(max_length=510, blank=True)
    new_numb = models.CharField(max_length=510, db_column='NEW NUMB', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'NewNumbers'

class Noorders(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    aio_number = models.IntegerField(null=True, db_column='AIO Number', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    company_name = models.CharField(max_length=100, db_column='Company Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    type = models.CharField(max_length=30, db_column='Type', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    contact_first_name = models.CharField(max_length=40, db_column='Contact First Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_last_name = models.CharField(max_length=40, db_column='Contact Last Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_2_first_name = models.CharField(max_length=40, db_column='Contact 2 First Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    contact_2_last_name = models.CharField(max_length=40, db_column='Contact 2 Last Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    suburb = models.CharField(max_length=100, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.CharField(max_length=8, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=100, db_column='State', blank=True) # Field name made lowercase.
    att = models.CharField(max_length=100, db_column='Att', blank=True) # Field name made lowercase.
    del_address_1 = models.CharField(max_length=100, db_column='Del Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_address_2 = models.CharField(max_length=100, db_column='Del Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_suburb = models.CharField(max_length=100, db_column='Del Suburb', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_post_code = models.CharField(max_length=100, db_column='Del Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_state = models.CharField(max_length=8, db_column='Del State', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_order = models.DateTimeField(null=True, db_column='Last Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    next_contact = models.DateTimeField(null=True, db_column='Next Contact', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_o/no = models.FloatField(null=True, db_column='Last O/No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_order_value = models.FloatField(null=True, db_column='Last Order Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'NoOrders'

class Notes(models.Model):
    notesid = models.IntegerField(null=True, db_column='NotesID', blank=True) # Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    note = models.CharField(max_length=510, db_column='Note', blank=True) # Field name made lowercase.
    next_contact = models.DateTimeField(null=True, db_column='Next Contact', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    done = models.CharField(max_length=4, db_column='Done', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Notes'

class Table1(models.Model):
    counter = models.IntegerField(db_column='Counter') # Field name made lowercase.
    customer = models.CharField(max_length=510, db_column='Customer', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=510, db_column='State', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.IntegerField(null=True, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    national_presort = models.CharField(max_length=510, db_column='National PreSort', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    anzsic = models.CharField(max_length=100, db_column='ANZSIC', blank=True) # Field name made lowercase.
    class_field = models.CharField(max_length=510, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    entry_type = models.CharField(max_length=100, db_column='Entry Type', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    add = models.CharField(max_length=100, db_column='Add', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=100, db_column='Tel', blank=True) # Field name made lowercase.
    nam = models.CharField(max_length=100, db_column='Nam', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Table1'

class Table1Backup(models.Model):
    counter = models.IntegerField(db_column='Counter') # Field name made lowercase.
    customer = models.CharField(max_length=510, db_column='Customer', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=510, db_column='State', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.IntegerField(null=True, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    national_presort = models.CharField(max_length=510, db_column='National PreSort', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    anzsic = models.CharField(max_length=100, db_column='ANZSIC', blank=True) # Field name made lowercase.
    class_field = models.CharField(max_length=510, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    entry_type = models.CharField(max_length=100, db_column='Entry Type', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    add = models.CharField(max_length=100, db_column='Add', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=100, db_column='Tel', blank=True) # Field name made lowercase.
    nam = models.CharField(max_length=100, db_column='Nam', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Table1Backup'

class Table1Copy(models.Model):
    counter = models.IntegerField(db_column='Counter') # Field name made lowercase.
    customer = models.CharField(max_length=510, db_column='Customer', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    state = models.CharField(max_length=510, db_column='State', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='Suburb', blank=True) # Field name made lowercase.
    post_code = models.IntegerField(null=True, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    national_presort = models.CharField(max_length=510, db_column='National PreSort', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    anzsic = models.CharField(max_length=100, db_column='ANZSIC', blank=True) # Field name made lowercase.
    class_field = models.CharField(max_length=510, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    entry_type = models.CharField(max_length=100, db_column='Entry Type', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    add = models.CharField(max_length=100, db_column='Add', blank=True) # Field name made lowercase.
    tel = models.CharField(max_length=100, db_column='Tel', blank=True) # Field name made lowercase.
    nam = models.CharField(max_length=100, db_column='Nam', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Table1Copy'

class Vet2(models.Model):
    customer = models.CharField(max_length=510, db_column='Customer', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=100, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=100, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='Suburb', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=510, db_column='State', blank=True) # Field name made lowercase.
    post_code = models.IntegerField(null=True, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class_field = models.CharField(max_length=510, db_column='Class', blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    class Meta:
        db_table = u'vet2'

