# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Catalog20012(models.Model):
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    page_no = models.CharField(max_length=100, db_column='Page No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    stock = models.IntegerField(null=True, db_column='Stock', blank=True) # Field name made lowercase.
    last_order_qty = models.IntegerField(null=True, db_column='Last Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_in_date = models.DateTimeField(null=True, db_column='Last In Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_to_order = models.IntegerField(null=True, db_column='Qty To Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Catalog 2001 - 2'

class ConversionErrors(models.Model):
    object_type = models.CharField(max_length=510, db_column='Object Type', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    object_name = models.CharField(max_length=510, db_column='Object Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    error_description = models.TextField(db_column='Error Description', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Conversion Errors'

class Localorders(models.Model):
    orderid = models.IntegerField(null=True, db_column='OrderId', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'LocalOrders'

class PasteErrors(models.Model):
    product_code = models.CharField(max_length=510, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    product_description = models.CharField(max_length=510, db_column='Product description', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    size = models.CharField(max_length=510, db_column='Size', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=510, db_column='Type', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=510, db_column='Message', blank=True) # Field name made lowercase.
    cost_price_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Price Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_50_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'50 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_1 = models.CharField(max_length=510, db_column='Per 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_100_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'100 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_2 = models.CharField(max_length=510, db_column='Per 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_200_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'200 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_3 = models.CharField(max_length=510, db_column='Per 3', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_300_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'300 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_4 = models.CharField(max_length=510, db_column='Per 4', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_500_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'500 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_5 = models.CharField(max_length=510, db_column='Per 5', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_1000_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'1000 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_6 = models.CharField(max_length=510, db_column='Per 6', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_250_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'250 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_7 = models.CharField(max_length=510, db_column='Per 7', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_2000_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'2000 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_8 = models.CharField(max_length=510, db_column='Per 8', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_2500_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'2500 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_9 = models.CharField(max_length=510, db_column='Per 9', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    supplier = models.CharField(max_length=510, db_column='Supplier', blank=True) # Field name made lowercase.
    pricelevel = models.CharField(max_length=510, db_column='PriceLevel', blank=True) # Field name made lowercase.
    royaltyfactor = models.FloatField(null=True, db_column='RoyaltyFactor', blank=True) # Field name made lowercase.
    new_cost = models.CharField(max_length=510, db_column='New Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    orderyn = models.IntegerField(null=True, db_column='OrderYN', blank=True) # Field name made lowercase.
    note = models.CharField(max_length=510, db_column='Note', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Paste Errors'

class Table1(models.Model):
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    pageno = models.CharField(max_length=100, db_column='PageNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Table1'

class Table2(models.Model):
    page_no = models.CharField(max_length=100, db_column='Page No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    pageno = models.CharField(max_length=100, db_column='PageNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Table2'

class CatalogBackup2001(models.Model):
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    page_no = models.CharField(max_length=100, db_column='Page No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    stock = models.IntegerField(null=True, db_column='Stock', blank=True) # Field name made lowercase.
    last_order_qty = models.IntegerField(null=True, db_column='Last Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_in_date = models.DateTimeField(null=True, db_column='Last In Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_to_order = models.IntegerField(null=True, db_column='Qty To Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Catalog Backup 2001'

class Bbb(models.Model):
    state = models.CharField(max_length=100, db_column='STATE', blank=True) # Field name made lowercase.
    numb = models.IntegerField(null=True, db_column='NUMB', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'bbb'

class Borders(models.Model):
    fakeid = models.IntegerField(db_column='FakeID') # Field name made lowercase.
    product_code = models.CharField(max_length=16, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    custid = models.IntegerField(null=True, db_column='CustID', blank=True) # Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_out = models.FloatField(null=True, db_column='Qty Out', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_stock = models.FloatField(null=True, db_column='From Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_surplus = models.FloatField(null=True, db_column='From Surplus', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_qty = models.FloatField(null=True, db_column='Back Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_id = models.IntegerField(null=True, db_column='Back Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_bo = models.FloatField(null=True, db_column='Qty B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date_bo = models.DateTimeField(null=True, db_column='Date B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    expected_bo = models.DateTimeField(null=True, db_column='Expected B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    printer_id = models.CharField(max_length=12, db_column='Printer Id', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    price_each = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Price Each', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Price', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_p = models.FloatField(null=True, db_column='Disc %%', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_d = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Disc $', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    net_value = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Net Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_in = models.FloatField(null=True, db_column='Qty In', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivered = models.DateTimeField(null=True, db_column='Delivered', blank=True) # Field name made lowercase.
    cost_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    oldborder = models.FloatField(null=True, db_column='OldBorder', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Borders'
        app_label = 'borders'

class CardDetails(models.Model):
    product_code = models.CharField(max_length=24, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    product_description = models.CharField(max_length=100, db_column='Product description', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    size = models.CharField(max_length=100, db_column='Size', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    cost_price_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Price Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_50_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'50 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_1 = models.CharField(max_length=100, db_column='Per 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_100_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'100 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_2 = models.CharField(max_length=100, db_column='Per 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_200_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'200 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_3 = models.CharField(max_length=100, db_column='Per 3', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_300_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'300 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_4 = models.CharField(max_length=100, db_column='Per 4', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_500_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'500 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_5 = models.CharField(max_length=100, db_column='Per 5', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_1000_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'1000 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_6 = models.CharField(max_length=100, db_column='Per 6', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_250_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'250 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_7 = models.CharField(max_length=100, db_column='Per 7', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_2000_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'2000 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_8 = models.CharField(max_length=100, db_column='Per 8', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_2500_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'2500 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    per_9 = models.CharField(max_length=100, db_column='Per 9', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    supplier = models.CharField(max_length=16, db_column='Supplier', blank=True) # Field name made lowercase.
    pricelevel = models.CharField(max_length=20, db_column='PriceLevel', blank=True) # Field name made lowercase.
    royaltyfactor = models.FloatField(null=True, db_column='RoyaltyFactor', blank=True) # Field name made lowercase.
    new_cost = models.CharField(max_length=100, db_column='New Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    orderyn = models.IntegerField(null=True, db_column='OrderYN', blank=True) # Field name made lowercase.
    note = models.CharField(max_length=500, db_column='Note', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Card Details'

class DetailsHistory(models.Model):
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    product_code = models.CharField(max_length=16, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_out = models.FloatField(null=True, db_column='Qty Out', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_stock = models.FloatField(null=True, db_column='From Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_surplus = models.FloatField(null=True, db_column='From Surplus', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_qty = models.FloatField(null=True, db_column='Back Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_id = models.IntegerField(null=True, db_column='Back Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_bo = models.FloatField(null=True, db_column='Qty B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date_bo = models.DateTimeField(null=True, db_column='Date B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    expected_bo = models.DateTimeField(null=True, db_column='Expected B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    printer_id = models.CharField(max_length=12, db_column='Printer Id', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    price_each = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Price Each', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Price', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_p = models.FloatField(null=True, db_column='Disc %%', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_d = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Disc $', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    net_value = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Net Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_in = models.FloatField(null=True, db_column='Qty In', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivered = models.DateTimeField(null=True, db_column='Delivered', blank=True) # Field name made lowercase.
    cost_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    stock = models.IntegerField(null=True, blank=True)
    priceb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='PriceB', blank=True) # Field name made lowercase.
    totb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='TotB', blank=True) # Field name made lowercase.
    discb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='DiscB', blank=True) # Field name made lowercase.
    netb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='NetB', blank=True) # Field name made lowercase.
    royalty = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Royalty', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Details History'
        app_label = 'detailshistory'

class KorenCatalogue(models.Model):
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    page_no = models.CharField(max_length=100, db_column='Page No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    stock = models.IntegerField(null=True, db_column='Stock', blank=True) # Field name made lowercase.
    last_order_qty = models.IntegerField(null=True, db_column='Last Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_in_date = models.DateTimeField(null=True, db_column='Last In Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_to_order = models.IntegerField(null=True, db_column='Qty To Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Koren Catalogue'

class Mail(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=100, db_column='Suburb', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Mail'

class Maildump(models.Model):
    company_name = models.CharField(max_length=100, db_column='Company Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    type = models.CharField(max_length=30, db_column='Type', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=100, db_column='Telephone', blank=True) # Field name made lowercase.
    del_address_1 = models.CharField(max_length=100, db_column='Del Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_address_2 = models.CharField(max_length=100, db_column='Del Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_suburb = models.CharField(max_length=100, db_column='Del Suburb', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_post_code = models.CharField(max_length=100, db_column='Del Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    del_state = models.CharField(max_length=8, db_column='Del State', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'MailDump'

class OrderDetails(models.Model):
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    product_code = models.CharField(max_length=24, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    ordersupplier = models.CharField(max_length=100, db_column='OrderSupplier', blank=True) # Field name made lowercase.
    qty_out = models.FloatField(null=True, db_column='Qty Out', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_stock = models.FloatField(null=True, db_column='From Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_surplus = models.FloatField(null=True, db_column='From Surplus', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_qty = models.FloatField(null=True, db_column='Back Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_order_id = models.IntegerField(null=True, db_column='Back Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_bo = models.FloatField(null=True, db_column='Qty B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date_bo = models.DateTimeField(null=True, db_column='Date B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    expected_bo = models.DateTimeField(null=True, db_column='Expected B/O', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    printer_id = models.CharField(max_length=12, db_column='Printer Id', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    price_each = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Price Each', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Price', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_p = models.FloatField(null=True, db_column='Disc %%', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    disc_d = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Disc $', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    net_value = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Net Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_in = models.FloatField(null=True, db_column='Qty In', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivered = models.DateTimeField(null=True, db_column='Delivered', blank=True) # Field name made lowercase.
    cost_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    stock = models.IntegerField(null=True, blank=True)
    priceb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='PriceB', blank=True) # Field name made lowercase.
    totb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='TotB', blank=True) # Field name made lowercase.
    discb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='DiscB', blank=True) # Field name made lowercase.
    netb = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='NetB', blank=True) # Field name made lowercase.
    royalty = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Royalty', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Order Details'
        app_label = 'orderdetails'

class OrderHistory(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    deliver_date = models.DateTimeField(null=True, db_column='Deliver Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    despatch_date = models.DateTimeField(null=True, db_column='Despatch Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_due = models.DateTimeField(null=True, db_column='Invoice Due', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    shipper_id = models.CharField(max_length=100, db_column='Shipper ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivery_charge = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Delivery Charge', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_total = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Invoice Total', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    notes = models.CharField(max_length=510, db_column='Notes', blank=True) # Field name made lowercase.
    order_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Order Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_no = models.IntegerField(null=True, db_column='Inv No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qpi_margin = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='QPI Margin', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Order History'

class Orders(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    deliver_date = models.DateTimeField(null=True, db_column='Deliver Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    despatch_date = models.DateTimeField(null=True, db_column='Despatch Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_due = models.DateTimeField(null=True, db_column='Invoice Due', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    shipper_id = models.CharField(max_length=100, db_column='Shipper ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivery_charge = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Delivery Charge', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_total = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Invoice Total', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    notes = models.CharField(max_length=510, db_column='Notes', blank=True) # Field name made lowercase.
    order_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Order Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_no = models.IntegerField(null=True, db_column='Inv No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qpi_margin = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='QPI Margin', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Orders'

class Packages(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    suburb = models.CharField(max_length=100, db_column='Suburb', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Packages'

class Pageprod(models.Model):
    prodno = models.CharField(max_length=100, db_column='Prodno', blank=True) # Field name made lowercase.
    page_no = models.CharField(max_length=100, db_column='page no', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'PageProd'

class SourcePriceLevel(models.Model):
    pricelevel = models.CharField(max_length=100, db_column='PriceLevel', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PriceLevel'

class Printers(models.Model):
    printer_id = models.CharField(max_length=12, db_column='Printer ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    pname = models.CharField(max_length=100, db_column='Pname', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=100, db_column='Phone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=100, db_column='Fax', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Printers'

class Products(models.Model):
    product_code = models.CharField(max_length=510, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    product_description = models.CharField(max_length=510, db_column='Product description', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    size = models.CharField(max_length=100, db_column='Size', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=510, db_column='Type', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    cost_price_ea = models.CharField(max_length=100, db_column='Cost Price Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    number_50_price = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column=u'50 Price', blank=True) # Field renamed to remove spaces. Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    qty = models.IntegerField(null=True, db_column='Qty', blank=True) # Field name made lowercase.
    total = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total', blank=True) # Field name made lowercase.
    sold = models.CharField(max_length=510, db_column='Sold', blank=True) # Field name made lowercase.
    soldval = models.CharField(max_length=510, db_column='SoldVal', blank=True) # Field name made lowercase.
    avgprice = models.CharField(max_length=510, db_column='AvgPrice', blank=True) # Field name made lowercase.
    value = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Value', blank=True) # Field name made lowercase.
    totsold = models.CharField(max_length=510, db_column='TotSold', blank=True) # Field name made lowercase.
    supplier = models.CharField(max_length=510, db_column='Supplier', blank=True) # Field name made lowercase.
    inventory = models.IntegerField(null=True, db_column='Inventory', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PRODUCTS'

class Ro2(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    deliver_date = models.DateTimeField(null=True, db_column='Deliver Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    despatch_date = models.DateTimeField(null=True, db_column='Despatch Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_due = models.DateTimeField(null=True, db_column='Invoice Due', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    shipper_id = models.CharField(max_length=100, db_column='Shipper ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivery_charge = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Delivery Charge', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_total = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Invoice Total', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    notes = models.CharField(max_length=510, db_column='Notes', blank=True) # Field name made lowercase.
    order_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Order Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_no = models.IntegerField(null=True, db_column='Inv No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qpi_margin = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='QPI Margin', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'ro2'

class Shippers(models.Model):
    shipper_id = models.CharField(max_length=12, db_column='Shipper ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    name = models.CharField(max_length=100, db_column='Name', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=100, db_column='Phone', blank=True) # Field name made lowercase.
    our_id_code = models.CharField(max_length=100, db_column='Our ID Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Shippers'

class Smartorder(models.Model):
    product_code = models.CharField(max_length=16, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    from_stock = models.FloatField(null=True, db_column='From Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    cost_ea = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Cost Ea', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    total_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Total Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    reason = models.CharField(max_length=100, db_column='Reason', blank=True) # Field name made lowercase.
    dateout = models.DateTimeField(null=True, db_column='DateOut', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SmartOrder'

class SpCatalogue2000(models.Model):
    prodno = models.CharField(max_length=100, db_column='ProdNo', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    page_no = models.CharField(max_length=100, db_column='Page No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    message = models.CharField(max_length=100, db_column='Message', blank=True) # Field name made lowercase.
    stock = models.IntegerField(null=True, db_column='Stock', blank=True) # Field name made lowercase.
    last_order_qty = models.IntegerField(null=True, db_column='Last Order Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_in_date = models.DateTimeField(null=True, db_column='Last In Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty_to_order = models.IntegerField(null=True, db_column='Qty To Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'SP Catalogue 2000'

class StateNumbers(models.Model):
    state = models.CharField(max_length=100, db_column='State', blank=True) # Field name made lowercase.
    pcode = models.CharField(max_length=100, db_column='Pcode', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'State Numbers'

class Stock(models.Model):
    product_code = models.CharField(max_length=24, db_column='Product Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qty = models.FloatField(null=True, db_column='Qty', blank=True) # Field name made lowercase.
    minimum_stock = models.FloatField(null=True, db_column='Minimum Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    back_orders = models.FloatField(null=True, db_column='Back Orders', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    usa_order = models.FloatField(null=True, db_column='USA Order', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    on_order_for_clients = models.FloatField(null=True, db_column='On Order For Clients', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    surplus = models.FloatField(null=True, db_column='Surplus', blank=True) # Field name made lowercase.
    suggest = models.FloatField(null=True, db_column='Suggest', blank=True) # Field name made lowercase.
    last_in_qty = models.FloatField(null=True, db_column='Last In Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_in_date = models.DateTimeField(null=True, db_column='Last In Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Stock'

class StockAudit(models.Model):
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    open_stock = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Open Stock', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    new_qty = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='New Qty', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    stock_movement = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Stock Movement', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    prev = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Prev', blank=True) # Field name made lowercase.
    last_date = models.DateTimeField(null=True, db_column='Last Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Stock Audit'

class Suppliers(models.Model):
    supplier = models.CharField(max_length=100, db_column='Supplier', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Suppliers'

class Tbltemp(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    order_id = models.IntegerField(null=True, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date = models.DateTimeField(null=True, db_column='Date', blank=True) # Field name made lowercase.
    deliver_date = models.DateTimeField(null=True, db_column='Deliver Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    despatch_date = models.DateTimeField(null=True, db_column='Despatch Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_due = models.DateTimeField(null=True, db_column='Invoice Due', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    shipper_id = models.CharField(max_length=100, db_column='Shipper ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    delivery_charge = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Delivery Charge', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    invoice_total = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Invoice Total', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    notes = models.CharField(max_length=510, db_column='Notes', blank=True) # Field name made lowercase.
    order_cost = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Order Cost', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_no = models.IntegerField(null=True, db_column='Inv No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    qpi_margin = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='QPI Margin', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'tblTEMP'

class Type(models.Model):
    type = models.CharField(max_length=30, db_column='TYPE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Type'

class SourceCompany(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    aio_number = models.IntegerField(null=True, db_column='AIO Number', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    company_name = models.CharField(max_length=100, db_column='Company Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    email = models.CharField(max_length=100, db_column='Email', blank=True) # Field name made lowercase.
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
    last_ono = models.FloatField(null=True, db_column='Last O/No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    last_order_value = models.FloatField(null=True, db_column='Last Order Value', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    new_no = models.IntegerField(null=True, db_column='New No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    class Meta:
        db_table = u'Company'

class Invoices(models.Model):
    inv_no = models.IntegerField(null=True, db_column='Inv No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    company_id = models.CharField(max_length=100, db_column='Company ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    order_id = models.CharField(max_length=100, db_column='Order ID', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_date = models.DateTimeField(null=True, db_column='Inv Date', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    inv_amt = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Inv Amt', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    date_paid = models.DateTimeField(null=True, db_column='Date Paid', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    cheque_no = models.FloatField(null=True, db_column='Cheque No', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    payment_amount = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Payment Amount', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    balance = models.DecimalField(decimal_places=2, null=True, max_digits=15, db_column='Balance', blank=True) # Field name made lowercase.
    notes = models.CharField(max_length=100, db_column='Notes', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Invoices'

class Membadd(models.Model):
    company_id = models.IntegerField(null=True, db_column='Company Id', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    company_name = models.CharField(max_length=100, db_column='Company Name', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    type = models.CharField(max_length=100, db_column='Type', blank=True) # Field name made lowercase.
    family = models.CharField(max_length=510, db_column='FAMILY', blank=True) # Field name made lowercase.
    given = models.CharField(max_length=510, db_column='GIVEN', blank=True) # Field name made lowercase.
    prefix = models.CharField(max_length=510, db_column='PREFIX', blank=True) # Field name made lowercase.
    address_1 = models.CharField(max_length=510, db_column='Address 1', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    address_2 = models.CharField(max_length=510, db_column='Address 2', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    suburb = models.CharField(max_length=510, db_column='SUBURB', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=100, db_column='STATE', blank=True) # Field name made lowercase.
    post_code = models.CharField(max_length=510, db_column='Post Code', blank=True) # Field renamed to remove spaces. Field name made lowercase.
    membcode = models.CharField(max_length=510, db_column='MEMBCODE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'MEMBADD'

