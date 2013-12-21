# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
#import os

#from decimal import Decimal
#from datetime import datetime, date, timedelta
#from tinymce.models import HTMLField

# framework
#from django.db.models.manager import Manager
#from django.db.models import signals
#from django.contrib.gis.db import models
#from django.contrib.auth.models import User as BackendUser
#from django.contrib.auth.models import UserManager
#from django.contrib.sites.models import Site
#from django.contrib.sites.managers import CurrentSiteManager
#from django.contrib.humanize.templatetags.humanize import naturalday
#from django.core.exceptions import ObjectDoesNotExist
#from django.core.mail import send_mail
#from django.template.defaultfilters import slugify
#from django.conf import settings
#from django.utils.safestring import mark_safe

# project
#from ilc.dsite.utils import seo_make_msg
#from .utils import geocode, state_from_address, COUNTRY, slug_filename
#from .thumbnail import trim_image
#from .managers import CouponManager
#from .const import *
#from .signals import coupon_post_save, trader_post_save, suburb_post_save, \
#    backenduser_post_save, couponvote_post_delete, metadata_update


#try:
#    from south.modelsinspector import add_introspection_rules
#    add_introspection_rules([], ["^tinymce\.models.\HTMLField"])
#    add_introspection_rules([], ["^dynamicsites\.fields\.SubdomainListField"])
#    add_introspection_rules([], ["^dynamicsites\.fields\.FolderNameField"])
#except Exception, e:
#    pass
class ImportNote(models.Model):
    """ Import notes
    """
    model = models.CharField(max_length=50)
    model_id = models.PositiveIntegerField()
    type = models.CharField(max_length=50, default=None)
    text = models.TextField()
    src_model = models.CharField(max_length=50, null=True, blank=True)
    src_model_id_field = models.CharField(max_length=50, null=True, blank=True)
    src_model_id_text = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.type + ' Import Note for ' + self.model + '.id = ' + str(self.model_id)

class Customer(models.Model):
    """ Customer; makes an order from SmartPractice
    """
    registration = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    suburb = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='Australia')
    telephone = models.CharField(max_length=40)
    fax = models.CharField(max_length=40)
    email = models.EmailField(max_length=255)
    delivery_attn = models.CharField(max_length=255)
    delivery_address_line_1 = models.CharField(max_length=255)
    delivery_address_line_2 = models.CharField(max_length=255)
    delivery_suburb = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=100)
    delivery_postcode = models.CharField(max_length=10)
    delivery_country = models.CharField(max_length=100, default='Australia')
    from_src_company_id = models.IntegerField(null=True, blank=True)
    from_src_membadd_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class CustomerContact(models.Model):
    """ Contact for a Customer
    """
    customer = models.ForeignKey(Customer, related_name='contacts')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return ' '.join((self.first_name, self.surname)).strip()

class Size(models.Model):
    """ Product Size/Dimensions
    """
    width = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    units = models.CharField(max_length=80, null=True)
    notes = models.TextField(null=True)
    sub_notes = models.TextField(null=True)
    #notes = models.CharField(max_length=120, null=True)

    def __unicode__(self):
        if self.width and self.height and self.depth:
            return "W:%d H:%d D:%d" % (self.width, self.height, self.depth)
        elif self.width and self.height:
            return "W:%d H:%d" % (self.width, self.height)
        else:
            return self.notes

class Medium(models.Model):
    """ Product Medium
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    notes = models.TextField(null=True)
    #notes = models.CharField(max_length=120, null=True)

    def __unicode__(self):
        return self.name

class RoyaltyImg(models.Model):
    """ Royalty Percent/Img for a Product
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    image = models.ImageField(upload_to='royalty_images', max_length=255, height_field='image_height', width_field='image_width', null=True)
    image_height = models.PositiveSmallIntegerField(null=True)
    image_width = models.PositiveSmallIntegerField(null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.name

class Supplier(models.Model):
    """ Supplier of Products SP sells (SP, JH, AIO, ...)
    """
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return "%s : %s" % (code, name)

class Product(models.Model):
    """ Products SmartPractice sells; supplied by Suppliers
    """
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    notes = models.TextField()
    message = models.TextField()
    current_stock = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=0)
    sp_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    size = models.ForeignKey(Size, related_name='+')
    medium = models.ForeignKey(Medium, related_name='+', null=True)
    royalty_img = models.ForeignKey(RoyaltyImg, related_name='+', null=True)
    supplier = models.ForeignKey(Supplier, related_name='products')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.code)

class Catalog(models.Model):
    """ Catalog's SmartPractice advertise products in
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class CatalogIssue(models.Model):
    """ An Issue of a Catalog
    """
    catalog = models.ForeignKey(Catalog, related_name='issues')
    products = models.ManyToManyField(Product, related_name='catalog_issues', through='CatalogIssueProduct')
    issue = models.CharField(max_length=80)

    def __unicode__(self):
        return self.issue

class CatalogIssueProduct(models.Model):
    """ Product advertised in specific issue of a catalog
    """
    page_ref = models.PositiveSmallIntegerField()
    img_ref = models.PositiveSmallIntegerField()
    sub_ref = models.CharField(max_length=3, null=True, blank=True)
    catalog_issue = models.ForeignKey(CatalogIssue)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "%s features in Issue %s of Catalog %s on Page %s Reference %s, %s" % (self.product, self.catalog_issue, self.catalog_issue.catalog, self.page_ref, self.img_ref, self.sub_ref)

class PriceLevelGroup(models.Model):
    """ Price Level Group for a PriceLevel; 'AR', 'LI', etc..
    """
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

# Dont need a through table...
#class PriceLevelProduct(models.Model):

class PriceLevel(models.Model):
    """ Price Level for a Product; products can have multiple price levels
    """
    products = models.ManyToManyField(Product, related_name='price_levels')
#    product = models.ForeignKey(Product, related_name='price_levels')
    price_level_group = models.ForeignKey(PriceLevelGroup, related_name='price_levels', null=True)
    min_amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField()
    cost_per_item = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_per_block = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    block_only = models.BooleanField(default=False)
    notes = models.TextField(null=True)
    #notes = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    """ Order placed by a Customer for Product(s) sold by SmartPractice
    """
    customer = models.ForeignKey(Customer, related_name='orders')
    products = models.ManyToManyField(Product, related_name='+', through='OrderProduct')
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sp_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    order_date = models.DateTimeField(default=datetime.now)
    wanted_by = models.DateTimeField(default=datetime.now)
    invoice_company_name = models.CharField(max_length=255)
    invoice_company_reg = models.CharField(max_length=120)
    invoice_address_line_1 = models.CharField(max_length=255)
    invoice_address_line_2 = models.CharField(max_length=255)
    invoice_suburb = models.CharField(max_length=100)
    invoice_state = models.CharField(max_length=100)
    invoice_postcode = models.CharField(max_length=10)
    invoice_country = models.CharField(max_length=100)
    shipping_attn = models.CharField(max_length=255)
    shipping_address_line_1 = models.CharField(max_length=255)
    shipping_address_line_2 = models.CharField(max_length=255)
    shipping_suburb = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=10)
    shipping_country = models.CharField(max_length=100)
    from_src_order_id = models.IntegerField(null=True, blank=True)
    from_borders_fakeid = models.IntegerField(null=True, blank=True)
    order_notes = models.CharField(max_length=510, null=True, blank=True)

    def __unicode__(self):
        return self.name

class OrderStatus(models.Model):
    """ Status for an Order; an Order can have multiple OrderStatus's as it progresses from Processing -> Shipped etc
    """
    PROCESSING = 'PS'
    CONFIRMED = 'CF'
    AWAITING_PAYMENT = 'AP'
    AWAITING_STOCK = 'AS'
    CANCELLED = 'CN'
    IN_FORFILLMENT = 'IF'
    SHIPPED = 'SD'
    ORDER_STATUS_CHOICES = (
        (PROCESSING, 'Processing'),
        (CONFIRMED, 'Confirmed'),
        (AWAITING_PAYMENT, 'Awaiting Payment'),
        (AWAITING_STOCK, 'Awaiting Stock (Back Order)'),
        (CANCELLED, 'Cancelled'),
        (IN_FORFILLMENT, 'In Forfillment'),
        (SHIPPED, 'Complete (Shipped)'),
    )

    order = models.ForeignKey(Order, related_name='statuses')
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=PROCESSING)
    notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
    
class OrderProduct(models.Model):
    """ 'Line Item' for an order; contains Product ordered on an Order with its quantity
    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    unit_tax = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    sp_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    royalty_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    back_order = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Company(models.Model):
    """ The various companies SmartPractice trade as; 'CAA' 'SP' etc
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25)
    registration = models.CharField(max_length=100)
    logo_img = models.ImageField(upload_to='company_logos', max_length=255, height_field='logo_height', width_field='logo_width', null=True)
    logo_height = models.PositiveSmallIntegerField(null=True)
    logo_width = models.PositiveSmallIntegerField(null=True)

    def __unicode__(self):
        return self.name

class Invoice(models.Model):
    """ An Invoice for an Order issued by a particular Company that SmartPractices trades as
    """
    order = models.ForeignKey(Order, related_name='invoices')
    company = models.ForeignKey(Company, related_name='+')
    timestamp = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name
   
##### END SMART PRACTICE #####

#  
# class CannedImage(models.Model): 
#     """ Default images provided to the users for their coupons. 
#     """ 
#  
# class CannedImage(models.Model): 
#     """ Default images provided to the users for their coupons. 
#     """ 
#     name = models.CharField(max_length=255) 
#     image = models.ImageField(upload_to="%s/canned" % settings.SITE_IMAGES_DIR_NAME) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class Category(models.Model): 
#     name = models.CharField(max_length=100, unique=True) 
#     slug = models.SlugField(unique=True) 
#     ordering = models.PositiveIntegerField(default=0) 
#     seo_text_heading = models.CharField(max_length=100, default="", blank=True) 
#     seo_text = models.TextField(default="", blank=True) 
#     canned_image = models.ForeignKey(CannedImage, null=True, blank=True) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#     def save(self, *args, **kwargs): 
#         if not self.slug: 
#             self.slug = slugify(self.name) 
#         super(Category, self).save(*args, **kwargs) 
#  
#     class Meta: 
#         verbose_name_plural = "categories" 
#         ordering = ('ordering', 'name') 
#  
#  
#     @models.permalink 
#     def get_absolute_url(self): 
#         return ( 
#             'category_detail', (), {'slug': self.slug} 
#         ) 
#  
#  
# class Newsletter(models.Model): 
#     """ A Newsletter type which users may subscribe to 
#     """ 
#     name = models.CharField(max_length=100, help_text="Newsletter Name") 
#     description = models.CharField(max_length=200, help_text="A brief description of this newsletter") 
#     is_active = models.BooleanField(default=True) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#     class Meta: 
#         ordering = ('name',) 
#  
#  
# class SiteUser(BackendUser): 
#     """ A site user, not a site administrator. 
#         We generally don't need to store much about these people, just the minimum. 
#     """ 
#     user = models.OneToOneField(BackendUser, parent_link=True) 
#     mobile = models.CharField(max_length=40, default="", blank=True, help_text="Enter your phone number if you want to text coupons to your mobile for free") 
#     tc_date = models.DateTimeField(null=True, blank=True, help_text="Date when the user agreed to the T&amp;C") 
#     receive_email = models.BooleanField("Accept email newsletters", default=True, help_text="Receive regular site news update, featured coupons, promotions and competitions!") 
#     map_preference = models.BooleanField(default=False) 
#     address = models.TextField(default="", blank=True) 
#     location = models.PointField(null=True, blank=True) 
#  
#     # Preferences 
#     gender = models.CharField(max_length=1, default="", choices=GENDERS, blank=True) 
#     date_of_birth = models.DateField(null=True, blank=True) 
#     receive_sms = models.BooleanField("Accept SMS updates", default=False) 
#     favourite_categories = models.ManyToManyField(Category, blank=True, null=True, related_name="site_users") 
#     newsletter_subscriptions = models.ManyToManyField(Newsletter, blank=True, null=True, related_name="subscribers") 
#     name = models.CharField(max_length=80, blank=True, null=True, unique=True) 
#  
#     objects = UserManager() 
#  
#     def __unicode__(self): 
#         return self.email 
#  
#     def age(self): 
#         if self.date_of_birth: 
#             # This is only rough, no need for 365.2425 or calendar years 
#             return (date.today() - self.date_of_birth).days % 365 
#  
#     @property 
#     def fb_profile(self): 
#         prof = self.social_auth.filter(provider='facebook') 
#         if prof: 
#             return prof[0] 
#         return False 
#  
#  
# class CustomerAccountType(models.Model): 
#     """ what access level do they have, e.g. basic, trial, standard, professional, enterprise """ 
#     name = models.CharField(max_length="40", default="") 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class CustomerAccount(models.Model): 
#     """ A paid account. """ 
#     name = models.CharField(max_length=200, default="") 
#     acn = models.CharField("ABN/ACN", max_length=11, unique=True, default="") 
#  
#     billing_address = models.TextField(default="", blank=True) 
#     physical_address = models.TextField(default="", blank=True) 
#     date_expiry = models.DateField(null=True, blank=True) 
#     account_type = models.ForeignKey(CustomerAccountType) 
#     # did the have a trial, when did / does trial expire 
#     date_trial_expiry = models.DateField(null=True, blank=True) 
#     notes = models.TextField(default="", blank=True) 
#     # Which trader this customer can edit. 
#     traders = models.ManyToManyField("Trader", blank=True, related_name="customer_accounts") 
#     created_by = models.ForeignKey(BackendUser, null=True, related_name="created", editable=False) 
#     last_modified_by = models.ForeignKey(BackendUser, null=True, related_name="modified", editable=False) 
#     date_created = models.DateTimeField(default=datetime.now, editable=False) 
#     date_modified = models.DateTimeField(auto_now=True, editable=False) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class Contact(models.Model): 
#     """ A contactable person. This may be a site """ 
#     first_name = models.CharField(max_length=100, default="", blank=True) 
#     last_name = models.CharField(max_length=100, default="", blank=True) 
#     email = models.EmailField(blank=True) 
#     position = models.CharField(max_length=40, default="", blank=True) 
#     user = models.OneToOneField(BackendUser, null=True, blank=True, related_name="customer_contact") 
#     phone = models.CharField(max_length=40, default="", blank=True) 
#     mobile = models.CharField(max_length=40, default="", blank=True) 
#     fax = models.CharField(max_length=40, default="", blank=True) 
#     mailing_address = models.TextField(default="", blank=True) 
#     notes = models.TextField(default="", blank=True) 
#     is_public = models.BooleanField(default=False) 
#     account = models.ForeignKey(CustomerAccount, null=True, blank=True) 
#  
#     @property 
#     def name(self): 
#         return ' '.join((self.first_name, self.last_name)) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class Locality(models.Model): 
#     """ A location based classification, like a region or a city. """ 
#     COUNTRY, STATE, REGION = 2, 3, 4 
#     LEVELS = ((COUNTRY, "Country"), (STATE, "State"), (REGION, "Region")) 
#  
#     name = models.CharField(max_length=50, default="", blank=True) 
#     slug = models.SlugField(unique=True) 
#     state = models.CharField(max_length=3, choices=STATES, default="", blank=True) 
#  
#     location = models.PointField(null=True, blank=True) 
#     level = models.PositiveSmallIntegerField(choices=LEVELS, default=STATE) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#     def save(self, *args, **kwargs): 
#         # Geocode the coordinates if they are missing 
#         if not self.location and self.name: 
#             geocoded = geocode(', '.join((self.name, COUNTRY))) 
#             if geocoded: 
#                 address, self.location = geocoded 
#                 self.state = state_from_address(address) 
#         if not self.slug: 
#             self.slug = slugify(self.name) 
#         super(Locality, self).save(*args, **kwargs) 
#  
#  
# class Region(Locality): 
#     def save(self, *args, **kwargs): 
#         if not self.level: 
#             self.level = self.REGION 
#         super(Region, self).save(*args, **kwargs) 
#  
#  
# class City(Locality): 
#     def save(self, *args, **kwargs): 
#         if not self.level: 
#             self.level = self.STATE 
#         super(City, self).save(*args, **kwargs) 
#  
#     class Meta: 
#         verbose_name_plural = u"cities" 
#  
#  
# class Suburb(models.Model): 
#     name = models.CharField(max_length=50, default="", blank=True) 
#     postcode = models.CharField(max_length=6, default="", blank=True) 
#     region = models.ForeignKey(Region, null=True, blank=True) 
#     city = models.ForeignKey(City, null=True, blank=True) 
#     state = models.CharField(max_length=3, choices=STATES, default="", blank=True) 
#     region_important = models.BooleanField(default=False, help_text="Should this suburb be shown on regional maps") 
#     state_important = models.BooleanField(default=False, help_text="Should this suburb be shown on state maps") 
#     location = models.PointField(null=True, blank=True) 
#  
#     class Meta: 
#         ordering = ('postcode',) 
#  
#     @property 
#     def placename(self): 
#         elements = [] 
#         if self.name: 
#             elements.append(self.name) 
#         if self.city: 
#             elements.append(str(self.city)) 
#         elif self.region: 
#             elements.append(str(self.region)) 
#         if self.state: 
#             elements.append(self.state) 
#         elements.append("Australia") 
#         return ', '.join(elements) 
#  
#     @property 
#     def georegion(self): 
#         if self.state: 
#             return 'AU-%s' % str(self.state).upper() 
#         else: 
#             return 'AU' 
#  
#     def __unicode__(self): 
#         return ' '.join((self.postcode, self.name)).strip() 
#  
#  
# class TraderShippingCompany(models.Model): 
#     name = models.CharField("Company name", max_length=64) 
#     contact_url = models.URLField(null=True, blank=True) 
#     image = models.ImageField("Shipping company logo", upload_to="%s/trader-shipping" % settings.SITE_IMAGES_DIR_NAME, null=True, blank=True, help_text="If you have a picture of the shipping company logo, upload it here.") 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class TraderShipping(models.Model): 
#     name = models.CharField("Shipping name", max_length=64) 
#     description = HTMLField("Description", null=True, blank=True, default="", help_text="Provide a brief description of the traders shipping features and don't forget to describe any special conditions") 
#     terms_url = models.URLField(null=True, blank=True) 
#     company = models.ForeignKey(TraderShippingCompany, blank=True, null=True) 
#     free_shipping = models.NullBooleanField("Free shipping", default=False) 
#     trader = models.ForeignKey('Trader') 
#     ship_australia = models.BooleanField("Australia and NZ", default=True) 
#     ship_samerica = models.BooleanField("South America", default=False) 
#     ship_namerica = models.BooleanField("North America", default=False) 
#     ship_ea = models.BooleanField("Europe and Asia", default=False) 
#     ship_africa = models.BooleanField("Africa", default=False) 
#     ship_ocenia = models.BooleanField("Ocenia", default=True) 
#  
#     def save(self, *args, **kwargs): 
#         if not self.name: 
#             self.name = self.trader.name 
#         super(TraderShipping, self).save(*args, **kwargs) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class TraderSecurity(models.Model): 
#     name = models.CharField("Name", max_length=64, help_text="It is used only for the staff.") 
#     description = HTMLField("Security Description", null=True, blank=True, help_text="Provide a brief description of how to redeem the traders secuirty measures") 
#     payment_methods = models.ManyToManyField('PaymentMethod', verbose_name="Payment Methods", null=True, blank=True) 
#     security_alliences = models.ManyToManyField('SecurityAllience', verbose_name="Security Alliences", null=True, blank=True) 
#     trader = models.ForeignKey('Trader') 
#  
#     def save(self, *args, **kwargs): 
#         if not self.name: 
#             self.name = self.trader.name 
#         super(TraderSecurity, self).save(*args, **kwargs) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class TraderRedeem(models.Model): 
#     name = models.CharField("Name", max_length=64, help_text="It is used only for the staff.") 
#     description = HTMLField("Redeem Description", null=True, blank=True, help_text="Provide a brief description of how to redeem the traders coupons") 
#     image = models.ImageField("Redeem image", upload_to="%s/traderredeem" % settings.SITE_IMAGES_DIR_NAME, null=True, blank=True, help_text="If you have a picture of the traders redeem page, upload it here.") 
#     trader = models.ForeignKey('Trader') 
#  
#     def save(self, *args, **kwargs): 
#         if not self.name: 
#             self.name = self.trader.name 
#         super(TraderRedeem, self).save(*args, **kwargs) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class TraderReturns(models.Model): 
#     name = models.CharField("Name", max_length=64, help_text="It is used only for the staff.") 
#     description = HTMLField("Returns policy", null=True, blank=True, help_text="Provide a brief description of how to redeem the traders returns policy") 
#     conditions = models.CharField(max_length=512, null=True, blank=True, help_text="Help shoppers understand this traders returns conditions with some key words and be sure to separate these words with semicolons as shown: (free returns; 100 day terms; full-refund 2-10 days)") 
#     trader = models.ForeignKey('Trader') 
#  
#     def save(self, *args, **kwargs): 
#         if not self.name: 
#             self.name = self.trader.name 
#         super(TraderReturns, self).save(*args, **kwargs) 
#  
#     @property 
#     def conditions_list(self): 
#         return self.conditions.split(';') if self.conditions else None 
#  
#     @property 
#     def active_tab(self): 
#         pass 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class PaymentMethod(models.Model): 
#     name = models.CharField("Payment Method", max_length=64) 
#     image = models.ImageField("Logo", upload_to="%s/payment-methods" % settings.SITE_IMAGES_DIR_NAME, null=True, blank=True, help_text="must be 41x22 pixels") 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class SecurityAllience(models.Model): 
#     name = models.CharField("Security Allience", max_length=64) 
#     image = models.ImageField("Logo", upload_to="%s/security-alliences" % settings.SITE_IMAGES_DIR_NAME, null=True, blank=True, help_text="must be 60x30 pixels") 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#  
# class Trader(models.Model): 
#     name = models.CharField("Business name", max_length=200, default="") 
#     slug = models.SlugField(unique=True) 
#  
#     iframe_support = models.BooleanField("iFrame Support", default=False, help_text="Does this traders site support our websites design overlays when directly using a coupon code?") 
#     website = models.URLField(default="", blank=True) 
#     contact = models.ForeignKey(Contact, null=True)  # main contact 
#     logo = models.ImageField(upload_to=slug_filename("%s/traders" % settings.SITE_IMAGES_DIR_NAME), default="", blank=True) 
#     in_top = models.BooleanField("Top Trader", default=False) 
#     description = models.TextField(default="", blank=True) 
#  
#     date_added = models.DateTimeField(default=datetime.now) 
#     is_active = models.BooleanField(default=True) 
#     int_comment = models.CharField("Internal comment", max_length=80, null=True, blank=True) 
#     similar_traders = models.ManyToManyField('self', related_name='similar', blank=True) 
#  
#     facebook = models.URLField(null=True, blank=True, help_text='Only pages in facebook.com domain [http://www.facebook.com/page_name_or_id]') 
#     facebook_id = models.CharField(max_length=16, null=True, editable=False) 
#     twitter = models.URLField(null=True, blank=True) 
#     googleplus = models.URLField(null=True, blank=True) 
#     phone = models.CharField(max_length=64, null=True, blank=True) 
#     email = models.CharField(max_length=128, null=True, blank=True) 
#     skype = models.CharField(max_length=64,null=True, blank=True) 
#  
#     # access code options 
#     access_fb = models.BooleanField('FB Share required', default=False) 
#     access_tw = models.BooleanField('TW Share required', default=False) 
#     access_gp = models.BooleanField('Google+ Share required', default=False) 
#     access_subscribe = models.BooleanField('Subscribe required', default=False) 
#  
#     class Meta: 
#         ordering = ('name',) 
#  
#     def __unicode__(self): 
#         return self.name 
#  
#     def save(self, *args, **kwargs): 
#         if not self.slug: 
#             self.slug = slugify(self.name) 
#             if self.slug.endswith('-coupon'): 
#                 self.slug = '%s-page' % self.slug 
#  
#         logo_commited = self.logo._committed 
#         if not self.description: 
#             self.description = seo_make_msg(self,'static_text') 
#  
#         super(Trader, self).save(*args, **kwargs) 
#         if not logo_commited: 
#             self.logo = trim_image(self.logo) 
#  
#     @models.permalink 
#     def get_absolute_url(self): 
#         return ( 
#             'trader_detail', (), {'slug': self.slug} 
#             ) 
#  
#     def website_link(self): 
#         return u'<a target="_blank" href="%s">%s</a>' % (self.website, self.website) 
#     website_link.allow_tags = True 
#     website_link.short_description = "website" 
#  
#     @property 
#     def num_active_coupons(self): 
#         return self.coupons.filter(active=True, site=settings.SITE_ID, date_expiry__gte=date.today()).count() 
#  
#     @property 
#     def num_all_coupons(self): 
#         return self.coupons.filter(site=settings.SITE_ID).count() 
#  
#     @property 
#     def trader_stats(self): 
#         ret = { 
#             'all': { 
#                 'verified': self.coupons.filter(is_checked=True).count(), 
#                 'active': self.coupons.filter(active=True, date_expiry__gte=date.today()).count(), 
#                 'expired': self.coupons.filter(active=True, date_expiry__lte=date.today()).count(), 
#             }, 
#         } 
#         for it, it_name in COUPON_TYPE: 
#             ret.update({ 
#                 it: { 
#                     'verified': self.coupons.filter(type=it, is_checked=True).count(), 
#                     'active': self.coupons.filter(type=it, active=True, date_expiry__gte=date.today()).count(), 
#                     'expired': self.coupons.filter(type=it, active=True, date_expiry__lte=date.today()).count(), 
#                 } 
#             }) 
#  
#         return ret 
#  
#     @property 
#     def display_img(self): 
#         if self.logo: 
#             return self.logo 
#         try: 
#             return self.coupons.exclude(image='').order_by('pk')[0].image 
#         except: 
#             return None 
#  
#     @property 
#     def votes_percent(self): 
#         co = self.rating.count() 
#         if not co: 
#             return 0 
#         return (sum([x.vote for x in self.rating.all()]) / self.rating.count()) * 20 
#  
#     @property 
#     def shipping(self): 
#         try: 
#             return self.tradershipping_set.all()[0] 
#         except: 
#             return False 
#  
#     @property 
#     def security(self): 
#         try: 
#             return self.tradersecurity_set.all()[0] 
#         except: 
#             return False 
#  
#     @property 
#     def redeem(self): 
#         try: 
#             return self.traderredeem_set.all()[0] 
#         except: 
#             return False 
#  
#     @property 
#     def return_policy(self): 
#         try: 
#             return self.traderreturns_set.all()[0] 
#         except: 
#             return False 
#  
#     @property 
#     def cross_domain_coupons(self, without_current=True): 
#         ret = [] 
#         lst = Site.objects.all() 
#         if without_current: 
#             lst = lst.exclude(id=settings.SITE_ID) 
#  
#         for s in lst: 
#             n = Coupon.objects.filter(trader=self, site=s).count() 
#             if n: 
#                 ret.append({ 
#                     'site': s, 
#                     'num': n 
#                 }) 
#  
#         return ret 
#  
#  
# class TraderWeeklyRating(models.Model): 
#     trader = models.ForeignKey(Trader, related_name="rating_weekly") 
#     site = models.ForeignKey(Site) 
#     value = models.FloatField() 
#     in_top = models.BooleanField(default=False)  # Trader.in_top overlapping 
#  
#     objects = models.Manager() 
#     on_site = CurrentSiteManager() 
#  
#     class Meta: 
#         ordering = ('-in_top', '-value') 
#  
#  
# class TraderRating(models.Model): 
#     trader = models.ForeignKey(Trader, related_name="rating") 
#     user = models.ForeignKey(SiteUser, db_index=True, null=True, blank=True) 
#     ip_address = models.IPAddressField(null=True, blank=True) 
#     vote = models.SmallIntegerField(default=5, choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))) 
#     timestamp = models.DateTimeField(auto_now_add=True, editable=False) 
#  
#     def __unicode__(self): 
#         return u'%d for %s' % (self.vote, self.trader) 
#  
#     class Meta: 
#         unique_together = (('trader', 'user'),) 
#  
#  
# def suburb_from_address(address): 
#     try: 
#         components = address.split(",")[-2].strip().split() 
#         name, state, postcode = " ".join(components[:-2]), components[-2], components[-1] 
#         if REVERSE_STATES_DICT.get(state): 
#             state=REVERSE_STATES_DICT[state] 
#  
#         if len(state) > 3:  # paranormal? 
#             for a, b in STATES: 
#                 if a in address or b in address: 
#                     state = a 
#     except IndexError: 
#         # Abort if anything doesn't look right. 
#         return 
#  
#     suburb = Suburb.objects.filter(postcode=postcode) 
#     if suburb: 
#         # choose best if multiple, #324 
#         if suburb.count() > 1 and suburb.filter(location__isnull=False).count() > 0: 
#             suburb = suburb.filter(location__isnull=False) 
#         suburb = suburb[0] 
#         if not suburb.name or not suburb.state: 
#             suburb.name = suburb.name or name 
#             suburb.state = suburb.state or state 
#             suburb.save() 
#     else: 
#         suburb = Suburb.objects.create(name=name, state=state, postcode=postcode) 
#  
#     return suburb 
#  
#  
# class TraderLocation(models.Model): 
#     """ This allows traders to have more than one location 
#         (where a single coupon is valid) 
#     """ 
#     trader = models.ForeignKey(Trader, related_name="locations") 
#     name = models.CharField("Location name", max_length=200, default="", blank=True, help_text="If this location has a branch/store/outlet name") 
#     contact = models.ForeignKey(Contact, null=True, blank=True, help_text="main contact for this location") 
#     address = models.TextField(default="", blank=True) 
#     suburb = models.ForeignKey(Suburb, null=True, blank=True) 
#     # state, region, country information is contained in the suburb listing 
#     location = models.PointField(null=True, blank=True) 
#     objects = models.GeoManager() 
#  
#     def __unicode__(self): 
#         #return self.name or self.suburb_id and self.suburb.name or u"" 
#         return "%s: %s" % (self.trader.name, self.address or self.name or self.suburb or "#%s" % self.id) 
#  
#     def save(self, *args, **kwargs): 
#         # Geocode the coordinates if they are missing 
#         # wrong 
#         # update coords always! guys want to edit addresses 
#         if self.address: 
#             geocoded = geocode(self.address) 
#             if geocoded: 
#                 address, self.location = geocoded 
#                 self.suburb = suburb_from_address(address) 
#             else:  # inform Lewi and Dom 
#                 msg = "Hi Dom and Lewi,\n\n" 
#                 msg += 'somebody input address "%s", but Google failed to recoginze it.' % self.address 
#                 msg += 'Trader=%s' % self.trader 
#                 msg += 'TraderLocation.id=%s' % self.id 
#                 msg += "\n\nI Love Coupons site" 
#                 emails = [x.email for x in BackendUser.objects.filter(is_superuser=True, groups__name='Notify by Email')] 
#                 send_mail('ILC geocode failed', msg, 'noreply@ilovecoupons.com.au', emails) 
#         super(TraderLocation, self).save(*args, **kwargs) 
#  
#     def delete(self):  # this prevent breaking of online_coupon flag 
#         for lc in LocatedCoupon.objects.filter(trader_location=self): 
#             lc.delete() 
#         super(TraderLocation, self).delete() 
#  
#     class Meta: 
#         ordering = ('trader',) 
#  
#  
# class Coupon(models.Model): 
#     site = models.ForeignKey(Site, null=True, blank=True) 
#     type = models.CharField(choices=COUPON_TYPE, default=COUPON_TYPE[0][0], max_length=16) 
#     trader = models.ForeignKey(Trader, related_name="coupons") 
#     heading = models.CharField("Coupon Heading*", default="", max_length=150, help_text="Stand out with a short, sharp product heading with a few key words.") 
#  
#     description = HTMLField("Description*", blank=True, default="", help_text="Provide a brief description of the coupon's features and don't forget to describe: The bargain, how to redeem it and any special conditions") 
#     description.allow_tags = True 
#     description.is_safe = True 
#  
#     date_expiry = models.DateField("Coupon Expiry Date", null=True, blank=True, help_text="Leave this blank if you don't know") 
#     active = models.BooleanField(default=True) 
#     online_only = models.BooleanField(default=True) 
#     is_checked = models.BooleanField("has been manually checked", default=False) 
#     verified_by = models.ForeignKey(SiteUser, null=True, related_name="verified_coupons") 
#     verified_by_dt = models.DateTimeField(editable=False, null=True) 
#  
#     code = models.CharField("Coupon Code", max_length=100, default="", blank=True, help_text="If this coupon requires a code to redeem it, please enter it above.") 
#     # please use clink (countable link) in templates! 
#     link = models.URLField("Website link", default="", blank=True, help_text="If it is an online deal, please provide the website address.", max_length=500, verify_exists=False) 
#     image = models.ImageField("Coupon Pic / Logo", upload_to="%s/coupons" % settings.SITE_IMAGES_DIR_NAME, default="", blank=True, help_text="If you have a picture of the coupon or the company logo, upload it here.  A default image will be used otherwise.") 
#     canned_image = models.ForeignKey(CannedImage, null=True, blank=True) 
#  
#     fb_image = models.ImageField("Pic / Logo for Facebook sharing", upload_to="%s/coupons" % settings.SITE_IMAGES_DIR_NAME, default="", blank=True, help_text="This picture will be used is someone shares the coupon page on Facebook.") 
#     category = models.ForeignKey(Category, related_name="coupons", null=True, blank=True, help_text="Assign this coupon to a category.") 
#     tags = models.CharField(max_length=750, blank=True, default="", help_text="Help shoppers to find this coupon by tagging it with some key words and be sure to separate these words with commas as shown: (computers, apple, 15 inch laptop)") 
#  
#     date_added = models.DateTimeField(auto_now_add=True, editable=False) 
#     date_update = models.DateTimeField(auto_now=True, editable=False) 
#     posted_by = models.ForeignKey(SiteUser, null=True, related_name="posted_coupons") 
#  
#     # PageRank 
#     rank = models.PositiveIntegerField("page rank", default=0, help_text="General relevance") 
#     local_rank = models.PositiveIntegerField("local page rank", default=0, help_text="Relevance for local searches") 
#     manual_rank = models.BooleanField("manual page rank override", default=False, help_text="Check to preserve manual rank overrides") 
#  
#     # Denormalised data 
#     votes_sum = models.IntegerField(default=0, editable=False) 
#     votes_count = models.IntegerField(default=0, editable=False) 
#     votes_percent = models.IntegerField(null=True, editable=False) 
#     rating = models.FloatField(null=True, blank=True) 
#     rating_weekly = models.FloatField(null=True, blank=True) 
#     rating_manual = models.IntegerField(null=True, blank=True) 
#  
#     slug = models.SlugField(unique=True, blank=True, null=True) 
#     affiliate = models.NullBooleanField(default=False) 
#     notify_expiration = models.BooleanField("Notify when the coupon expires", default=False) 
#     never_notify_expiration = models.BooleanField("Never notify expiration (even if is affiliate or something)", default=False) 
#     scanned_image = models.ImageField("Scanned Coupon", upload_to="%s/scoupon" % settings.SITE_IMAGES_DIR_NAME, null=True, blank=True, help_text="Scanned image of coupon here") 
#     int_comment = models.CharField("Internal comment", max_length=300, null=True, blank=True) 
#  
#     # we have no idea how many special coupons will be, therefore use each new flag as a power of 2, e.g. 1,2,4,8,etc then we can sum it like 1+2 if necessary and create some special function to determine wich flags are active 
#     # first special flag is: couponcode 
#     # see "determine_special" filter 
#     special = models.PositiveIntegerField("Special Flags", help_text="Speciality Flags (use unix-like bit sum)", null=True, blank=True) 
#  
#     master_brands = models.ManyToManyField(Trader, verbose_name="Master brands", null=True, blank=True) 
#     enslaved_by = models.ForeignKey('self', null=True, blank=True) 
#     noindex_zone = models.BooleanField('noindex redirect', default=False) 
#     noindex_time = models.DateTimeField('noindex redirect time', null=True, blank=True) 
#     source = models.CharField(max_length=12, choices=COUPON_SOURCE, default='-') 
#     termconditions = models.TextField('Terms & Conditions', blank=True, null=True, help_text="Help shoppers understand this coupon by terms with some key words and be sure to separate these words with new lines as shown:<br><br> one valid per person<br>second pair of equal of lessor value<br>melbourne residents only") 
#     banner = models.ImageField('Banner', upload_to="%s/coupons/banner" % settings.SITE_IMAGES_DIR_NAME, blank=True, null=True, help_text="Banner (width=468px)") 
#  
#     # access code options 
#     access_fb = models.BooleanField('FB Share required', default=False) 
#     access_tw = models.BooleanField('TW Share required', default=False) 
#     access_gp = models.BooleanField('Google+ Share required', default=False) 
#     access_subscribe = models.BooleanField('Subscribe required', default=False) 
#  
#     # managers 
#     on_site = CurrentSiteManager() 
#     objects = CouponManager() 
#  
#     def admin_trader_link(self): 
#         return '<a href="/admin/coupons/trader/%s/">%s</a>' % (self.trader.id, self.trader.name) 
#     admin_trader_link.allow_tags = True 
#  
#     def __unicode__(self): 
#         return self.heading 
#  
#     @models.permalink 
#     def get_absolute_url(self): 
#         if getattr(self.site.dsettings.theme, 'slug', None) == 'old_site': 
#             return ('coupon_detail_old_style', (), { 
#                 'coupon_slug': self.slug 
#             }) 
#  
#         return ('coupon_detail', (), { 
#             'slug': self.trader.slug, 
#             'coupon_slug': self.slug 
#         }) 
#  
#     @models.permalink 
#     def get_absolute_url_old_style(self): 
#         return ('coupon_detail_old_style', (), { 
#             'coupon_slug': self.slug 
#         }) 
#  
#     def website_link(self): 
#         return mark_safe('<a target="_blank" href="%s">show</a>' % (self.get_absolute_url(),)) 
#     website_link.allow_tags = True 
#     website_link.short_description = "Link" 
#  
#     def check_verify(self, user): 
#         try: 
#             verify = Worked.objects.get(coupon=self, user=user) 
#             self.verify = [1, 2][verify.worked] 
#         except ObjectDoesNotExist: 
#             self.verify = 0 
#  
#     @property 
#     def access(self): 
#         if not self.specific_access: 
#             ac = { 
#                 'fb': self.trader.access_fb, 
#                 'tw': self.trader.access_tw, 
#                 'gp': self.trader.access_gp, 
#                 'sb': self.trader.access_subscribe 
#             } 
#         else: 
#             ac = { 
#                 'fb': self.access_fb, 
#                 'tw': self.access_tw, 
#                 'gp': self.access_gp, 
#                 'sb': self.access_subscribe 
#             } 
#  
#         if not self.trader.facebook_id: 
#             ac['fb'] = False 
#         if not self.trader.twitter: 
#             ac['tw'] = False 
#         if not self.trader.googleplus: 
#             ac['gp'] = False 
#  
#         return ac 
#  
#     @property 
#     def is_special_code(self): 
#         if self.affiliate and self.special == 1: 
#             return True 
#         return False 
#  
#     @property 
#     def specific_access(self): 
#         if self.access_fb or self.access_tw or self.access_gp or self.access_subscribe: 
#             return True 
#         return False 
#  
#     @property 
#     def verify_count(self): 
#         return self.worked_set.filter(worked=True).count() 
#  
#     @property 
#     def main_image(self): 
#         return self.image or self.trader.logo or self.category.canned_image.image 
#  
#     @property 
#     def clink(self):  # countable link - use it in templates to count clicks! 
#         if self.link: 
#             return "/coupons/%s/website/" % self.slug 
#         else: 
#             return '' 
#  
#     @property 
#     def votes_percentile(self): 
#         if self.votes_percent is not None: 
#             return (int(self.votes_percent) / 10 + 1) * 10 
#  
#     @property 
#     def votes_percent_text(self): 
#         if self.votes_percent is not None: 
#             return u"%s%%" % self.votes_percent 
#         return u"New" 
#  
#     @property 
#     def expiry(self): 
#         today = date.today() 
#         if self.date_expiry < today: 
#             return u'<span class="expired">Expires: %s days ago</span>' % (today - self.date_expiry).days 
#         elif self.date_expiry: 
#             return u'Expires %s' % naturalday(self.date_expiry) 
#  
#     @property 
#     def expiry_days(self): 
#         today = date.today() 
#         if self.date_expiry < today: 
#             return (today - self.date_expiry).days 
#         else: 
#             return (self.date_expiry - today).days 
#  
#     @property 
#     def is_expired(self): 
#         if self.date_expiry and self.date_expiry < date.today(): 
#             return True 
#         return False 
#  
#     @property 
#     def has_coupon_popup(self): 
#         if self.specific_access or self.trader.access_fb or self.trader.access_tw or self.trader.access_gp or self.trader.access_subscribe: 
#             return True 
#         return False 
#  
#     @property 
#     def status(self): 
#         if self.is_expired: 
#             return 'expired' 
#         if self.is_checked: 
#             return 'verified' 
#         return 'active' 
#  
#     def coupon_slugify(self):  # make something like sony-coupon7 
#         slug = "%s-coupon" % self.trader.slug[:39]  # compatible with up to 9999 coupons for one trader 
#         exist = Coupon.objects.filter(slug__istartswith=slug).exclude(id=self.id).order_by('-id') 
#         if exist:  # if already exist, then +1 at the end 
#             extra = exist[0].slug.replace(slug, "") 
#             if not extra: 
#                 num = 2 
#             else: 
#                 try: 
#                     num = int(extra[1:]) 
#                 except ValueError: 
#                     num = 2 
#             while True:  # right into space! 
#                 num += 1 
#                 bslug = slug + "-" + str(num) 
#                 if not Coupon.objects.filter(slug=bslug).count(): 
#                     break 
#         else: 
#             bslug = slug 
#         return bslug 
#  
#     def save(self, *args, **kwargs): 
#         if not self.image and self.canned_image: 
#             self.image = self.canned_image.image 
#         if not self.slug: 
#             self.slug = self.coupon_slugify() 
#  
#         super(Coupon, self).save(*args, **kwargs) 
#  
#     def get_votes_percent(self): 
#         """ A method to regenerate the votes_percent. """ 
#         self.votes_percent = (Decimal(100) * ((self.votes_count - self.votes_sum) / 2 + self.votes_sum) / self.votes_count).quantize(Decimal("1")) 
#         return self.votes_percent 
#  
#     def related_coupons(self): 
#         """ Return a queryset of related coupons. """ 
#         return self.trader.coupons.all().exclude(id=self.id) 
#  
#     def get_cur_month_traffic(self): 
#         month = date.today().replace(day=1) 
#         return MounthTraffic.objects.get_or_create(coupon=self, mounth=month)[0] 
#  
#     def get_prev_month_traffic(self): 
#         month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1) 
#         return MounthTraffic.objects.get_or_create(coupon=self, mounth=month)[0] 
#  
#     def inc_traffic_counter(self): 
#         obj = self.get_cur_month_traffic() 
#         obj.count += 1 
#         obj.save() 
#  
#     class Meta: 
#         ordering = ('-pk',) 
#  
#  
# class MasterSlaveOverwrite(models.Model):  # 386, in comments 
#     master = models.ForeignKey(Trader, null=True, blank=True, related_name="master_rel") 
#     slave = models.ForeignKey(Trader,  null=True, blank=True, related_name="slave_rel") 
#     link = models.URLField(null=True, blank=True, max_length=500, verify_exists=False) 
#     image = models.ImageField(null=True, blank=True, upload_to="%s/coupons" % settings.SITE_IMAGES_DIR_NAME) 
#  
#     def __unicode__(self): 
#         return "%s->%s" % (self.master, self.slave) 
#  
#     class Meta: 
#         unique_together = ('master', 'slave') 
#  
#  
# class CouponCode(models.Model): 
#     coupon = models.ForeignKey(Coupon) 
#     code = models.CharField("Coupon Code", max_length=100) 
#     user = models.ForeignKey(SiteUser, null=True, blank=True) 
#     ip_address = models.IPAddressField(null=True, blank=True) 
#     used_at = models.DateTimeField(null=True, blank=True) 
#     useragent = models.CharField(max_length=255,null=True,blank=True) 
#     int_comment = models.CharField(max_length=255, null=True, blank=True) 
#  
#     def __unicode__(self): 
#         return "%s::%s"%(self.coupon, self.code) 
#  
#     class Meta: 
#         unique_together = ('coupon', 'code',) 
#  
#  
# class LocatedCouponManager(models.GeoManager): 
#     """ Manages our located coupon denormalised model. """ 
#  
#     def select_related(self): 
#         """ Select related by default, avoiding the unnecessary trader location field. 
#         """ 
#         return self.get_query_set().select_related('coupon', 'trader') 
#  
#     def quick_create(self, location, coupon): 
#         postcode = location.suburb and location.suburb.postcode or "" 
#         state = location.suburb and location.suburb.state or "" 
#         self.create(coupon=coupon, trader=coupon.trader, trader_location=location, postcode=postcode, state=state, location=location.location, name=location.name) 
#  
#     def location_added(self, location): 
#         for coupon in location.trader.coupons.all(): 
#             self.quick_create(location, coupon) 
#  
#     def location_updated(self, location): 
#         # locatecoupons with specified location and trader to update their parameters 
#         locations = self.get_query_set().filter(trader=location.trader).filter(trader_location=location) 
#         if location.suburb: 
#             postcode = location.suburb.postcode 
#             state = location.suburb.state 
#             locations.update(postcode=postcode, state=state, name=location.name, location=location.location) 
#  
#     def suburb_updated(self, suburb): 
#         locations = self.get_query_set().filter(trader_location__suburb=suburb).update(postcode=suburb.postcode, state=suburb.state) 
#  
#     def reset_dataset(self): 
#         """ Reset the entire located coupon dataset. 
#             This will be lots of queries. 
#         """ 
#         self.get_query_set().delete() 
#         all_coupons = iter(Coupon.objects.all().select_related().order_by('trader')) 
#         all_locations = TraderLocation.objects.all().select_related().order_by('trader') 
#  
#         # Work through the locations and coupons simultaneously, creating objects where the trader is the same 
#         coupon = None 
#         try: 
#             for location in all_locations: 
#                 while 1: 
#                     if coupon is None: 
#                         coupon = all_coupons.next() 
#                     if coupon.trader != location.trader: 
#                         break 
#                     else: 
#                         self.quick_create(location, coupon) 
#                         coupon = None 
#         except StopIteration: 
#             return 
#  
#  
# class LocatedCoupon(models.Model): 
#     """ A denormalised model that links an instance of a coupon with a location. 
#         This should be added and removed with changes to coupons and trader 
#         locations. 
#  
#     """ 
#     coupon = models.ForeignKey(Coupon, db_index=True, related_name="located_coupons") 
#     trader = models.ForeignKey(Trader, db_index=True, related_name="located_coupons") 
#  
#     # This is for syncing, not searching 
#     trader_location = models.ForeignKey(TraderLocation, db_index=True, related_name="located_coupons") 
#     # These are for searching 
#     name = models.CharField(max_length=200, default="", blank=True) 
#     postcode = models.CharField(max_length=6, db_index=True, default="", blank=True) 
#     state = models.CharField(max_length=3, db_index=True, choices=STATES, default="", blank=True) 
#     location = models.PointField(null=True, blank=True) 
#  
#     objects = LocatedCouponManager() 
#  
#     def __unicode__(self): 
#         return 'coupon %d, trader_location %d' % (self.coupon_id, self.trader_location_id) 
#  
#     class Meta: 
#         unique_together = ('coupon', 'trader_location') 
#  
#     def save(self, *args, **kwargs):  # here we manage online_only flag of coupon 
#         self.trader = self.coupon.trader 
#  
#         if self.trader_location: 
#             if self.trader_location.location:  # and not self.location: 
#                 self.location = self.trader_location.location 
#             if self.trader_location.suburb and self.trader_location.suburb.postcode:  #and not self.postcode: 
#                 self.postcode = self.trader_location.suburb.postcode 
#             if self.trader_location.suburb and self.trader_location.suburb.state:  #and not self.state: 
#                 self.state = self.trader_location.suburb.state 
#  
#         if self.location: # have location 
#             if self.coupon.online_only: 
#                 self.coupon.online_only = False 
#                 self.coupon.save() 
#         else:  # no location 
#             if not self.coupon.online_only:  # but coupon thinks it has location 
#                 check4loc = self.coupon.located_coupons.filter(location__isnull=False) 
#                 if not check4loc:  # we ensured that there are no locations for this coupon 
#                     self.coupon.online_only=True 
#                     self.coupon.save() 
#  
#         super(LocatedCoupon, self).save(*args, **kwargs) 
#  
#     def delete(self): 
#         coupon = self.coupon 
#         super(LocatedCoupon, self).delete() 
#         check4loc=coupon.located_coupons.filter(location__isnull=False) 
#         if not check4loc: 
#             coupon.online_only=True 
#             coupon.save() 
#  
#  
# class CouponVote(models.Model): 
#     coupon = models.ForeignKey(Coupon, db_index=True, related_name="votes") 
#     user = models.ForeignKey(SiteUser, db_index=True, null=True, blank=True) 
#     ip_address = models.IPAddressField(null=True, blank=True) 
#     vote = models.SmallIntegerField(default=0, choices=((1, "Positive"), (-1, "Negative"))) 
#     timestamp = models.DateTimeField(default=datetime.now, editable=False) 
#  
#     def __unicode__(self): 
#         return u'%d for %s' % (self.vote, self.coupon) 
#  
#     class Meta: 
#         unique_together = (('coupon', 'user'),) 
#  
#     def save(self, *args, **kwargs): 
#         super(CouponVote, self).save(*args, **kwargs) 
#         # Update denormalised fields 
#         Coupon.objects.register_vote(vote=self) 
#  
#  
# class CouponInteractionManager(models.Manager): 
#     def add(self, request, coupon, type): 
#         user = request.user.siteuser 
#         interaction, created = CouponInteraction.objects.get_or_create(coupon=coupon, type=type, user=user) 
#         return created 
#  
#  
# class CouponInteraction(models.Model): 
#     coupon = models.ForeignKey(Coupon, related_name="interactions") 
#     type = models.CharField(max_length=1, choices=INTERACTION_TYPES) 
#     user = models.ForeignKey(SiteUser, null=True, blank=True) 
#     ip_address = models.IPAddressField(null=True, blank=True) 
#     timestamp = models.DateTimeField(default=datetime.now, editable=False) 
#  
#     objects = CouponInteractionManager() 
#  
#     def __unicode__(self): 
#         return u'%s for %s' % (self.get_type_display(), self.coupon) 
#  
#  
# class FavoriteCoupon(models.Model): 
#     coupon = models.ForeignKey(Coupon, related_name="favorites") 
#     user = models.ForeignKey(SiteUser, null=True) 
#  
#     def __unicode__(self): 
#         return u'%s likes %s' % (self.user, self.coupon) 
#  
#     class Meta: 
#         unique_together = ('coupon', 'user') 
#  
#  
# class FriendLink(models.Model): 
#     user = models.ForeignKey(BackendUser, blank=True, null=True) 
#     email = models.EmailField() 
#     comments = models.TextField(blank=True) 
#     name = models.CharField(max_length=50, blank=True) 
#     created = models.DateTimeField(auto_now_add=True) 
#  
#  
# # http://en.wikipedia.org/wiki/Postcodes_in_Australia 
# class Postcode(models.Model): 
#     postcode = models.CharField(max_length=6) 
#     locality = models.CharField(max_length=80) 
#     comments = models.CharField(max_length=160, null=True, blank=True) 
#     state = models.CharField(max_length=3, choices=STATES) 
#     location = models.PointField(srid=4326, null=True, blank=True) 
#  
#     class Meta: 
#         unique_together=(('postcode','locality','state')) 
#  
#     def __unicode__(self): 
#         return u'%s: %s, %s' % (self.postcode, self.locality, self.state) 
#  
#  
# class Event(models.Model): 
#     type = models.CharField("Action", choices=ETYPES, default=ETYPES[0][0], max_length=16) 
#     coupon = models.ForeignKey(Coupon, null=True, blank=True) 
#     info = models.CharField(max_length=255, null=True, blank=True) 
#     ip = models.IPAddressField(null=True,blank=True) 
#     date = models.DateTimeField(auto_now_add=True) 
#     user = models.ForeignKey(SiteUser, null=True, blank=True, editable=False) 
#     useragent = models.CharField(max_length=255,null=True,blank=True) 
#     rating = models.SmallIntegerField(null=True, blank=True) 
#  
#     def __unicode__(self): 
#         return u'%s' % self.date 
#  
#     def save(self, *args, **kwargs): 
#         if self.useragent: 
#             self.useragent = self.useragent[:255] 
#             for bot in BOTLIST: 
#                 if self.useragent.startswith(bot): 
#                     return 
#         else: 
#             self.useragent = "" 
#  
#         super(Event, self).save(*args, **kwargs) 
#  
#         # keep it below real save to take into account new rating 
#         if self.coupon:  # fast and dirty 
#             Coupon.objects.update_denormalised_fields(self.coupon) 
#  
#  
# class CommentSubscription(models.Model): 
#     email = models.EmailField() 
#     obj = models.ForeignKey(Coupon) 
#  
#     class Meta: 
#         unique_together = [('email', 'obj')] 
#  
#  
# class TraderCommentSubscription(models.Model): 
#     email = models.EmailField() 
#     obj = models.ForeignKey(Trader) 
#  
#     class Meta: 
#         unique_together = [('email', 'obj')] 
#  
#  
# class PostCommentSubscription(models.Model): 
#     email = models.EmailField() 
#     obj = models.ForeignKey('blog.Post') 
#  
#     class Meta: 
#         unique_together = [('email', 'obj')] 
#  
#  
# class NewsletterSubscription(models.Model): 
#     name = models.CharField(max_length=80, null=True, blank=True) 
#     email = models.EmailField(unique=True) 
#     postcode = models.CharField(max_length=6, default='', blank=True) 
#     subscribed = models.BooleanField(default=True) 
#     created_on = models.DateField(auto_now_add=True) 
#     updated_on = models.DateField(auto_now=True) 
#     user = models.OneToOneField(BackendUser, null=True, blank=True) 
#     site = models.ForeignKey(Site, null=True, blank=True) 
#     trader = models.ManyToManyField(Trader, null=True, blank=True) 
#  
#     objects = Manager() 
#     on_site = CurrentSiteManager() 
#  
#     def __unicode__(self): 
#             return u'%s' % (self.email,) 
#  
#  
# class MounthTraffic(models.Model): 
#     coupon = models.ForeignKey(Coupon) 
#     mounth = models.DateField() 
#     count = models.IntegerField(default=0) 
#  
#     class Meta: 
#         unique_together = [('coupon', 'mounth')] 
#  
#     def __unicode__(self): 
#         return u'%s | %i | %s' % (self.mounth, self.count, self.coupon) 
#  
#  
# class EditorsChoice(models.Model): 
#     coupon = models.ForeignKey(Coupon) 
#     posted_by = models.ForeignKey(SiteUser, null=True) 
#     date_added = models.DateTimeField(default=datetime.now, editable=False) 
#  
#     def __unicode__(self): 
#         return u'EChoice for %s' % (self.coupon,) 
#  
#  
# class Worked(models.Model): 
#     coupon = models.ForeignKey(Coupon) 
#     user = models.ForeignKey(SiteUser) 
#     worked = models.BooleanField("Coupon worked", default=True) 
#  
#     class Meta: 
#         unique_together = ('coupon', 'user') 
#  
#     def __unicode__(self): 
#         return u'Worked for %s' % (self.user,) 
#  
# # Signals 
# signals.post_save.connect(coupon_post_save, sender=Coupon) 
# #signals.m2m_changed.connect(coupon_m2m_changed, sender=Coupon.master_brands.through) 
# signals.post_save.connect(trader_post_save, sender=Trader) 
# signals.post_save.connect(suburb_post_save, sender=Suburb) 
# signals.post_save.connect(backenduser_post_save, sender=BackendUser) 
