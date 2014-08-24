# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
from django.conf import settings
from decimal import Decimal
#from colorfield.fields import ColorField
#from frontend.utils import phone_for_search
#from .managers import SPUserManager


#class SPUser(AbstractBaseUser):
#    F_WEIGHT = [
#        ('bold', 'bold'),
#        ('bolder', 'bolder'),
#        ('lighter', 'lighter'),
#        ('normal', 'normal')
#    ]
#    username = models.CharField(max_length=64, unique=True)
#    email = models.EmailField(
#        verbose_name='email address',
#        max_length=255,
#        unique=True,
#        null=True,
#        blank=True
#    )
#    is_active = models.BooleanField(default=True)
#    is_admin = models.BooleanField(default=False)
#
#    font_size = models.IntegerField(default=12, null=True, blank=True)
#    font_weight = models.CharField(choices=F_WEIGHT, default='normal', max_length=16, null=True, blank=True)
#    bg_color = ColorField(default='#FFFFFF', null=True, blank=True)
#    label_bg_color = ColorField(default='#EEEEEE', null=True, blank=True)
#    font_color = ColorField(default='#2B2B2B', null=True, blank=True)
#    jodabrian_visible = models.BooleanField(default=True)
#
#    USERNAME_FIELD = 'username'
#    objects = SPUserManager()
#
#    def get_full_name(self):
#        # The user is identified by their email address
#        return self.email

#    def get_short_name(self):
        # The user is identified by their email address
#        return self.email

#    def __unicode__(self):
#        return self.username

#    def has_perm(self, perm, obj=None):
#        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
#        return True

#    def has_module_perms(self, app_label):
#        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
#        return True

#    @property
#    def is_staff(self):
#        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
#        return self.is_admin


class ImportNote(models.Model):
    """ Import notes
    """
    model = models.CharField(max_length=50)
    model_id = models.PositiveIntegerField()
    type = models.CharField(max_length=50, default=None)
    text = models.TextField()
    note = models.TextField(null=True, blank=True)
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
    telephone_clean = models.CharField(max_length=40, blank=True)  # auto-generated field
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
    slug = models.SlugField(unique=True, max_length=150)
    notes = models.ManyToManyField('Note', related_name='c_notes', blank=True)
    last_read = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.set_slug()
#        self.telephone_clean = phone_for_search(self.telephone)
        super(Customer, self).save(*args, **kwargs)

    def set_slug(self):
        if not self.slug:
            next_pk = 1
            if Customer.objects.using('target_db').all().count() > 0:
                next_pk = Customer.objects.using('target_db').last().pk + 1
            
            self.slug = "%i-%s" % (next_pk, slugify(self.name))

    @property
    def same_delivery_address(self):
        if self.address_line_1 == self.delivery_address_line_1 and \
                self.address_line_2 == self.delivery_address_line_2 and \
                self.delivery_suburb == self.suburb and \
                self.delivery_state == self.state and \
                self.delivery_postcode == self.postcode and \
                self.name == self.delivery_attn:
            return True
        return False
 
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
        return '%s %s' % (self.first_name, self.surname)

    def info(self):
        ret = '%s %s' % (self.first_name, self.surname)
        if self.phone:
            ret = '%s, %s' % (ret, self.phone)
        if self.email:
            ret = '%s, %s' % (ret, self.email)

        return ret


class Size(models.Model):
    """ Product Size/Dimensions
    """
    width = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    units = models.CharField(max_length=80, null=True)
    notes = models.TextField(null=True)
    sub_notes = models.TextField(null=True)

    class Meta:
        ordering = ('width', 'height', 'depth', 'units')

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

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.description


class Supplier(models.Model):
    """ Supplier of Products SP sells (SP, JH, AIO, ...)
    """
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ('code', 'name')

    def __unicode__(self):
        return "%s : %s" % (self.code, self.name)


class Product(models.Model):
    """ Products SmartPractice sells; supplied by Suppliers
    """
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    notes = models.ManyToManyField('Note', related_name='p_notes', blank=True)
    message = models.TextField()
    current_stock = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=0)
    sp_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    size = models.ForeignKey(Size, related_name='+', on_delete=models.PROTECT)
    medium = models.ForeignKey(Medium, related_name='+', null=True, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, related_name='products', on_delete=models.PROTECT)
    royalty_group = models.ForeignKey('RoyaltyGroup', null=True, on_delete=models.PROTECT)
    manual_royalty = models.PositiveSmallIntegerField(help_text='[0..100]%', null=True)
    last_read = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    @property
    def royalty(self):
        return self.manual_royalty or self.royalty_group.royalty if self.royalty_group else 0

    @property
    def default_price(self):
        if self.price_levels.exists():
            return self.price_levels.order_by('-cost_per_item')[0].cost_per_item
        return self.sp_cost * (1 + Decimal(self.royalty)/100)

    @property
    def back_orders(self):
        ret = []
        for a in self.ordered_list.all():
            for b in a.back_orders.filter(complete=False):
                ret.append(b)
        return ret

    @property
    def stock_out(self):
        """
        @return: sum of qty from all active orders
        """
        qty = 0
        for o in self.ordered_list.all():
            if o.order.last_status not in (OrderStatus.CANCELLED, OrderStatus.SHIPPED):
                qty += o.quantity
        return qty

    @property
    def last_order(self):
        try:
            return self.ordered_list.order_by('-order__order_date')[0]
        except IndexError:
            return None

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.code)


class Catalog(models.Model):
    """ Catalog's SmartPractice advertise products in
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CatalogIssue(models.Model):
    """ An Issue of a Catalog
    """
    catalog = models.ForeignKey(Catalog, related_name='issues')
    products = models.ManyToManyField(Product, related_name='catalog_issues', through='CatalogIssueProduct')
    issue = models.CharField(max_length=80)

    def __unicode__(self):
        return '%s / %s' % (self.catalog.name, self.issue)


class CatalogIssueProduct(models.Model):
    """ Product advertised in specific issue of a catalog
    """
    catalog_issue = models.ForeignKey(CatalogIssue)
    product = models.ForeignKey(Product, related_name='catalog_links')

    page_ref = models.PositiveSmallIntegerField()
    img_ref = models.PositiveSmallIntegerField()
    sub_ref = models.CharField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return "%s features in Issue %s of Catalog %s on Page %s Reference %s, %s" % (
            self.product,
            self.catalog_issue,
            self.catalog_issue.catalog,
            self.page_ref,
            self.img_ref,
            self.sub_ref)


class PriceLevelGroup(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class RoyaltyGroup(models.Model):
    """ Price Level Group for a PriceLevel; 'AR', 'LI', etc..
    """
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, null=True, blank=True)
    royalty = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class PriceLevel(models.Model):
    """ Price Level for a Product; products can have multiple price levels
    """
    products = models.ManyToManyField(Product, related_name='price_levels')
    price_level_group = models.ForeignKey(PriceLevelGroup, related_name='price_levels', null=True, blank=True)
    min_amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(blank=True, null=True)
    cost_per_item = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Level #%s' % self.pk

    class Meta:
        ordering = ('-min_amount',)


class Order(models.Model):
    """ Order placed by a Customer for Product(s) sold by SmartPractice
    """
    customer = models.ForeignKey(Customer, related_name='orders')
    products = models.ManyToManyField(Product, related_name='+', through='OrderProduct')
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # total net_cost + shipping_cost
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # total net_price + shipping_cost

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
    notes = models.ManyToManyField('Note', related_name='o_notes')
    last_read = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    @property
    def order_date_str(self):
        return '%s' % self.order_date.strftime("%Y-%m-%d")

    @property
    def order_month_str(self):
        return '%s' % self.order_date.strftime("%Y-%m")

    @property
    def last_invoice(self):
        return self.invoices.order_by('-timestamp')[0] if self.invoices.count() else None

    @property
    def last_status(self):
        return self.statuses.order_by('-timestamp')[0] if self.statuses.count() else None

    def __unicode__(self):
        return 'Order %s' % self.pk

    @property
    def summary(self):
        data = {
            'discount': Decimal(0),
            'tax': Decimal(0),
            'sub_cost': Decimal(0),
            'sub_price': Decimal(0),
            'sub_profit': Decimal(0),
            'gross_cost': Decimal(0),
            'gross_price': Decimal(0),
            'gross_profit': Decimal(0),
            'net_cost': Decimal(0),
            'net_price': Decimal(0),
            'net_profit': Decimal(0),
        }

        for order_product in self.ordered_products.all():
            data['discount'] += order_product.discount_sum
            data['tax'] += order_product.tax_sum
            data['sub_cost'] += order_product.sub_cost
            data['sub_price'] += order_product.sub_price
            data['sub_profit'] += order_product.sub_profit
            data['gross_cost'] += order_product.gross_cost
            data['gross_price'] += order_product.gross_price
            data['gross_profit'] += order_product.gross_profit
            data['net_cost'] += order_product.net_cost
            data['net_price'] += order_product.net_price
            data['net_profit'] += order_product.net_profit

        return data

    def total_recount(self, save=False):
        data = self.summary
        self.total_price = float(data['net_price']) + float(self.shipping_cost)
        self.total_cost = float(data['net_cost']) + float(self.shipping_cost)

        if save:
            self.save(total_recount=False)

    def save(self, total_recount=True, *args, **kwargs):
        if total_recount:
            self.total_recount(save=False)
        super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-order_date',)


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
    STATUSES = [x[0] for x in ORDER_STATUS_CHOICES]

    order = models.ForeignKey(Order, related_name='statuses')
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=PROCESSING)
    notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.order, self.status)

    def save(self, *args, **kwargs):
        super(OrderStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-timestamp',)


class OrderProduct(models.Model):
    """ 'Line Item' for an order; contains Product ordered on an Order with its quantity
    """
    order = models.ForeignKey(Order, related_name='ordered_products')
    product = models.ForeignKey(Product, related_name='ordered_list')
    quantity = models.PositiveSmallIntegerField()
    last_quantity = models.PositiveSmallIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    unit_tax = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    with_tax = models.BooleanField(default=False)

    class Meta:
        ordering = ('product__code',)

    def __unicode__(self):
        return '%s %s' % (self.order, self.product)

    def stock_update(self, quantity=None):
        if quantity is None:
            quantity = self.quantity

        if self.last_quantity != quantity:
            bo_query = self.back_orders.filter(complete=False)
            delta = quantity - self.last_quantity
            if delta > 0:  # ordered more
                if delta > self.product.current_stock:
                    bo_amount = delta - self.product.current_stock
                    self.product.current_stock = 0

                    # Create BackOrder
                    if bo_query.exists():
                        bo_query.update(amount=models.F('amount')+bo_amount)  # must be only one!
                    else:
                        self.back_orders.create(amount=bo_amount)
                else:
                    self.product.current_stock -= delta
            else:  # ordered less
                delta *= -1  # delta -50 => 50
                if bo_query.exists():
                    bo = bo_query.get()
                    delta_with_bo = bo.amount - delta
                    if delta_with_bo > 0:
                        bo.amount = delta_with_bo
                        bo.save()
                    else:
                        bo.delete()
                        self.product.current_stock -= delta_with_bo
                else:
                    self.product.current_stock += delta

            self.product.save()
            self.last_quantity = quantity

    def save(self, *args, **kwargs):
        if self.pk:
            q = 0 if self.order.last_status.status == OrderStatus.CANCELLED else None
            self.stock_update(quantity=q)
            self.back_order = True if self.back_orders.exists() else False
        super(OrderProduct, self).save(*args, **kwargs)

    def delete(self, using=None):
        self.stock_update(quantity=0)
        super(OrderProduct, self).delete(using)

    @property
    def order_date_str(self):
        return self.order.order_date_str

    @property
    def order_month_str(self):
        return self.order.order_month_str

    @property
    def supplier(self):
        return self.product.supplier.code

    @property
    def cost(self):
        try:
            return self.product.sp_cost * self.quantity
        except TypeError:
            return 0

    @property
    def price(self):
        try:
            return self.unit_price * self.quantity
        except TypeError:
            return 0

    @property
    def profit(self):
        return self.price - self.cost

    #  Sub is the basic cost (include royalty)
    @property
    def sub_cost(self):
        return self.cost

    @property
    def sub_price(self):
        return self.price * (1 + Decimal(self.product.royalty)/100)

    @property
    def sub_profit(self):
        return self.sub_price - self.sub_cost

    #  Gross - including discount
    @property
    def discount_sum(self):
        return self.price * self.discount_percentage / 100

    @property
    def gross_cost(self):
        return self.sub_cost

    @property
    def gross_price(self):
        return self.sub_price - self.discount_sum

    @property
    def gross_profit(self):
        return self.gross_price - self.gross_cost

    #  NET - including TAX
    @property
    def tax_sum(self):
        if self.with_tax:
            return self.sub_price * settings.TAX_PERCENT / 100
        return Decimal(0)

    @property
    def net_cost(self):
        return self.gross_cost + self.tax_sum
        ''' Stevo, maybe we should take TAX from cost (not price)?
        def cost_tax_sum(self):
            if self.with_tax:
                return self.gross_cost * settings.TAX_PERCENT / 100
            return 0.00

        return self.gross_cost + self.cost_tax_sum()
        '''

    @property
    def net_price(self):
        return self.gross_price + self.tax_sum

    @property
    def net_profit(self):
        return self.net_price - self.net_cost


class Company(models.Model):
    """ The various companies SmartPractice trade as; 'CAA' 'SP' etc
    """
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25)
    registration = models.CharField(max_length=100)
    logo_img = models.ImageField(upload_to='company_logos', max_length=255, height_field='logo_height', width_field='logo_width', null=True)
    logo_height = models.PositiveSmallIntegerField(null=True)
    logo_width = models.PositiveSmallIntegerField(null=True)
    pobox = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    default_invoice = models.ForeignKey('Document', null=True, blank=True, related_name='default_invoices')
    default_packing_slip = models.ForeignKey('Document', null=True, blank=True, related_name='default_packing_slip')

    def __unicode__(self):
        return self.name


class Invoice(models.Model):
    """ An Invoice for an Order issued by a particular Company that SmartPractices trades as
    """
    order = models.ForeignKey(Order, related_name='invoices')
    company = models.ForeignKey(Company, related_name='+')
    number = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=datetime.now, auto_now_add=True)

    def __unicode__(self):
        return 'Order %s; Number: %s' % (self.order, self.number)


class Note(models.Model):
    text = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s...' % self.text[:30]


class BackOrder(models.Model):
    product = models.ForeignKey('Product', related_name='back_orders')
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    customer = models.ForeignKey('Customer', related_name='back_orders')
    from_borders_fakeid = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-timestamp',)


class StockAdjust(models.Model):
    R_NEW, R_ERROR, R_TAKE = range(3)
    REASONS = (
        (R_NEW, 'New stock'),
        (R_ERROR, 'Stock Error'),
        (R_TAKE, 'Stock take')
    )

    product = models.ForeignKey('Product', related_name='stock_adjust')
    current_amount = models.IntegerField()
    added_amount = models.IntegerField()
    #user = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.PositiveSmallIntegerField(choices=REASONS)

    def __unicode__(self):
        return '%s added %s' % (self.product, self.added_amount)

    def save(self, *args, **kwargs):
        created = False if self.pk else True
        super(StockAdjust, self).save(*args, **kwargs)

        if created:
            self.product.current_stock += self.added_amount
            self.product.save()


    class Meta:
        ordering = ('-timestamp', )


class Document(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    dt = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, null=True, upload_to='documents')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-dt',)
