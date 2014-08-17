#!/usr/bin/env python
import os, sys, tty, re, collections, termios, pickle, decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "sp_migrate.settings")
import django
from django.db import transaction
from django.db.models import Q
from datetime import *

# SmartData + SmartProg database to import data from
SOURCE_DB='source_new_db'
# Hunter DB, currently unprocessed...
HUNTER_DB='hunter_new_db'
# TargetDB - our sane models
TARGET_DB='target_db'

GST_PERCENTAGE = 10.0
GST_STARTED_DATE = datetime.strptime('1/07/00', "%d/%m/%y")

# source table Company contains our Customer's and CustomerContact's
from source.models import SourceCompany # renamed to SourceCompany to not collide with our target Company
from target.models import Customer, CustomerContact

# Column name mappings
#                      target_col   : <source_col|[source_col1, source_col2, ...]>
COMPANY_TABLE_MAP = { 'name' : 'company_name',
                      'customer_type' : 'type',
                      'address_line_1' : 'address_1',
                      'address_line_2' : 'address_2',
                      'suburb' : 'suburb',
                      'state' : 'state',
                      'postcode' : 'post_code',
                      'telephone' : 'telephone',
                      'fax' : 'fax',
                      'email' : 'email',
                      'delivery_attn' : 'att',
                      'delivery_address_line_1' : 'del_address_1',
                      'delivery_address_line_2' : 'del_address_2',
                      'delivery_suburb' : 'del_suburb',
                      'delivery_state' : 'del_state',
                      'delivery_postcode' : 'del_post_code',
                      'from_src_company_id' : 'company_id' }

PRIMARY_CONTACT_MAP = { 'first_name' : 'contact_first_name',
                        'surname' : 'contact_last_name' }

SECONDARY_CONTACT_MAP = { 'first_name' : 'contact_2_first_name',
                          'surname' : 'contact_2_last_name' }

# source table Membadd contains our Customer's and CustomerContacts...
from source.models import Membadd
#               target_col   : <source_col|[source_col1, source_col2, ...]>
MEMBADD_MAP = { 'from_src_membadd_id': 'company_id',
                'name' : 'company_name',
                'customer_type' : 'type',
                'address_line_1' : 'address_1',
                'address_line_2' : 'address_2',
                'suburb' : 'suburb',
                'state' : 'state',
                'postcode' : 'post_code',
                'delivery_attn' : ['prefix', 'given', 'family'],
                'delivery_address_line_1' : 'address_1',
                'delivery_address_line_2' : 'address_2',
                'delivery_suburb' : 'suburb',
                'delivery_state' : 'state',
                'delivery_postcode' : 'post_code' }

MEMBADD_CONTACT_MAP = { 'surname' : 'family',
                        'first_name' : ['prefix', 'given'] }


# source table SourcePriceLevel contains our PriceLevelGroup's ('AR', 'LI', etc)
from source.models import SourcePriceLevel
from target.models import PriceLevelGroup
# Source table CardDetails contains our Product's, Stock contains stock for products
from source.models import CardDetails, Stock
from target.models import Product, Size, Medium, PriceLevel, RoyaltyGroup, Supplier
# Source table SpCatalogue2000 contains PageNo for where a Product is located in a Catalog
from source.models import SpCatalogue2000
# PageNo etc will be imported into our Catalog, CatalogIssue and CatalogIssueProduct models
from target.models import Catalog, CatalogIssue, CatalogIssueProduct

CARDDETAILS_MAP = { 'code' : 'product_code',
                    'name' : 'product_description',
                    'type' : 'type',
                    'description' : 'product_description',
                    'message' : 'message',
                    'notes' : 'note',
                    'sp_cost' : 'cost_price_ea' }

CARDDETAILS_STOCK_MAP = { 'current_stock' : 'qty',
                          'minimum_stock' : 'minimum_stock' }

# source table Orders contains 'recentish' orders, with their details in 'Order Details'
# source table Order History contains 'older' orders, with their details in 'Details History'
from source.models import Orders, OrderDetails, OrderHistory, DetailsHistory, Ro2
from target.models import Order, OrderStatus, OrderProduct, Company, Invoice
# From source table 'Orders'/'Order History'
#  'Net Value': will hold cost for Customer less any discount
ORDERS_TABLEMAP = { 'from_src_order_id': 'order_id',
                    'order_date' : 'date',
                    'wanted_by' : 'date',
                    #'sub_total' : '',  Set to Invoice Total - Delivery Charge
                    'shipping_cost' : 'delivery_charge',
                    'total_cost' : 'invoice_total',
                    'sp_cost' : 'order_cost',
                    'order_notes' : 'notes' }

# this maps from a Found Target Customer from a Source Order to fields in the Target Order table.
#                            <target:Order field> : <target:Customer field>
FOUND_CUSTOMER_ORDER_MAP = { 'invoice_company_name' : 'name',
                             'invoice_company_reg' : 'registration',
                             'invoice_address_line_1' : 'address_line_1',
                             'invoice_address_line_2' : 'address_line_2',
                             'invoice_suburb' : 'suburb',
                             'invoice_state' : 'state',
                             'invoice_postcode' : 'postcode',
                             'invoice_country' : 'country',
                             'shipping_attn' : 'delivery_attn',
                             'shipping_address_line_1' : 'delivery_address_line_1',
                             'shipping_address_line_2' : 'delivery_address_line_2',
                             'shipping_suburb' : 'delivery_suburb',
                             'shipping_state' : 'delivery_state',
                             'shipping_postcode' : 'delivery_postcode',
                             'shipping_country' : 'delivery_country' }

# maps source 'Order Details' and 'Details History' table to target OrderProduct
ORDERDETAILS_TABLEMAP = { 'quantity' : 'qty_out',
                          'unit_price' : 'price_each',
                          'sp_price' : 'cost_ea',
                          'discount_percentage' : 'disc_p',
                          'discount_price' : 'disc_d',
                          'royalty_amount' : 'royalty' }

# source table Borders contains Back ORDERS
from source.models import Borders
# we will import Back Orders as Standard Orders with the OrderProduct.back_order = true
BORDERS_TABLEMAP = { 'from_borders_fakeid': 'fakeid' }
# Source Borders does not contain 'royalty' cost
BORDERS_DETAIL_TABLEMAP = { 'amount' : 'back_order_qty' }


from target.models import ImportNote

"""   'SourceModel' : {
        'pk_field' : 'identifying_column_for_this_insane_db_table',   hence 'pk_field' is not really primary key..
        'TargetModel' : ['SourceModel.src_field', 'SourceModel.src_field_2', ...],
        'TargetModel2' : ['SourceModel.src_field', ... ],
        ...
      },
"""
IMPORTNOTE_TABLEMAP = {
    'CardDetails' : {
        'pk_field' : 'product_code',
        'Medium' : ['size', 'type'],
        'Size' : ['size'],
        'PriceLevel' : []
     }
}

def add_import_match_detail(matched_target_model, from_src_model, from_src_field=None, extra_note=None):
    src_model_name = from_src_model.__class__.__name__
    matched_target_model_name = matched_target_model.__class__.__name__
    if not src_model_name in IMPORTNOTE_TABLEMAP or not matched_target_model_name in IMPORTNOTE_TABLEMAP[src_model_name]:
        if not src_model_name in IMPORTNOTE_TABLEMAP:
            print 'ERROR!! You asked me for the location of a source row from a source model you neglected to give me the details to, pretty poor form.'
            print 'Cant find', model_name, 'in IMPORTNOTE_TABLEMAP'
        else:
            print 'ERROR!! You asked me for the source data from', src_model_name, 'which matched the target model', matched_target_model_name
            print 'But', matched_target_model_name, 'is not in IMPORTNOTE_TABLEMAP[' + src_model_name + ']; Fix it!'

        print 'Source', src_model_name + ':', inspect_model_obj(from_src_model)
        print 'Matched Target', matched_target_model_name + ':', inspect_model_obj(matched_target_model)
        print 'IMPORTNOTE_TABLEMAP is broken, bailing out'
        sys.exit(1)

    src_id_field = IMPORTNOTE_TABLEMAP[src_model_name]['pk_field']
    src_id_value = getattr(from_src_model, src_id_field)

    src_data = []
    if from_src_field:
        if hasattr(from_src_field, '__iter__'):
            for src_field in from_src_field:
                src_data.append(repr(src_field) + ': ' + repr(getattr(from_src_model, src_field)))
        else:
            src_data.append(repr(from_src_field) + ': ' + repr(getattr(from_src_model, from_src_field)))
    else:
        for src_field in IMPORTNOTE_TABLEMAP[src_model_name][matched_target_model_name]:
            src_data.append(repr(src_field) + ': ' + repr(getattr(from_src_model, src_field)))

    source_data = '{' + ', '.join(src_data) + '}'
    note_detail = { 'model': matched_target_model.__class__.__name__, 'model_id': matched_target_model.id, 'type': 'MATCH', 'text': source_data, 'src_model': src_model_name, 'src_model_id_field': src_id_field, 'src_model_id_text': src_id_value, 'note': extra_note}
    import_note = ImportNote(**note_detail)
    import_note.save(using=TARGET_DB)

#### Functions to convert source tables Company and Membadd into target tables Customer and CustomerContact
def convert_source_company_and_membadd():
    #SRC_TABLES = [ SourceCompany, Membadd ]
    #SRC_TABLES = [ Membadd, SourceCompany ]
    SRC_TABLES = [ SourceCompany ]
    use_saved_choices = None
    while use_saved_choices != 'y' and use_saved_choices != 'n':
        print 'Do you want to automatically use the last saved choice to handle duplicate company records? (y/n)'
        use_saved_choices = get_char()

    PREVIOUS_COMPANY_CHOICES = None

    if use_saved_choices == 'y' or use_saved_choices == 'Y':
        PREVIOUS_COMPANY_CHOICES = load_previous_duplicate_record_choices('company.pkl')

    if not PREVIOUS_COMPANY_CHOICES:
        PREVIOUS_COMPANY_CHOICES = { }

    CURRENT_COMPANY_CHOICES = { }

    for src_table in SRC_TABLES:
        created_customers, failed_customers = 0, 0
        created_customer_contacts, failed_customer_contacts = 0, 0
        auto_duplicate_resolves, manual_duplicate_resolves = 0, 0
        processed_records, skipped_records = 0, 0
        src_table_name = None

        for src_customer in src_table.objects.using(SOURCE_DB).all():
            if not src_table_name:
                src_table_name = src_customer.__class__.__name__

            print "--------------------------------------------------------------------------------------------------------"
            print "Found source", src_table_name, ':', inspect_model_obj(src_customer), "\n"

            customer = Customer(registration='<UNKNOWN>')
            primary_contact = None
            secondary_contact = None

            if src_table_name == 'SourceCompany':
                dictionary_table_merge(COMPANY_TABLE_MAP, src_customer, customer)
                
                if src_customer.contact_first_name or src_customer.contact_last_name:
                    primary_contact = CustomerContact(phone=customer.telephone, email=customer.email)
                    dictionary_table_merge(PRIMARY_CONTACT_MAP, src_customer, primary_contact)

                if src_customer.contact_2_first_name or src_customer.contact_2_last_name:
                    secondary_contact = CustomerContact(phone=customer.telephone, email=customer.email)
                    dictionary_table_merge(SECONDARY_CONTACT_MAP, src_customer, secondary_contact)
            elif src_table_name == 'Membadd':
                customer.email=''
                dictionary_table_merge(MEMBADD_MAP, src_customer, customer)

                if src_customer.family or src_customer.given:
                    primary_contact = CustomerContact()
                    dictionary_table_merge(MEMBADD_CONTACT_MAP, src_customer, primary_contact)
            else:
                print 'Something crazy is going on, found a model class name I wasnt expecting:', src_table_name
                print 'Bailing Out'
                sys.exit(1)

            customer.set_slug()
            customer_exists = Customer.objects.using(TARGET_DB).filter(Q(from_src_company_id=src_customer.company_id) | Q(from_src_membadd_id=src_customer.company_id))
            if customer_exists.count() > 0:
                found_duplicate_customer = False
                for existing_customer in customer_exists:
                    manually_resolved_duplicate = False
                    customer_details_map = { 'existing' : existing_customer,
                                             'new' : customer,
                                             'new_primary' : primary_contact,
                                             'new_secondary' : secondary_contact,
                                             'new_src_table' : src_table_name }
                    if same_customer_details(customer_details_map):
                        print "Found existing Customer: " + inspect_model_obj(existing_customer) + "\n"
                        print "Existing CustomerContacts: " + inspect_model_collection(existing_customer.contacts.all()) + "\n"
                        print "Skipping", src_table_name
                        print "--------------------------------------------------------------------------------------------------------\n\n"
                        skipped_records += 1
                        found_duplicate_customer = True
                        if src_customer.company_id in CURRENT_COMPANY_CHOICES:
                            CURRENT_COMPANY_CHOICES[src_customer.company_id][src_table_name] = False
                        else:
                            CURRENT_COMPANY_CHOICES[src_customer.company_id] = { src_table_name : False }

                        if existing_customer.from_src_company_id:
                            CURRENT_COMPANY_CHOICES[src_customer.company_id]['SourceCompany'] = True
                        elif existing_customer.from_src_membadd_id:
                            CURRENT_COMPANY_CHOICES[src_customer.company_id]['Membadd'] = True
                        else:
                            print 'Unable to determine existing customer import from table! ExistingCustomer:', inspect_model_obj(existing_customer)
                            print 'Cannot set CURRENT_COMPANY_CHOICES[' + str(src_customer.company_id) + ']'
                            pause_terminal()
                        break
                    else:
                        # if it contains deleted, choose 'other record'
                        if src_customer.company_id in PREVIOUS_COMPANY_CHOICES and src_table_name in PREVIOUS_COMPANY_CHOICES[src_customer.company_id]: # automatic duplicate resolution...
                            auto_duplicate_resolves += 1
                            if src_customer.company_id in CURRENT_COMPANY_CHOICES:
                                CURRENT_COMPANY_CHOICES[src_customer.company_id][src_table_name] = PREVIOUS_COMPANY_CHOICES[src_customer.company_id][src_table_name]
                            else:
                                CURRENT_COMPANY_CHOICES[src_customer.company_id] = { src_table_name : PREVIOUS_COMPANY_CHOICES[src_customer.company_id][src_table_name] }
                            
                            if PREVIOUS_COMPANY_CHOICES[src_customer.company_id][src_table_name]:
                                # Want to import 'this' customer. break out of loop and save customer. (if not customer.id will evaluate true, and then save customer)
                                break
                            else:
                                # Want to ignore 'this' customer
                                skipped_records += 1
                                found_duplicate_customer = True # this is to continue outer for loop
                                break
                        else: # manual duplicate resolution
                            created_customer, failed_customer, created_primary_contact, failed_primary_contact, created_secondary_contact, failed_secondary_contact = handle_mismatched_customer_records(customer_details_map, CURRENT_COMPANY_CHOICES)
                            manually_resolved_duplicate = True
                            manual_duplicate_resolves += 1
                            if created_customer or failed_customer:
                                processed_records += 1
                            if not created_customer and not failed_customer:
                                skipped_records += 1

                            if created_customer:
                                created_customers += 1
                            if failed_customer:
                                failed_customers += 1
                            if created_primary_contact:
                                created_customer_contacts += 1
                            if failed_primary_contact:
                                failed_customer_contacts += 1
                            if created_secondary_contact:
                                created_customer_contacts += 1
                            if failed_secondary_contact:
                                failed_customer_contacts += 1

                if found_duplicate_customer or manually_resolved_duplicate:
                    continue

            if not customer.id:
                processed_records += 1
                if save_model_obj(customer):
                    created_customers += 1
                    if primary_contact:
                        primary_contact.customer = customer
                        if save_model_obj(primary_contact):
                            created_customer_contacts += 1
                        else:
                            failed_customer_contacts += 1

                    if secondary_contact:
                        secondary_contact.customer = customer
                        if save_model_obj(secondary_contact):
                            created_customer_contacts += 1
                        else:
                            failed_customer_contacts += 1

                    if src_customer.company_id in CURRENT_COMPANY_CHOICES:
                        CURRENT_COMPANY_CHOICES[src_customer.company_id][src_table_name] = True
                    else:
                        CURRENT_COMPANY_CHOICES[src_customer.company_id] = { src_table_name : True }
                else:
                    failed_customers += 1
                    continue

            if customer.id:
                print "--------------------------------------------------------------------------------------------------------"
                print "customer.contacts collection: " + inspect_model_collection(customer.contacts.all())
                print "--------------------------------------------------------------------------------------------------------\n\n"

        source_stats = { 'table': src_table_name,
                         'records': src_table.objects.using(SOURCE_DB).all().count(),
                         'processed': processed_records,
                         'skipped': skipped_records }

        target_stats = [ ('Customer', created_customers, failed_customers),
                         ('CustomerContact', created_customer_contacts, failed_customer_contacts) ]

        duplicate_stats = { 'auto' : auto_duplicate_resolves,
                            'manual' : manual_duplicate_resolves }

        print_convert_stats(source_stats, target_stats, duplicate_stats)

    store_duplicate_record_choices('company.pkl', CURRENT_COMPANY_CHOICES)

def handle_mismatched_customer_records(customer_details_map, CURRENT_COMPANY_CHOICES):
    created_customer = failed_customer = False
    created_primary_contact = failed_primary_contact = False
    created_secondary_contact = failed_secondary_contact = False

    print 'Existing Customer:', inspect_model_obj(customer_details_map['existing'])
    print 'Existing CustomerContact:', inspect_model_collection(customer_details_map['existing'].contacts.all())
    print 'New Customer:', inspect_model_obj(customer_details_map['new'])
    if customer_details_map['new_primary']:
        print 'New Customer Primary Contact:', inspect_model_obj(customer_details_map['new_primary'])
    if customer_details_map['new_secondary']:
        print 'New Customer Secondary Contact:', inspect_model_obj(customer_details_map['new_secondary'])

    choice = None
    while choice != 'k' and choice != 'd' and choice != 'i':
        print '\nWhat do you want to do?  K = Keep Existing Contact, Ignore New Customer.  D = Delete Existing Contact, Import New Customer.  I = Import New Customer, Leave/Ignore Existing Customer.'
        print '(k/d/i) ?'
        choice = get_char()

    if customer_details_map['existing'].from_src_company_id:
        existing_table = 'SourceCompany'
        src_company_id = customer_details_map['existing'].from_src_company_id
    elif customer_details_map['existing'].from_src_membadd_id:
        existing_table = 'Membadd'
        src_company_id = customer_details_map['existing'].from_src_membadd_id
    else:
        print 'Could not determine existing customer import table! Existing Customer:', inspect_model_obj(customer_details_map['existing'])
        pause_terminal()

    if not src_company_id in CURRENT_COMPANY_CHOICES:
        CURRENT_COMPANY_CHOICES[src_company_id] = { }

    if choice == 'k' or choice == 'K':
        # Keep existing customer, ignore new customer
        CURRENT_COMPANY_CHOICES[src_company_id][existing_table] = True
        CURRENT_COMPANY_CHOICES[src_company_id][customer_details_map['new_src_table']] = False

    if choice == 'd' or choice == 'D':
        # Delete Existing Contact, Import New Customer
        CURRENT_COMPANY_CHOICES[src_company_id][existing_table] = False
        CURRENT_COMPANY_CHOICES[src_company_id][customer_details_map['new_src_table']] = True
        print 'Deleting Existing Customer CustomerContact(s):', inspect_model_collection(customer_details_map['existing'].contacts.all())
        for existing_customer_contact in customer_details_map['existing'].contacts.all():
            existing_customer_contact.delete()
        print 'Deleting Existing Customer:', inspect_model_obj(customer_details_map['existing'])
        customer_details_map['existing'].delete()

    if choice == 'd' or choice == 'D' or choice == 'i' or choice == 'I':
        # Import New Customer ('d' is same logic apart from deleting existing)
        CURRENT_COMPANY_CHOICES[src_company_id][customer_details_map['new_src_table']] = True
        if choice == 'i' or choice == 'I':
            CURRENT_COMPANY_CHOICES[src_company_id][existing_table] = True

        if save_model_obj(customer_details_map['new']):
            created_customer = True
            if customer_details_map['new_primary']:
                customer_details_map['new_primary'].customer = customer_details_map['new']
                if save_model_obj(customer_details_map['new_primary']):
                    created_primary_contact = True
                else:
                    failed_primary_contact = True

            if customer_details_map['new_secondary']:
                customer_details_map['new_secondary'].customer = customer_details_map['new']
                if save_model_obj(customer_details_map['new_secondary']):
                    created_secondary_contact = True
                else:
                    failed_secondary_contact = True
        else:
            failed_customer = True

    return created_customer, failed_customer, created_primary_contact, failed_primary_contact, created_secondary_contact, failed_secondary_contact

def same_customer_details(customer_details_map):
    CUSTOMER_COMPARE_COLS = [ 'name', 'customer_type', 'address_line_1', 'address_line_2', 'suburb', 'state', 'postcode', 'country', 'telephone', 'fax', 'email',
                              'delivery_attn', 'delivery_address_line_1', 'delivery_address_line_2', 'delivery_suburb', 'delivery_state', 'delivery_postcode', 'delivery_country' ]

    CUSTOMERCONTACT_COMPARE_COLS = [ 'first_name', 'surname', 'phone', 'email' ]

    same_customer_details = True
    for column in CUSTOMER_COMPARE_COLS:
        if str(getattr(customer_details_map['existing'], column)) != str(getattr(customer_details_map['new'], column)):
            print 'Existing Customer Record Mismatch! Existing Customer ID', customer_details_map['existing'].id, column, '=', getattr(customer_details_map['existing'], column), '||', 'New Customer Record', column, '=', getattr(customer_details_map['new'], column)
            same_customer_details = False

    existing_contacts = customer_details_map['existing'].contacts.count()
    new_contacts = 0
    if customer_details_map['new_primary']:
        new_contacts += 1
    if customer_details_map['new_secondary']:
        new_contacts += 1

    customer_details_map['new_customercontacts'] = new_contacts

    if new_contacts != 0 or existing_contacts != 0:
        if new_contacts != existing_contacts:
            print_customercontact_mismatch(customer_details_map)
            return False
        else:
            # Number of CustomerContacts matches..
            found_primary_contact = { 'first_name' : False, 'surname' : False, 'phone' : False, 'email' : False }
            found_secondary_contact = { 'first_name' : False, 'surname' : False, 'phone' : False, 'email' : False }
            for existing_contact in customer_details_map['existing'].contacts.all():
                for column in CUSTOMERCONTACT_COMPARE_COLS:
                    if customer_details_map['new_primary'] and str(getattr(existing_contact, column)) == str(getattr(customer_details_map['new_primary'], column)):
                        found_primary_contact[column] = True
                    if customer_details_map['new_secondary'] and str(getattr(existing_contact, column)) == str(getattr(customer_details_map['new_secondary'], column)):
                        found_secondary_contact[column] = True

            customer_details_map['found_primary'] = found_primary_contact
            customer_details_map['found_secondary'] = found_secondary_contact

            if new_contacts == 2: # primary & secondary
                for column in CUSTOMERCONTACT_COMPARE_COLS:
                    if not found_primary_contact[column] or not found_secondary_contact[column]:
                        customer_details_map['column'] = column
                        print_customercontact_mismatch(customer_details_map)
                        return False
            elif new_contacts == 1: # one of primary or secondary
                for column in CUSTOMERCONTACT_COMPARE_COLS:
                    if (customer_details_map['new_primary'] and not found_primary_contact[column]) or (customer_details_map['new_secondary'] and not found_secondary_contact[column]):
                         customer_details_map['column'] = column
                         print_customercontact_mismatch(customer_details_map)
                         return False
            else:
                print 'Something crazy is going on, new_contacts is not 2 or 1 and apparently not 0 either!?!? new_contacts:', new_contacts, 'existing_contacts:', existing_contacts
                print 'This shouldnt happen... Bailing Out'
                sys.exit(1)
    else: # both existing, and new customer objects have no related CustomerContact(s)
        pass

    return same_customer_details # True / False depending on match of Customer object; CustomerContacts we're OK/Matched

def print_customercontact_mismatch(customer_details_map):
    if 'column' in customer_details_map:
        column = ' on Field: ' + customer_details_map['column']
    else:
        column = ''
    print 'Existing Customer CustomerContact Record Mismatch!', column, 'Existing Customer ID', customer_details_map['existing'].id, 'has', customer_details_map['existing'].contacts.count(), 'CustomerContact Records'
    print 'New Customer has', customer_details_map['new_customercontacts'], 'CustomerContact Records'
    print 'Existing Customer CustomerContacts:', inspect_model_collection(customer_details_map['existing'].contacts.all())
    if customer_details_map['new_primary']:
        print 'New Customer primary CustomerContact:', inspect_model_obj(customer_details_map['new_primary'])
    if 'found_primary' in customer_details_map:
        print 'FoundPrimaryContact:', customer_details_map['found_primary']
    if customer_details_map['new_secondary']:
        print 'New Customer secondary CustomerContact:', inspect_model_obj(customer_details_map['new_secondary'])
    if 'found_secondary' in customer_details_map:
        print 'FoundSecondaryContact:', customer_details_map['found_secondary']

###### END

##### FUNCTIONS to convert source tables CardDetails and Stock into target tables Product, PriceLevel, Medium and Size
def convert_source_carddetails():
    created_products, failed_products = 0, 0
    created_sizes, failed_sizes = 0, 0
    created_mediums, failed_mediums = 0, 0
    created_price_levels, failed_price_levels = 0, 0
    created_price_level_groups, failed_price_level_groups = 0, 0
    created_royalty_imgs, failed_royalty_imgs = 0, 0
    created_suppliers, failed_suppliers = 0, 0
    created_catalogs, failed_catalogs = 0, 0
    created_catalog_issues, failed_catalog_issues = 0, 0
    created_catalog_issue_products, failed_catalog_issue_products = 0, 0
    processed_records, skipped_records = 0, 0

    sanitize_mediums_dict()

    UNKNOWN_SUPPLIER_NAME = 'Unknown Supplier Name'
    # 'Supplier Code' : { 'name' : 'Name Of Supplier', 'word' : ['list', 'of', 'words'], 're' : ['listof', 'res'] },
    SUPPLIERS_MAP = { 'AMI' : { 'name' : 'Activator Methods International Ltd', 'word' : ['AMI'], 're' : [] },
                      'BT' : { 'name' : 'Back Talk Systems Inc', 'word' : ['BT'], 're' : [] },
                      'CAA' : { 'name' : 'Chiropractors Association of Australia', 'word' : ['CAA'], 're' : [] },
                      'Koren 1' : { 'name' : 'Koren Publications 1', 'word' : ['Korean 1'], 're' : [] },
                      'Koren 2' : { 'name' : 'Koren Publications 2', 'word' : [], 're' : ['[Kk]oren\s{1}2'] },
                      'LT' : { 'name' : 'Looney Tunes', 'word' : ['LT'], 're' : [] },
                      'SP' : { 'name' : 'Smart Practice', 'word' : ['SP', 'sP', 'Sp', 'sp'], 're' : [] },
                      'JH' : { 'name' : 'Disney', 'word' : ['JH'], 're' : [] }, # JH = Jim Hensen, possibly THE HONOURABLE J.H. DISNEY or something entirely different
                      'MedART' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : ['MedART'], 're' : [] },
                      'AIO' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : ['AIO'], 're' : [] },
                      'OLD' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : [], 're' : ['[Oo]L[Dd]'] },
                      'AIOLT' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : ['AIOLT'], 're' : [] },
                      'JP' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : ['JP'], 're' : [] },
                      'SPLT' : { 'name' : UNKNOWN_SUPPLIER_NAME, 'word' : ['SPLT'], 're' : [] } }

    for src_pricelevel in SourcePriceLevel.objects.using(SOURCE_DB).all():
        price_level_group, created_price_level_group, failed_price_level_group = get_or_create_model(PriceLevelGroup, {'name' : src_pricelevel.pricelevel, 'description' : 'Imported PriceLevelGroup ' + src_pricelevel.pricelevel})
        if created_price_level_group:
            created_price_level_groups += 1
        if failed_price_level_group:
            failed_price_level_groups += 1

    for src_carddetail in CardDetails.objects.using(SOURCE_DB).all():
        print "--------------------------------------------------------------------------------------------------------"
        print "Found source CardDetail: " + inspect_model_obj(src_carddetail) + "\n"
        product_exists = Product.objects.using(TARGET_DB).filter(code=src_carddetail.product_code)
        if product_exists.count() > 0:
            print "Found existing Product: " + inspect_model_obj(product_exists[0]) + "\n"
            print "Skipping CardDetail"
            print "--------------------------------------------------------------------------------------------------------\n\n"
            skipped_records += 1
            continue
        else:
            processed_records += 1

        size_medium_match_detail = { 'size' : None, 'medium' : None }
        size, created_size, failed_size, medium, created_medium, failed_medium = determine_product_size_and_medium(src_carddetail.size, src_carddetail.type, size_medium_match_detail)

        if failed_size:
            failed_sizes += 1
            failed_products += 1
            continue
        else:
            add_import_match_detail(size, src_carddetail, size_medium_match_detail['size'])
        if created_size:
            created_sizes += 1

        if failed_medium:
            failed_mediums += 1
            failed_products += 1
            continue
        else:
            add_import_match_detail(medium, src_carddetail, size_medium_match_detail['medium'])
        if created_medium:
            created_mediums += 1

        royalty = None
        if src_carddetail.royaltyfactor:
            royalty_percentage = abs(round((1.0 - src_carddetail.royaltyfactor) * -100.0, 2))
            if royalty_percentage == 0.0:
                royalty_name = 'No Royalty'
            else:
                royalty_name = str(royalty_percentage) + ' Percent'
            royalty_desc = 'Imported from RoyaltyFactor ' + str(src_carddetail.royaltyfactor)
            royalty, created_royalty, failed_royalty = get_or_create_model(RoyaltyGroup, {'name': royalty_name, 'description': royalty_desc, 'royalty' : royalty_percentage})
            if created_royalty:
                created_royalty_imgs += 1
            if failed_royalty:
                failed_royalty_imgs += 1

        supplier = None
        created_supplier = failed_supplier = False
        if src_carddetail.supplier:
            for supplier_code, supplier_details in SUPPLIERS_MAP.iteritems():
                if src_carddetail.supplier in supplier_details['word'] or matches_regex_list(src_carddetail.supplier, supplier_details['re']):
                    supplier, created_supplier, failed_supplier = get_or_create_model(Supplier, {'code' : supplier_code, 'name' : supplier_details['name']})
                    break

        if not supplier:
            supplier, created_supplier, failed_supplier = get_or_create_model(Supplier, {'code' : 'NONE', 'name' : 'Imported Without Supplier'})

        if created_supplier:
            created_suppliers += 1
        if failed_supplier:
            failed_suppliers += 1

        print '---medium:' + inspect_model_obj(medium)
        print '---royalty_group:' + inspect_model_obj(royalty)
        print '--supplier:' + inspect_model_obj(supplier)

        product = Product(medium=medium, royalty_group=royalty, size=size, supplier=supplier)
        dictionary_table_merge(CARDDETAILS_MAP, src_carddetail, product)

        try:
            src_product_stock = Stock.objects.using(SOURCE_DB).filter(product_code=src_carddetail.product_code)[0]
        except IndexError:
            src_product_stock = None

        if src_product_stock:
            dictionary_table_merge(CARDDETAILS_STOCK_MAP, src_product_stock, product)

        if save_model_obj(product):
            created_products += 1
            price_level_group = None

            if src_carddetail.pricelevel:
                price_level_group, created_price_level_group, failed_price_level_group = get_or_create_model(PriceLevelGroup, {'name' : src_carddetail.pricelevel, 'description' : 'Imported PriceLevelGroup ' + src_carddetail.pricelevel})
                if created_price_level_group:
                    created_price_level_groups += 1
                if failed_price_level_group:
                    failed_price_level_groups += 1

            num_created, num_failed = create_product_price_levels(src_carddetail, product, price_level_group)
            created_price_levels += num_created
            failed_price_levels += num_failed

            catalogs_created, catalogs_failed, catalog_issues_created, catalog_issues_failed, catalog_issue_products_created, catalog_issue_products_failed = create_product_catalogs(product)
            created_catalogs += catalogs_created
            failed_catalogs += catalogs_failed
            created_catalog_issues += catalog_issues_created
            failed_catalog_issues += catalog_issues_failed
            created_catalog_issue_products += catalog_issue_products_created
            failed_catalog_issue_products += catalog_issue_products_failed
        else:
            failed_products += 1

    source_stats = { 'table': 'Card Details',
                     'records': CardDetails.objects.using(SOURCE_DB).all().count(),
                     'processed': processed_records,
                     'skipped': skipped_records }

    target_stats = [ ('Product', created_products, failed_products),
                     ('Supplier', created_suppliers, failed_suppliers),
                     ('Size', created_sizes, failed_sizes),
                     ('Medium', created_mediums, failed_mediums),
                     ('RoyaltyGroup', created_royalty_imgs, failed_royalty_imgs),
                     ('PriceLevelGroup', created_price_level_groups, failed_price_level_groups),
                     ('PriceLevel', created_price_levels, failed_price_levels),
                     ('Catalog', created_catalogs, failed_catalogs),
                     ('CatalogIssue', created_catalog_issues, failed_catalog_issues),
                     ('CatalogIssueProduct', created_catalog_issue_products, failed_catalog_issue_products) ]

    print_convert_stats(source_stats, target_stats)

# PageNo Catalogs
# BT = Back Talk
# D = Dental
# K = Koren
# V = Veterinary
# CAA = Chiropractors Assoc...
# O = Optom
# P = Pedo
# AMI = Activator Methods
# C = Chiropractors
def create_product_catalogs(product):
    created_catalogs, failed_catalogs = 0, 0
    created_catalog_issues, failed_catalog_issues = 0, 0
    created_catalog_issue_products, failed_catalog_issue_products = 0, 0

    CATALOG_ISSUE = 'ORiGiNEiL'

    CATALOG_MAP = { 'V' : 'Veterinary',
                    'AMI' : 'Activator Methods International Ltd',
                    'CAA' : 'Chiropractors Association of Australia',
                    'O' : 'Optometry',
                    'D' : 'Dentistry',
                    'BT' : 'Back Talk Systems Inc',
                    'C' : 'Chiropractors',
                    'P' : 'Podiatry',
                    'K' : 'Koren' }

    page_no_re = re.compile('^([^\d\-]{1,})-?([\d]{1,})-([\d]{1,})(.*)$')

    src_catalog_records = SpCatalogue2000.objects.using(SOURCE_DB).filter(prodno=product.code)

    print 'Found', src_catalog_records.count(), 'Source Catalog Records for Product Code', product.code

    for src_catalog in src_catalog_records:
        if src_catalog.page_no:
            print 'Source Catalog Record SpCatalogue2000:', inspect_model_obj(src_catalog)

            page_match = page_no_re.match(src_catalog.page_no)
            if page_match:
                catalog_code = page_match.group(1)
                catalog_page = page_match.group(2)
                catalog_img_ref = page_match.group(3)
                catalog_sub_ref = page_match.group(4)

                if not catalog_code in CATALOG_MAP:
                    print 'Could not find catalog_code:', catalog_code, 'in CATALOG_MAP'
                    print 'CATALOG_MAP:', CATALOG_MAP
                    print 'Source Page No:', src_catalog.page_no, 'Page Match Groups - catalog_code:', catalog_code, 'catalog_page:', catalog_page, 'catalog_img_ref:', catalog_img_ref, 'catalog_sub_ref:', catalog_sub_ref
                    pause_terminal()
                    continue
                else:
                    catalog, created, failed = get_or_create_model(Catalog, {'name': CATALOG_MAP[catalog_code] })
                    if failed:
                        failed_catalogs += 1
                        print 'Could not get or create Catalog:', inspect_model_obj(catalog)
                        print 'Cannot create CatalogIssue or CatalogIssueProduct; skipping Source Catalog Record'
                        pause_terminal()
                        continue

                    if created:
                        created_catalogs += 1

                    catalog_issue, created, failed = get_or_create_model(CatalogIssue, {'catalog' : catalog, 'issue' : CATALOG_ISSUE})
                    if failed:
                        failed_catalog_issues += 1
                        print 'Could not get or create CatalogIssue:', inspect_model_obj(catalog_issue)
                        print 'Cannot create CatalogIssueProduct; skipping to next Source Catalog Record'
                        pause_terminal()
                        continue

                    if created:
                        created_catalog_issues += 1

                    catalog_issue_product, created, failed = get_or_create_model(CatalogIssueProduct, {'catalog_issue': catalog_issue, 'product': product, 'page_ref': catalog_page, 'img_ref': catalog_img_ref, 'sub_ref': catalog_sub_ref})
                    if failed:
                        failed_catalog_issue_products += 1
                        print 'Could not get or create CatalogIssueProduct:', inspect_model_obj(catalog_issue_product)
                        print 'Skipping to next Source Catalog Record'
                        pause_terminal()
                        continue

                    if created:
                        created_catalog_issue_products += 1
            else: # page_match is False
                print 'Could not match catalog page from Source Catalog Record using Page No:', src_catalog.page_no
                print 'Skipping to next Source Catalog Record'
                pause_terminal()
                continue
        else: # src_catalog.page_no is Empty/Null/None
            print 'Source Catalog Record has no Page No! Skipping to next Source Catalog Receord'
            continue

    return created_catalogs, failed_catalogs, created_catalog_issues, failed_catalog_issues, created_catalog_issue_products, failed_catalog_issue_products

NO_MEDIUM = {'name': 'No Medium', 'description': 'Imported Without Medium'}
NO_MATCHED_MEDIUM = {'name': 'Unmatched Medium', 'description': 'Imported With UNMATCHED Medium'}
def determine_product_size_and_medium(src_size, src_type, match_detail):
    NO_SIZE = {'width': None, 'height': None, 'depth': None, 'notes': 'Imported Without Size'}
    NO_MATCHED_SIZE = {'width': None, 'height': None, 'depth': None, 'units': None, 'notes': 'Imported Without a MATCHED Size'}

    # fractional sizes need matching: {'size': u'7/16"x1 3/4"'}  {'size': u'7 1/2 x9'}  {'size': u'1"x1 5/8"'}
    # is this 2.0feet x 2.8feet??? {'size': u'2 0" x  2 8"'}   

    #huh? {'size': u'71/2x9'}  {'size': u'1 x 1 5/"'}  {'size': u'61x51cm/56x61cm'}

    # process both size and type for a medium.
    medium, created_medium, failed_medium = determine_product_medium({'type': src_type, 'size': src_size}, match_detail)

    if not src_size:
        size, created_size, failed_size = get_or_create_model(Size, NO_SIZE)
    else:
        l_w_h_re = re.compile('([\d\.]{1,})["L\s]{1,}[xX][\s]?([\d\.]{1,})["W\s]{1,}[xX][\s]?([\d\.]{1,})[H"c]{1,}')
        width_height_re = re.compile('[\s]{0,}([\d\.]{1,})[\s"\'cms]{0,}[xX][\s]{0,}([\d\.]{1,})[\s"\'Ccms]{0,}(.*)')
        height_re = re.compile('(\d+)[\'"\scm]{0,}(.*)')
        skip_height_re = re.compile('.*([Bb][Rr][Oo][Cc][Hh][Uu][Rr][Ee]|pckt|[Pp]age|[Tt]ape|sheet|/roll|tube|pp|Room|/Pack|X|[Dd]iam|Phase|sizes)s?')
        cm_re = re.compile('.*\d\s?[cC]ms?.*')
        mm_re = re.compile('.*\d\s?mm.*')
        inch_re = re.compile('.*\d\s?("|\'\').*')
        oz_re = re.compile('.*\d\s?[Oo][Zz].*')
        mg_re = re.compile('.*\d\s?[Mm][Gg].*')
        gm_re = re.compile('.*\d\s?gm.*')
        yard_re = re.compile('.*\d\s?[Yy]ards?.*')

        normal_re = re.compile('[Nn]ormal')
        standard_re = re.compile('[Ss]([TtRrd][Ddt]|tanda[rn]d)[\s\.]{0,}(.*)')
        sml_re = re.compile('s,m,l')
        xsmall_re = re.compile('([Xx]|Extra)[\s]{0,}[Ss]mall[\s]{0,}(.*)')
        small_re = re.compile('[Ss][Mm][Aa][Ll][Ll][\s]{0,}(.*)')
        medium_re = re.compile('[Mm][Ee][Dd][Ii][Uu][Mm][\s]{0,}(.*)')
        large_re = re.compile('[Ll][Aa][Rr][Gg][Ee][\s]{0,}(.*)')
        xlarge_re = re.compile('(Extra|[Xx])[\s\-]?[Ll](arge|rg)[\s]{0,}(.*)')
        child_re = re.compile('[Cc]hild')
        adult_re = re.compile('[Aa]dult')

        # sticker sizes/shapes
        stick_rect_re = re.compile('(rectangle|Oblong)')
        stick_square_re = re.compile('Square')
        stick_oval_re = re.compile('Ova[l;]')
        stick_circle_re = re.compile('[Cc]ircle')
        stick_roll_re = re.compile('[Ss]?t?i?c?k?e?r?[\s]?[Rr]olls?[\s]{0,}(.*)')

        comp_form_re = re.compile('Comp([\s]|[ui]ter[\s])[Ff]orm')

        depth = None
        height = None
        width = None
        notes = None
        sub_notes = None

        l_w_h_match = l_w_h_re.match(src_size)
        width_height_match = width_height_re.match(src_size)
        height_match = height_re.match(src_size)
        bad_height_match = skip_height_re.match(src_size)
        
        normal_match = normal_re.match(src_size)
        standard_match = standard_re.match(src_size)
        sml_match = sml_re.match(src_size)
        xsmall_match = xsmall_re.match(src_size)
        small_match = small_re.match(src_size)
        medium_match = medium_re.match(src_size)
        large_match = large_re.match(src_size)
        xlarge_match = xlarge_re.match(src_size)
        child_match = child_re.match(src_size)
        adult_match = adult_re.match(src_size)

        rect_match = stick_rect_re.match(src_size)
        square_match = stick_square_re.match(src_size)
        oval_match = stick_oval_re.match(src_size)
        circle_match = stick_circle_re.match(src_size)
        roll_match = stick_roll_re.match(src_size)

        comp_match = comp_form_re.match(src_size)

        # {'size': u'4-Up   11" x 8.5"'}
        if src_size == u'4-Up   11" x 8.5"':
            width = '11'
            height = '8.5'
            notes = '4-Up'
        # {'size': u'3\xbd" x1"'}
        elif src_size == u'3\xbd" x1"':
            width = '3'
            height = '1'
        # {'size': u'9" x 13" 23 x 33cm'}   <--- matches to CMs but picks up the inch numbers...
        elif src_size == u'9" x 13" 23 x 33cm':
            width = '23'
            height = '33'
        elif normal_match:
            notes = 'Normal'
        elif standard_match:
            notes = 'Standard'
            sub_notes = standard_match.group(2)
        elif sml_match:
            notes = 'Small, Medium and Large'
        elif xsmall_match:
            notes = 'Extra Small'
            sub_notes = xsmall_match.group(2)
        elif small_match:
            notes = 'Small'
            sub_notes = small_match.group(1)
        elif medium_match:
            notes = 'Medium'
            sub_notes = medium_match.group(1)
        elif large_match:
            notes = 'Large'
            sub_notes = large_match.group(1)
        elif xlarge_match:
            notes = 'Extra Large'
            sub_notes = xlarge_match.group(3)
        elif child_match:
            notes = 'Child'
        elif adult_match:
            notes = 'Adult'
        elif rect_match:
            notes = 'Rectangle'
        elif square_match:
            notes = 'Square'
        elif oval_match:
            notes = 'Oval'
        elif circle_match:
            notes = 'Circle'
        elif roll_match:
            notes = 'Roll'
            sub_notes = roll_match.group(1)
        elif comp_match:
            notes = 'Computer Form'
        elif l_w_h_match:
            depth = l_w_h_match.group(1)
            width = l_w_h_match.group(2)
            height = l_w_h_match.group(3)
        elif width_height_match:
            width = width_height_match.group(1)
            height = width_height_match.group(2)
            notes = width_height_match.group(3)
        elif height_match and not bad_height_match and height_match.group(1) != str('0'):
            height = height_match.group(1)
            notes = height_match.group(2)

        if height:
            if cm_re.match(src_size):
                units = 'cm'
            elif mm_re.match(src_size):
                units = 'mm'
            elif inch_re.match(src_size):
                units = 'inch'
            elif oz_re.match(src_size):
                units = 'ounce'
            elif mg_re.match(src_size):
                units = 'mg'
            elif gm_re.match(src_size):
                units = 'gram'
            elif yard_re.match(src_size):
                units = 'yard'
            else:
                units = 'unknown'

            if re.compile('.*Round').match(src_size):
                notes = 'Round'

            size, created_size, failed_size = get_or_create_model(Size, {'depth': depth, 'width':width, 'height':height, 'units': units, 'notes': notes})
            if not failed_size:
                match_detail['size'] = 'size'

        elif notes: # matches 'Standard', 'Small', etc..
            size, created_size, failed_size = get_or_create_model(Size, {'notes': notes, 'sub_notes': sub_notes})
            if not failed_size:
                match_detail['size'] = 'size'
        else:
            # Did not specifically match a size
            size, created_size, failed_size = get_or_create_model(Size, NO_MATCHED_SIZE)

    return size, created_size, failed_size, medium, created_medium, failed_medium

# MEDIUMS = { 'Medium Name' : {
#                      'word' : ['exact', 'words', 'to', 'match', 'this', 'MeDiUM', ... ],
#                      're' : ['regex1_to_match_medium', 'regex_2', ... ]
#                      'use_value_for_description' : True / False    # When True, the created Medium.description will be set to the trimmed source field (Size or Type)
#                                                                    # When False (or not present), the created Medium.description will be set to the Medium Name
#                      'greater_than' : [ 'Medium Name 1', ... ]     # When Medium is matched by both the Source Size and Source Type its possible to match two different mediums.
#                                                                    # Any Medium Name listed under the 'greater_than' list, means upon two di BAD LUCK FIGURE IT OUT YOURSELF
#                      'lesser_than' : [ 'Medium Name 1', ... ]      # these are the lesser than mediums.... blah blah read above BAD LUCK... WANGOD!!!
MEDIUMS = {
    'Paper' : { 'word' : ['A4', 'A5', 'A3', '1/3 A4 size'], 're' : ['(\d+)[\s]{0,}[pP]ages?'], 'greater_than' : [], 'lesser_than' : [] },
    'Sheet' : { 'word' : [], 're' : ['[Ss]heets?[\s]{1,}[Pp]?a?p?e?r?'], 'greater_than' : [], 'lesser_than' : [] },
    'Brochure' : { 'word' : [], 're' : ['.*[Bb][RrOo][OoRr][Cc][Hh][Uu][Rr][Ee]'], 'greater_than' : [], 'lesser_than' : [] },
    'Folding Card' : { 'word' : ['Flip-Top Cards', 'Fold Card', 'Xmas Folding Card', 'Note-Size Folding', 'Die-Cut Folding'], 're' : ['.*([Ff][Oo]r?[Ll][Dd][Ii][Nn][Gg]|[Mm]ultifold)'], 'greater_than' : [], 'lesser_than' : [] },
    'Postcard' : { 'word' : ['Standard Postcards', 'Xmas Postcard'], 're' : ['(P/c|[Pp]card|[Pp][Oo]st[\s]?[Cc]ard|Potsc)', 'Koren\s[Pp]ostcards?'], 'greater_than' : [], 'lesser_than' : [] },
    'Laser Card' : { 'word' : ['Four Up Post Card'], 're' : ['.*[Ll]a[sz]er\s(format|[Cc]ard)'], 'greater_than' : [], 'lesser_than' : [] },
    'Tape' : { 'word' : [], 're' : ['(\d+)[\s]{0,}[Tt]apes?'], 'greater_than' : [], 'lesser_than' : [] },
    'Tube' : { 'word' : [], 're' : ['(\d+)[\s]{0.}[Tt]ubes?'], 'greater_than' : [], 'lesser_than' : [] },
    'Jar' : {  'word' : [], 're' : ['[Jj]ars?'], 'greater_than' : [], 'lesser_than' : [] },
    'Magnet' : { 'word' : [], 're' : ['.*[Mm][Aa][Gg][Nn][Ee][Tt]'], 'greater_than' : [], 'lesser_than' : [] },
    'Bag' : { 'word' : [],  're' : ['.*([Tt]ote|[Bb]ag)'], 'greater_than' : [], 'lesser_than' : [] },
    'Spidertech' : { 'word' : [], 're' : ['Spidertech'], 'greater_than' : [], 'lesser_than' : [], 'use_value_for_description' : True },
    'Badge' : { 'word' : [], 're' : ['.*[Bb][Aa][Dd][Gg][Ee]'], 'greater_than' : [], 'lesser_than' : [] },
    'Card' : { 'word' : ['Cards', 'Crads', 'Card', 'card'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Kit' : { 'word' : ['Kit', 'kit'], 're' : ['Take[\s]{1,}Home[\s]{1,}Kit'], 'greater_than' : [], 'lesser_than' : [] },
    'Stationary' : {
        'word' : ['Pen', 'Pencil', 'Pad', 'Scissors-type trimmer', 'Stationery', 'Eraser', 'Pin/Tacs', 'Bone Pen', 'Neck Stick Pen' ],
        're' : [], 'greater_than' : [], 'lesser_than' : []
    },
    'Sticker' : { 'word' : ['Sticker', 'Stickers', 'Sticker roll', 'Boxed Stickes', 'sticker', 'Roll of stickers', 'Personalised Stickers'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Plaque' : { 'word' : ['wall plaque', 'Wall Plaque'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Computer Form' : { 'word' : ['Computer Form', 'Comp form', 'Compiter Form', 'comp form'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Clipboard' : { 'word' : ['Clipboard'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Book' : { 'word' : [], 're' : ['[Bb]ooks?$'], 'greater_than' : [], 'lesser_than' : [] },
    'Clinic Supplies' : { 'word' : ['Clinic Supplies'], 're' : ['[Ww]all[\s]+[Cc]hart'], 'greater_than' : [], 'lesser_than' : [] },
    'Miscellaneous' : { 'word' : ['Miscellaneous'], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Patient Education/Instruction' : { 'word' : [ 'Patient Education', 'Patient Instruction', 'Information Pads' ], 're' : [], 'greater_than' : [], 'lesser_than' : [] },
    'Multimedia' : {
        'word' : ['CD', 'Video', 'DVD', 'X-Ray', 'Audio Tapes Koren', 'Compact Disc', 'Video Tapes', 'Cassette', 'Book& CD', 'Brochure Disc', '6 Audio Tapes', 'Neck & Arm Pain DVD', '21st Century Smile DVD', 'CD of AMCT book', 'Virtual Tour DVD', 'Ted Koren Lecture Notes & CD', 'CD and Vaccination Notes', 'Smile after smile video', 'Waiting Room DVD-Pal Version', 'Patient Care CD', 'xray film', 'Basic Scan Protocol CD', 'Basic Scan Protocol DVD', 'Spinal Research Book/CD', 'Childhood Vaccination Book/CD', 'X-Ray film', 'X-ray Charts'],
        're' : [], 'greater_than' : [], 'lesser_than' : []
    },
    'Pamphlet' : { 'word' : [], 're' : ['[Pp]{1}amphlet'], 'greater_than' : [], 'lesser_than' : [] },
    'Flyer' : { 'word' : [], 're' : ['[Ff]{1}lyer'], 'greater_than' : [], 'lesser_than' : [] },
    'Poster' : { 'word' : [], 're' : ['.*[Pp]{1}oster'], 'greater_than' : [], 'lesser_than' : [] },
    'Calendar' : { 'word' : [], 're' : ['.*[Cc]{1}[Aa][Ll][Ee][Nn][Dd][Aa][Rr].*'], 'greater_than' : [], 'lesser_than' : [] },
    'Clothing/Apparel' : {
        'word' : ['Polo Shirt', 'Labcoat', 'scrub jacket', 'fitted scrub pant', 'Smart Bib', 'Adult Shoes', 'PVC Wallet-Personal', 'Shoehorn/Backscratcher', 'Gloves'],
        're' : ['([Cc]{1}lothing|Scr?ub\s{1}Top|[Tt]{1}-?[Ss]{1}hirt|.*[Pp]{1}ants|[Nn]{1}eck[\s]+|Bibs.*|.*Bibs|.*[Jj]acket|.*V?\s?Top.*|V[\s\-]{1}Neck|CAA.*Gown|Lab Coat|Cardigan|Gowns[\s]{1,}.*)'], 'greater_than' : [], 'lesser_than' : [] 
    } }
def sanitize_mediums_dict():
    # Add NO_MEDIUM and NO_MATCHED_MEDIUM to MEDIUMS dict
    #   MEDIUMS.keys() contains all 'Named' Mediums when adding NO_MATCHED_MEDIUM
    MEDIUMS[NO_MATCHED_MEDIUM['name']] = { 'greater_than': [NO_MEDIUM['name']], 'lesser_than' : list(MEDIUMS.keys()) }
    #   but here MEDIUMS.keys() will contain NO_MATCHED_MEDIUM, which is/should-be in the lesser than match details for NO_MEDIUM
    MEDIUMS[NO_MEDIUM['name']] = { 'lesser_than': list(MEDIUMS.keys()) }

    # Ensure all possible Medium matching details keys are set for each Medium in the MEDIUMS dict
    #  and add NO_MEDIUM and NO_MATCHED_MEDIUM to the 'greater_than' details of all 'Named' Mediums
    for medium_name in list(MEDIUMS.keys()):
        for key in ['word', 're', 'greater_than', 'lesser_than']:
            if not key in MEDIUMS[medium_name]:
                MEDIUMS[medium_name][key] = []
        if not 'use_value_for_description' in MEDIUMS[medium_name]:
            MEDIUMS[medium_name]['use_value_for_description'] = False

        if not medium_name in [NO_MEDIUM['name'], NO_MATCHED_MEDIUM['name']]:
            for non_medium_name in [NO_MEDIUM['name'], NO_MATCHED_MEDIUM['name']]:
                if not non_medium_name in MEDIUMS[medium_name]['greater_than']:
                    MEDIUMS[medium_name]['greater_than'].append(non_medium_name)

    # Sanity Check: ensure all 'greater_than' Mediums contain a 'lesser_than' for the corresponding Medium
    insane = False
    for medium_name, match_details in MEDIUMS.iteritems():
        for greater_than_medium in match_details['greater_than']:
            if not medium_name in MEDIUMS[greater_than_medium]['lesser_than']:
                print 'MEDIUMS Configuration Mismatch!'
                print 'Medium', medium_name, 'has', greater_than_medium, 'as a GREATER THAN Medium'
                print 'However, Medium', greater_than_medium, 'DOES NOT HAVE', medium_name, 'as a LESSER THAN Medium'
                print 'Medium:', medium_name, 'MatchDetails:', MEDIUMS[medium_name]
                print 'Medium:', greater_than_medium, 'MatchDetails:', MEDIUMS[greater_than_medium], '\n'
                insane = True

        for lesser_than_medium in match_details['lesser_than']:
            if not medium_name in MEDIUMS[lesser_than_medium]['greater_than']:
                print 'MEDIUMS Configuration Mismatch!'
                print 'Medium', medium_name, 'has', lesser_than_medium, 'as a LESSER THAN Medium'
                print 'However, Medium', lesser_than_medium, 'DOES NOT HAVE', medium_name, 'as a GREATER THAN Medium'
                print 'Medium:', medium_name, 'MatchDetails:', MEDIUMS[medium_name]
                print 'Medium:', greater_than_medium, 'MatchDetails:', MEDIUMS[greater_than_medium]
                insane = True

    if insane:
        print 'Fix the MEDIUMS dict, and try again.  Bailing Out'
        sys.exit(1)
    
# word_list contains either both, or one of, a source Card Details "Size" and "Type" field, depending on whether a Size was matched from src_size.
def determine_product_medium(word_dict, match_detail):
    possible_mediums = []

    for src_field_name, src_field_value in word_dict.iteritems():
        if not src_field_value:
            if not NO_MEDIUM['name'] in map(lambda x: x['medium']['name'], possible_mediums):
                possible_mediums.append({'source_field' : None, 'source_value': None, 'medium' : NO_MEDIUM})
            continue

        clean_field = src_field_value.strip()

        for medium_name, match_details in MEDIUMS.iteritems():
            if clean_field in match_details['word'] or matches_regex_list(clean_field, match_details['re']):
                if not medium_name in map(lambda x: x['medium']['name'], possible_mediums):
                    if match_details['use_value_for_description']:
                        medium_description = clean_field
                    else:
                        medium_description = medium_name

                    possible_mediums.append({'source_field': src_field_name, 'source_value': clean_field, 'medium' : {'name' : medium_name, 'description' : medium_description}})

    if len(possible_mediums) == 0:
        possible_mediums.append({'source_field' : None, 'source_value': None, 'medium' : NO_MATCHED_MEDIUM})

    medium_details_to_use = reduce(find_greatest_medium, possible_mediums)

    if medium_details_to_use.__class__.__name__ == 'list':
        # we could not reduce to one medium, somebody has to decide what to do.
        # pick a choice goes here...
        print 'Product matches multiple Medium\'s which cannot be resolved automatically'
        print 'Mediums matched from Source Card Details:', possible_mediums
        chosen_medium = False
        while chosen_medium not in map(lambda x: str(x), range(0, len(possible_mediums))):
            for i, possible_medium in enumerate(possible_mediums):
                print '(' + str(i) + ') Possible Medium:', possible_medium
            print 'Which Medium do you want to use for this Product? (' + '/'.join(map(lambda x: str(x), range(0, len(possible_mediums)))) + ')'
            chosen_medium = get_char()

        medium_details_to_use = possible_mediums[int(chosen_medium)]

    medium, created_medium, failed_medium = get_or_create_model(Medium, medium_details_to_use['medium'])
    
    if not failed_medium:
        match_detail['medium'] = medium_details_to_use['source_field']
        
    return medium, created_medium, failed_medium

def find_greatest_medium(medium_a, medium_b):
    # TODO Move Conditional Greater into MEDIUMS dict
    #   { 'Medium Name' : { 'greater_than' : 'Other Medium Name', 'by_source' : 'source that matched Medium Name' } }
     #   'Paper' : { 'greater_than' : 'Clothing/Apparel', 'by_source': 'A4' },
    CONDITIONAL_GREATER = { 
        'Multimedia' : { 'greater_than' : ['Tape', 'Brochure', 'Clothing/Apparel'], 'by_source' : ['Cassette', 'Brochure Disc', 'Neck & Arm Pain DVD'] },
        'Folding Card' : { 'greater_than' : ['Clothing/Apparel', 'Paper', 'Postcard'], 'by_source' : ['Flip-Top Cards', 'Folding Card']},
        'Postcard' : { 'greater_than' : ['Computer Form'], 'by_source' : ['Post Card'] },
        'Laser Card' : { 'greater_than' : ['Postcard'], 'by_source' : ['4-Up laser format'] },
        'Card' : { 'greater_than' : ['Folding Card'], 'by_source' : ['Card'] },
        'Book' : { 'greater_than' : ['Paper'], 'by_source' : ['Books'] },
        'Stationary' : { 'greater_than' : ['Clothing/Apparel', 'Paper'], 'by_source' : ['Neck Stick Pen', 'Stationery'] },
        'Brochure' : { 'greater_than' : ['Folding Card', 'Paper'], 'by_source' : ['Patient Information Brochure', 'brochure'] },
        'Pamphlet' : { 'greater_than' : ['Paper'], 'by_source' : ['Pamphlet'] },
        'Patient Education/Instruction' : { 'greater_than' : ['Brochure'], 'by_source' : ['Patient Education'] },
        'Clinic Supplies' : { 'greater_than' : ['Paper'], 'by_source' : ['Clinic Supplies'] }
    }

    # medium_a can possibly contain multiple Mediums as not all Mediums have been weighted for GREATNESS
    if medium_a.__class__.__name__ == 'list':
        for this_medium_a in medium_a:
            # want to check if medium_b is greater than any mediums in medium_a list, if it is, medium_b should be returned; else medium_b is added to the list and list is returned
            if this_medium_a['medium']['name'] in MEDIUMS[medium_b['medium']['name']]['greater_than'] and medium_b['medium']['name'] in MEDIUMS[this_medium_a['medium']['name']]['lesser_than']:
                return medium_b
            elif medium_b['medium']['name'] in CONDITIONAL_GREATER and this_medium_a['medium']['name'] in CONDITIONAL_GREATER[medium_b['medium']['name']]['greater_than'] and medium_b['source_value'] in CONDITIONAL_GREATER[medium_b['medium']['name']]['by_source']:
                return medium_b

        medium_a.append(medium_b)
        return medium_a
    else:
        # evaluating only two Mediums...
            # medium_a is GREATER THAN medium_b
        if medium_b['medium']['name'] in MEDIUMS[medium_a['medium']['name']]['greater_than'] and medium_a['medium']['name'] in MEDIUMS[medium_b['medium']['name']]['lesser_than']:
            return medium_a
        elif medium_a['medium']['name'] in CONDITIONAL_GREATER and medium_b['medium']['name'] in CONDITIONAL_GREATER[medium_a['medium']['name']]['greater_than'] and medium_a['source_value'] in CONDITIONAL_GREATER[medium_a['medium']['name']]['by_source']:
            return medium_a
        
            # medium_b is GREATER THAN medium_a
        elif medium_a['medium']['name'] in MEDIUMS[medium_b['medium']['name']]['greater_than'] and medium_b['medium']['name'] in MEDIUMS[medium_a['medium']['name']]['lesser_than']:
            return medium_b
        elif medium_b['medium']['name'] in CONDITIONAL_GREATER and medium_a['medium']['name'] in CONDITIONAL_GREATER[medium_b['medium']['name']]['greater_than'] and medium_b['source_value'] in CONDITIONAL_GREATER[medium_b['medium']['name']]['by_source']:
            return medium_b
        else:
            return [medium_a, medium_b]


def create_product_price_levels(src_carddetail, product, price_level_group):
    created, failed = 0, 0
    one_item_words = ['each', 'Each', '1 each', 'EACH', '1 pad', 'per pkg', 'pkg', 'Pkt', 'pkt', 'per unit', 'per unt', 'per pack', 'PK', 'Bag', 'Per box']
    item_per_number_re = re.compile('(per|Pkt|each)[/\s]{1,}(\d+)')
    item_range_re = re.compile('(\d).*-.*(\d)')
    item_number_re = re.compile('\d+')
    item_min_re = re.compile('((\d+).*\+|\+(\d+)|(\d+)\s{1,}[Pp]lus)')
    price_number_re = re.compile('number_(\d+)_price')

    BLOCK_PRICELEVEL_MAP = { 'number_50_price': 'per_1',
                             'number_100_price' : 'per_2',
                             'number_200_price' : 'per_3',
                             'number_300_price' : 'per_4',
                             'number_500_price' : 'per_5',
                             'number_1000_price' : 'per_6',
                             'number_250_price' : 'per_7',
                             'number_2000_price' : 'per_8',
                             'number_2500_price' : 'per_9' }

    # Cost Price Ea is the SmartPractice cost of the product... now stored as Product.sp_cost
    #if src_carddetail.cost_price_ea > 0:
    #    price_level_each = PriceLevel(product=product, min_amount=1, max_amount=1, cost_per_item=src_carddetail.cost_price_ea, cost_per_block=src_carddetail.cost_price_ea, block_only=False)
    #    if save_model_obj(price_level_each):
    #        created += 1
    #    else:
    #        failed += 1

    for price_field, per_field in BLOCK_PRICELEVEL_MAP.iteritems():
        price_value = getattr(src_carddetail, price_field)
        per_value = getattr(src_carddetail, per_field)
        notes = None

        if price_value > 0:
            if per_value:
                clean_per_value = per_value.strip()
                per_num_match = item_per_number_re.match(clean_per_value)
                range_match = item_range_re.match(clean_per_value)
                int_match = item_number_re.match(clean_per_value)
                min_match = item_min_re.match(clean_per_value)

                if clean_per_value in one_item_words:
                    min_amt = max_amt = 1
                elif per_num_match:
                    min_amt = max_amt = per_num_match.group(2)
                elif range_match:
                    min_amt = range_match.group(1)
                    max_amt = range_match.group(2)
                elif min_match:
                    if min_match.group(2):
                        min_amt = min_match.group(2)
                    elif min_match.group(3):
                        min_amt = min_match.group(3)
                    elif min_match.group(4):
                        min_amt = min_match.group(4)
                    max_amt = 0
                elif int_match:
                    min_amt = max_amt = int_match.group(0)
                else:
                    min_amt = max_amt = 0 # really got NFI whats going on here, just set to 0 so it imports.  PriceLevel.notes will contain the textual per_value
                    notes = 'UNDETERMINED AMOUNTS'
            else:
                # no textual 'per' value, assume the 'per' is the number_X_price ; a block of X items.
                number_block = price_number_re.match(price_field)
                min_amt = max_amt = number_block.group(1)
                per_value = 'number block match (' + str(min_amt) + ')'

            price_level = PriceLevel(min_amount=min_amt, max_amount=max_amt, cost_per_item=price_value, notes=notes)
            found_existing_price_level = False
            # if we have a PriceLevelGroup, its possible this PriceLevel already exists.  If it exists, we just add this product to the pricelevel.
            if price_level_group:
                print 'We Have a Price Level Group!', inspect_model_obj(price_level_group)
                #print 'price_level_group.price_levels', inspect_model_collection(price_level_group.price_levels.all())
                price_level.price_level_group = price_level_group
                # go through price_levels to see if this one already exists
                for existing_price_level in price_level_group.price_levels.all():
                    if same_price_level_details(existing_price_level, price_level):
                        print 'Found existing PriceLevel', inspect_model_obj(existing_price_level), 'for PriceLevelGroup', inspect_model_obj(price_level_group)
                        print 'Adding Product to existing PriceLevel'
                        existing_price_level.products.add(product)
                        #if not save_model_obj(existing_price_level, True):
                        #    print 'Error saving existing price level adding the Product', inspect_model_obj(product)
                        #    pause_terminal()
                        #else:
                        add_import_match_detail(existing_price_level, src_carddetail, [price_field, per_field], per_value)

                        found_existing_price_level = True
                        break
                        #return created, failed
                        #if existing_price_level.notes:
                        #    existing_price_level.notes += ', ' + str(per_value)
                        #else:
                        #    existing_price_level.notes = str(per_value)
                        #if not save_model_obj(existing_price_level, True):
                        #    print 'Error saving existing price level adding the per_value to the PriceLevel.notes field'
                        #    pause_terminal()
                     

            if not found_existing_price_level:
                if save_model_obj(price_level):
                    created += 1
                    price_level.products.add(product)
                    #if not save_model_obj(price_level, True):
                    #    print 'Error re-saving new price level adding the Product!'
                    #    print 'PriceLevel', inspect_model_obj(price_level)
                    #    print 'Product', inspect_model_obj(product)
                    #    pause_terminal()
                    #else:
                    add_import_match_detail(price_level, src_carddetail, [price_field, per_field], per_value)
                else:
                    failed += 1

    return created, failed

def same_price_level_details(existing_price_level, new_price_level):
    print 'Comparing Existing PriceLevel', inspect_model_obj(existing_price_level)
    print 'With New PriceLevel', inspect_model_obj(new_price_level)

    PRICELEVEL_COMPARE_COLS = [ 'min_amount', 'max_amount', 'cost_per_item' ]

    same_price_level = True
    for column in PRICELEVEL_COMPARE_COLS:
        if str(getattr(existing_price_level, column)) != str(getattr(new_price_level, column)):
            print 'PriceLevel detail mismatch! Existing PriceLevel', existing_price_level.id, column, '=', getattr(existing_price_level, column), 'New PriceLevel', column, '=', getattr(new_price_level, column)
            same_price_level = False

    return same_price_level
##### END

##### FUNCTIONS to convert source table Borders into target tables Order, OrderStatus, OrderProduct
# Borders Columns:
#   Qty Out:    Quantity Out - this many of the items we're/are in stock NOW to forfill the order, but the customer has ordered more than this number.  This number seems to always match "From Stock"
#   +From Stock: as it is the number of items 'shipped'/'assigned to this order' that are currently in stock.
#   Back Order Qty:  The number of items on backorder to forfill this product order for the customer.  (Back Order Qty) + (Qty Out || From Stock) == total number of this item the customer ordered.
#   Price Each: The price, for the customer (assumption: see 'Cost Ea'), for 1x of this item.
#   Total Price: Total price the customer pays for all the items. (Back Order Qty + (Qty Out || From Stock)) * (Price Ea) == Total Price
#   Net Value: appears to dupe Total Price; cannot find record where "Total Price" != "Net Value" (true for Borders, but Net Value is less the discount, or is it the other way? :)
#   Cost Ea:  The price, for SmartPractice??, for 1x of this item.  Cost Ea is USUALLY < "Price Each", except 4 records, so this is my assumption....
def convert_source_borders():
    created_back_orders, failed_back_orders = 0, 0
    processed_records, skipped_records = 0, 0

    for src_border in Borders.objects.using(SOURCE_DB).all():
        print "--------------------------------------------------------------------------------------------------------"
        print "Found source Border (Back Order):", inspect_model_obj(src_border), "\n"

        if not src_border.custid:
            print 'Source Border (Back Order) has no CustID??'
            print 'Skipping Back Order'
            print "--------------------------------------------------------------------------------------------------------\n\n"
            skipped_records += 1
            continue

        border_exists = BackOrder.objects.using(TARGET_DB).filter(from_borders_fakeid=src_border.fakeid)
        if border_exists.count() > 0:
            print "Found existing Back Order: " + inspect_model_obj(border_exists[0]) + "\n"
            print "Existing OrderProducts: " + inspect_model_collection(border_exists[0].products.all()) + "\n"
            print "Skipping Back Order"
            print "--------------------------------------------------------------------------------------------------------\n\n"
            skipped_records += 1
            continue

        try:
            customer = Customer.objects.using(TARGET_DB).filter(from_src_company_id=src_border.custid)[0]
        except IndexError:
            print 'Could not find a Customer created with the CustID:', src_border.custid
            print 'Skipping Back Order'
            print "--------------------------------------------------------------------------------------------------------\n\n"
            skipped_records += 1
            continue

        product = get_model(Product, {'code' : src_border.product_code})
        if not product:
            print 'Could not find a Product with Code', src_border.product_code, 'for Back Order with FakeID:', src_border.fakeid
            print 'Source Borrder:', inspect_model_obj(src_border)
            print 'Cannot create Back Order for this product, skipping Back Order'
            skipped_records += 1
            try:
                source_product = CardDetails.objects.using(SOURCE_DB).filter(product_code=src_border.product_code)[0]
                print 'Found Product in Source CardDetails table:', inspect_model_obj(source_product)
            except IndexError:
                print 'Could not find Product in Source CardDetails table'
            pause_terminal()
            continue

        processed_records += 1

        back_order = BackOrder(customer=customer, product=product, from_borders_fakeid=src_border.fakeid, amount=src_border.back_order_qty)
        
        if save_model_obj(back_order):
            created_back_orders += 1
        else:
            failed_back_orders += 1

    source_stats = { 'table': 'Borders',
                     'records': Borders.objects.using(SOURCE_DB).all().count(),
                     'processed': processed_records,
                     'skipped': skipped_records }

    target_stats = [ ('Order', created_back_orders, failed_back_orders) ]

    print_convert_stats(source_stats, target_stats)
##### END

##### FUNCTIONS to convert source tables Orders, OrderHistory, Ro2, OrderDetails, DetailsHistory into target tables Order, OrderProduct, OrderStatus, Company and Invoice
# Orders source table
#  'Invoice Total': Total cost, for the customer, for the order placed.  Order Cost + QPI Margin + Delivery Charge== Invoice Total
#  'Order Cost': Cost of the order for SmartPractice.
#  'Delivery Charge': Shipping cost
#  'QPI Margin': Profit made from this order.  Invoice Total - Order Cost - Delivery Charge == QPI Margin

def convert_source_orders():
    #SRC_ORDER_TABLES = [ Orders, OrderHistory, Ro2 ]
    #SRC_ORDER_DETAIL_TABLES = [ OrderDetails, DetailsHistory ]
    SRC_ORDER_TABLES = [ Orders ]
    ONLY_PROCESS_ORDER_DETAILS_FROM = OrderDetails

    use_saved_choices = None
    while use_saved_choices != 'y' and use_saved_choices != 'n':
        print 'Do you want to automatically use the last saved choice to handle duplicate order detail records? (y/n)'
        use_saved_choices = get_char()

    PREVIOUS_ORDER_CHOICES = None

    if use_saved_choices == 'y' or use_saved_choices == 'Y':
        PREVIOUS_ORDER_CHOICES = load_previous_duplicate_record_choices('order.pkl')

    if not PREVIOUS_ORDER_CHOICES:
        PREVIOUS_ORDER_CHOICES = { }

    CURRENT_ORDER_CHOICES = { }

    for src_order_table in SRC_ORDER_TABLES:
        created_orders, failed_orders = 0, 0
        created_order_products, failed_order_products, skipped_order_products = 0, 0, 0
        created_companies, failed_companies = 0, 0
        created_invoices, failed_invoices = 0, 0
        processed_records, skipped_records = 0, 0

        src_order_table_name = None

        for src_order in src_order_table.objects.using(SOURCE_DB).all():
            if not src_order_table_name:
                src_order_table_name = src_order.__class__.__name__

            print "--------------------------------------------------------------------------------------------------------"
            print "Found source", src_order_table_name + ':', inspect_model_obj(src_order), "\n"
            
            if not src_order.company_id:
                print 'Source Order has no Company ID??'
                print 'Skipping Order from source (class:', src_order.__class__.__name__, ')'
                print "--------------------------------------------------------------------------------------------------------\n\n"
                skipped_records += 1
                continue
            
            order_exists = Order.objects.using(TARGET_DB).filter(from_src_order_id=src_order.order_id)
            if order_exists.count() > 0:
                print "Found existing Order: " + inspect_model_obj(order_exists[0]) + "\n"
                print "Existing OrderProducts: " + inspect_model_collection(order_exists[0].products.all()) + "\n"
                print "Skipping Order from source (class:", src_order.__class__.__name__, ')'
                print "--------------------------------------------------------------------------------------------------------\n\n"
                skipped_records += 1
                continue

            if ONLY_PROCESS_ORDER_DETAILS_FROM:
                src_order_details = ONLY_PROCESS_ORDER_DETAILS_FROM.objects.using(SOURCE_DB).filter(order_id=src_order.order_id)
                if src_order_details.count() == 0:
                    print 'Source Order', src_order.order_id, '(class:', src_order.__class__.__name__ + ')', 'has no associated records in Source Order Details table', inspect_model_obj(src_order)
                    print 'Skipping Order'
                    print "--------------------------------------------------------------------------------------------------------\n\n"
                    skipped_records += 1
                    continue
            else:
                src_order_details_results = OrderDetails.objects.using(SOURCE_DB).filter(order_id=src_order.order_id)
                order_details_records = src_order_details_results.count()
                src_details_history_results = DetailsHistory.objects.using(SOURCE_DB).filter(order_id=src_order.order_id)
                details_history_records = src_details_history_results.count()

                print 'Found', order_details_records, 'Source OrderDetails record(s) for Order ID', src_order.order_id
                print 'Found', details_history_records, 'Source DetailsHistory record(s) for Order ID', src_order.order_id

                if not src_order.order_id in CURRENT_ORDER_CHOICES:
                    CURRENT_ORDER_CHOICES[src_order.order_id] = {}

                if order_details_records > 0 and details_history_records > 0:
                    if order_details_records == details_history_records:
                        src_order_details = None
                        for detail_a in src_order_details_results:
                            same_detail = False
                            for detail_b in src_details_history_results:
                                if same_order_details(detail_a, detail_b):
                                    same_detail = True
                                    break

                            if not same_detail:
                                print 'Source Order Details Record mismatch'
                                if src_order.order_id in PREVIOUS_ORDER_CHOICES:
                                    CURRENT_ORDER_CHOICES[src_order.order_id] = PREVIOUS_ORDER_CHOICES[src_order.order_id]
                                    if PREVIOUS_ORDER_CHOICES[src_order.order_id]['OrderDetails'] and PREVIOUS_ORDER_CHOICES[src_order.order_id]['DetailsHistory']:
                                        # merge
                                        src_order_details = merge_order_detail_collections(src_order_details_results, src_details_history_results)
                                    elif PREVIOUS_ORDER_CHOICES[src_order.order_id]['OrderDetails'] and not PREVIOUS_ORDER_CHOICES[src_order.order_id]['DetailsHistory']:
                                        src_order_details = src_order_details_results
                                    elif not PREVIOUS_ORDER_CHOICES[src_order.order_id]['OrderDetails'] and PREVIOUS_ORDER_CHOICES[src_order.order_id]['DetailsHistory']:
                                        src_order_details = src_details_history_results
                                else:
                                    src_order_details = handle_mismatched_order_details_records(src_order_details_results, src_details_history_results, CURRENT_ORDER_CHOICES)
                                break

                        if not src_order_details: # details results identical in OrderDetails and DetailsHistory
                            CURRENT_ORDER_CHOICES[src_order.order_id]['OrderDetails'] = True
                            CURRENT_ORDER_CHOICES[src_order.order_id]['DetailsHistory'] = False
                            src_order_details = src_order_details_results
                    else: # number of records in OrderDetails and DetailsHistory do not match
                        print 'Source Order Details record count mismatch!'
                        src_order_details = handle_mismatched_order_details_records(src_order_details_results, src_details_history_results, CURRENT_ORDER_CHOICES)
                elif order_details_records > 0 and details_history_records == 0:
                    CURRENT_ORDER_CHOICES[src_order.order_id]['OrderDetails'] = True
                    CURRENT_ORDER_CHOICES[src_order.order_id]['DetailsHistory'] = False
                    src_order_details = src_order_details_results
                elif order_details_records == 0 and details_history_records > 0:
                    CURRENT_ORDER_CHOICES[src_order.order_id]['OrderDetails'] = False
                    CURRENT_ORDER_CHOICES[src_order.order_id]['DetailsHistory'] = True
                    src_order_details = src_details_history_results
                elif order_details_records == 0 and details_history_records == 0:
                    print 'Source Order', src_order.order_id, '(class:', src_order.__class__.__name__ + ')', 'has no associated records in Source Order Details table', inspect_model_obj(src_order)
                    print 'Skipping Order'
                    print "--------------------------------------------------------------------------------------------------------\n\n"
                    skipped_records += 1
                    continue
                else:
                    print 'Dunno wtf is going on ??? your order details table counts are whack!!!!!! skipping to next order...'
                    pause_terminal()
                    skipped_records += 1
                    continue

            try:
                customer = Customer.objects.using(TARGET_DB).filter(from_src_company_id=src_order.company_id)[0]
            except IndexError:
                print 'Could not find a Customer created with the Company ID:', src_order.company_id
                print 'Skipping Order', '(class:', src_order.__class__.__name__ + ')'
                print "--------------------------------------------------------------------------------------------------------\n\n"
                skipped_records += 1
                continue

            processed_records += 1

            order = Order(customer=customer)
            dictionary_table_merge(ORDERS_TABLEMAP, src_order, order)
            dictionary_table_merge(FOUND_CUSTOMER_ORDER_MAP, customer, order)

            # does our total_cost include/exclude any discounts??
            # IMO; sub_total == cost of items ordered (excluding discount)
            #      shipping_cost == obvious
            #      discount == sum of all discounts applied to products on this order
            #      total_cost == sub_total + shipping_cost - discount
            if order.total_cost and order.shipping_cost:
                order.sub_total = order.total_cost - order.shipping_cost
            else:
                order.sub_total = order.total_cost

            if save_model_obj(order):
                order_status = OrderStatus(status='SD', notes='Imported Order; assumed shipped', order=order)
                if not save_model_obj(order_status):
                    print 'Could not save OrderStatus for Order', inspect_model_obj(order)
                    print 'OrderStatus:', inspect_model_obj(order_status)
                    print 'Order failed, skipping order'
                    print "--------------------------------------------------------------------------------------------------------\n\n"
                    failed_orders += 1
                    continue
            
                created_orders += 1

                if src_order.shipper_id and src_order.inv_no:
                    company = None
                    if src_order.shipper_id == '1' or src_order.shipper_id == '2': #Smart Practice
                        company, created, failed = get_or_create_model(Company, {'name': 'Smart Practice', 'phone': '<insert here>', 'fax': '<insert here>', 'registration': '<insert here>'})
                    elif src_order.shipper_id == '3': # SmartMethods
                        company, created, failed = get_or_create_model(Company, {'name': 'Smart Methods', 'phone': '<insert here>', 'fax': '<insert here>', 'registration': '<insert here>'})

                    if created:
                        created_companies += 1
                    if failed:
                        failed_companies += 1

                    if company:
                        if hasattr(src_order, 'invoice_date') and src_order.invoice_date:
                            invoice = Invoice(order=order, company=company, timestamp=src_order.invoice_date, number=src_order.inv_no)
                        elif hasattr(src_order, 'invoice_due') and src_order.invoice_due:
                            invoice = Invoice(order=order, company=company, timestamp=src_order.invoice_due, number=src_order.inv_no)
                        else:
                            invoice = Invoice(order=order, company=company, number=src_order.inv_no)
                            
                        if save_model_obj(invoice):
                            created_invoices += 1
                        else:
                            failed_invoices += 1

                print 'Found', len(src_order_details), 'source order details records to process'

                for src_order_detail in src_order_details:
                    print 'Found Source Order Detail (class:', src_order_detail.__class__.__name__, ')', inspect_model_obj(src_order_detail)
                    
                    if not src_order_detail.qty_out:
                        print 'Source Order Detail has no quantity, cannot create OrderProduct, skipping to next ordered item'
                        skipped_order_products += 1
                        continue

                    product = get_model(Product, {'code' : src_order_detail.product_code})
                    if not product:
                        print 'Could not find a Product with Code', src_order_detail.product_code, 'for source Order ID', src_order_detail.order_id
                        print 'Source Order Detail (class:', src_order_detail.__class__.__name__ + ') :', inspect_model_obj(src_order_detail)
                        print 'Cannot create OrderProduct for this product, skipping to next ordered product'
                        skipped_order_products += 1
                        try:
                            source_product = CardDetails.objects.using(SOURCE_DB).filter(product_code=src_order_detail.product_code)[0]
                            print 'Found Product in Source CardDetails table:', inspect_model_obj(source_product)
                        except IndexError:
                            print 'Could not find Product in Source CardDetails table'
                        pause_terminal()
                        continue
                    
                    order_product = OrderProduct(order=order, product=product)
                    dictionary_table_merge(ORDERDETAILS_TABLEMAP, src_order_detail, order_product)
        
                    if order_product.unit_price and order_product.unit_price > 0 and src_order.date and src_order.date > GST_STARTED_DATE:
                        order_product.unit_tax = calculate_gst_component(order_product.unit_price)

                    if save_model_obj(order_product):
                        created_order_products += 1
                        if order_product.discount_price and order_product.discount_price > 0:
                            order.discount += order_product.discount_price
                            order.save()
                            #if not save_model_obj(order):#, True):
                            #    print 'Error saving Order trying to update the total discount from a ordered product discount; Order:', inspect_model_obj(order)
                            #    print 'OrderProduct:', inspect_model_obj(order_product), "\n"
                            #    pause_terminal()
                        if order_product.unit_tax and order_product.unit_tax > 0:
                            order.tax += order_product.unit_tax * decimal.Decimal(order_product.quantity)
                            order.save()
                            #if not save_model_obj(order):#, True):
                            #    print 'Error saving Order trying to update the total tax from a ordered products unit tax; Order:', inspect_model_obj(order)
                            #    print 'OrderProduct:', inspect_model_obj(order_product), "\n"
                            #    pause_terminal()
                    else:
                        print 'Error saving OrderProduct for Order'
                        print 'Order:', inspect_model_obj(order), 'OrderProduct:', inspect_model_obj(order_product)
                        failed_order_products += 1


                print "--------------------------------------------------------------------------------------------------------"
                print "order.products (", order.products.count(), ") collection: " + inspect_model_collection(order.products.all())
                print "--------------------------------------------------------------------------------------------------------\n\n"
            else:
                failed_orders += 1
        
        source_stats = { 'table': src_order_table_name,
                         'records': src_order_table.objects.using(SOURCE_DB).all().count(),
                         'processed': processed_records,
                         'skipped': skipped_records }

        target_stats = [ ('Order', created_orders, failed_orders),
                         ('OrderProduct', created_order_products, failed_order_products),
                         ('Company', created_companies, failed_companies),
                         ('Invoice', created_invoices, failed_invoices) ]

        print_convert_stats(source_stats, target_stats)

    store_duplicate_record_choices('order.pkl', CURRENT_ORDER_CHOICES)

def handle_mismatched_order_details_records(order_details_results, details_history_results, CURRENT_ORDER_CHOICES):
    print 'Source Order Details Table "OrderDetails" has:', order_details_results.count(), 'record(s)'
    print 'Source Order Details Table "DetailsHistory" has:', details_history_results.count(), 'record(s)'
    print 'OrderDetails collection:', inspect_model_collection_and_find_related({'src_collection': order_details_results, 'src_key': 'product_code', 'target_model': Product, 'target_key': 'code'})
    print 'DetailsHistory collection:', inspect_model_collection_and_find_related({'src_collection': details_history_results, 'src_key': 'product_code', 'target_model': Product, 'target_key': 'code'})
    details_choice = None
    while details_choice != 'o' and details_choice != 'O' and details_choice != 'h' and details_choice != 'H' and details_choice != 'm' and details_choice != 'M':
        print 'o = use OrderDetails | h = use DetailsHistory | m = merge OrderDetails and DetailsHistory unique records  (o/h/m):'
        details_choice = get_char()

    if details_choice == 'o' or details_choice == 'O':
        CURRENT_ORDER_CHOICES[order_details_results[0].order_id]['OrderDetails'] = True
        CURRENT_ORDER_CHOICES[order_details_results[0].order_id]['DetailsHistory'] = False
        src_order_details = order_details_results
    elif details_choice == 'h' or details_choice == 'H':
        CURRENT_ORDER_CHOICES[details_history_results[0].order_id]['OrderDetails'] = False
        CURRENT_ORDER_CHOICES[details_history_results[0].order_id]['DetailsHistory'] = True
        src_order_details = details_history_results
    elif details_choice == 'm' or details_choice == 'M':
        CURRENT_ORDER_CHOICES[order_details_results[0].order_id]['OrderDetails'] = True
        CURRENT_ORDER_CHOICES[order_details_results[0].order_id]['DetailsHistory'] = True
        src_order_details = merge_order_detail_collections(order_details_results, details_history_results)
    else:
        print 'Someone hit some whack character while handling mismatched order details! Stop that ya hear?? Try again buddy'
        src_order_details = handle_mismatched_order_details_records(order_details_results, details_history_results, CURRENT_ORDER_CHOICES)

    return src_order_details

def same_order_details(detail_a, detail_b):
    SRC_ORDER_DETAILS_COMPARE_COLS = [ 'product_code', 'qty_out', 'from_stock', 'from_surplus', 'back_order_qty',
                                       'back_order_id', 'qty_bo', 'price_each', 'total_price', 'disc_p', 'disc_d',
                                       'net_value', 'qty_in', 'cost_ea', 'total_cost', 'royalty' ]

    class_a = detail_a.__class__.__name__
    class_b = detail_b.__class__.__name__

    for column in SRC_ORDER_DETAILS_COMPARE_COLS:
        if str(getattr(detail_a, column)) != str(getattr(detail_b, column)):
            print 'Source Order Details Record Mismatched', class_a + '.id =', detail_a.id, class_a + '.' + column, '=', getattr(detail_a, column), class_b + '.id =', detail_b.id, class_b + '.' + column, '=', getattr(detail_b, column)
            return False

    return True

def merge_order_detail_collections(detail_collection_a, detail_collection_b):
    src_order_details = list(detail_collection_a)
    for detail_b in detail_collection_b:
        unique = True
        for detail_a in detail_collection_a:
            if same_order_details(detail_a, detail_b):
                unique = False
                break

        if unique:
            src_order_details.append(detail_b)

    return src_order_details
##### END

##### GENERAL FUNCTIONS
def matches_regex_list(value, re_list):
    for regex in re_list:
        if re.compile(regex).match(value):
            return True

    return False

# pass in cost including gst, returns gst component.
#   DONE!  - Fix This!! all the values in SP Source DB are EXCLUDING GST!!
def calculate_gst_component(value):
    return round(calculate_gst_component_from_excluding_value(value), 2)

def calculate_gst_component_from_excluding_value(value_ex_gst):
    return decimal.Decimal(decimal.Decimal(decimal.Decimal(GST_PERCENTAGE) / decimal.Decimal(100.0)) * decimal.Decimal(value_ex_gst))

# wholly decimal.Decimal batman!
def calculate_gst_component_from_including_value(value_inc_gst):
    return decimal.Decimal(decimal.Decimal(value_inc_gst) - decimal.Decimal((decimal.Decimal(decimal.Decimal(100.0) / decimal.Decimal(decimal.Decimal(100.0) + decimal.Decimal(GST_PERCENTAGE))) * decimal.Decimal(value_inc_gst))))

def print_convert_stats(source, target, duplicate=None):
    print '--------------------------------------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------------------------------------'
    print 'Convert Source Table', source['table']
    print source['table'], 'Table Records:', source['records'], 'Processed:', source['processed'], 'Skipped:', source['skipped'], 'Total:', source['processed'] + source['skipped']
    print '--------------------------------------------------------------------------------------------------------'

    for target_table, created, failed in target:
        print target_table, 'Record(s) Created:', created, 'Failed:', failed, 'Total:', created + failed

    if duplicate:
        print '--------------------------------------------------------------------------------------------------------'
        print 'Duplicate Resolution(s) Automatic:', duplicate['auto'], 'Manual:', duplicate['manual'], 'Total:', duplicate['auto'] + duplicate['manual']

    print '--------------------------------------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------------------------------------'
    pause_terminal()

def dictionary_table_merge(table_map, source_obj, target_obj):
    for target_field, source_field in table_map.iteritems():
        if hasattr(source_field, '__iter__'):
            source_value = ''
            for src_field in source_field:
                src_field_value = getattr(source_obj, src_field)
                if src_field_value:
                    source_value += src_field_value + ' '
            source_value = source_value.rstrip(' ')
        else:
            source_value = getattr(source_obj, source_field)

        if source_value:
            setattr(target_obj, target_field, source_value)

def get_model(Model, criteria_map):
    try:
        model = Model.objects.using(TARGET_DB).filter(**criteria_map)[0]
    except IndexError:
        return False

    return model

def get_or_create_model(Model, column_map):
    try:
        model = Model.objects.using(TARGET_DB).filter(**column_map)[0]
        created = False
        failed = False
    except IndexError:
        model = Model(**column_map)
        if save_model_obj(model):
            created = True
            failed = False
        else:
            created = False
            failed = True

    return model, created, failed

# silent is set to true when updating an existing model (e.g. setting the tax for an order); without silent it appears like it has "Created a XYZClass...." when it really didnt
@transaction.commit_manually(using=TARGET_DB)
def save_model_obj(model, silent=False):
    try:
        model.full_clean()
        if not silent:
            print model.__class__.__name__ + " passes validation!"
        valid = True
    except django.core.exceptions.ValidationError as e:
        if not silent:
            print model.__class__.__name__ + " fails validation! " + str(e.message_dict)
        valid = False
    except:
        print "Unknown Error validating " + model.__class__.__name__, inspect_model_obj(model)
        pause_terminal()
        raise

    try:
        model.save(using=TARGET_DB)
        transaction.commit(using=TARGET_DB)
        if not silent:
            print "Created " + model.__class__.__name__ + ": " + inspect_model_obj(model) + "\n"
        return True
    except django.db.utils.DatabaseError as e:
        print "Database Error saving " + model.__class__.__name__ + ": " + str(e)
        print model.__class__.__name__ + " Object: " + inspect_model_obj(model)
        transaction.rollback(using=TARGET_DB)
        pause_terminal()
        return False
    except:
        print model.__class__.__name__ + " Object: " + inspect_model_obj(model)
        transaction.rollback(using=TARGET_DB)
        if not valid:
            print 'Error saving ' + model.__class__.__name__ + ' (Failed validation; look above for cause)'
            pause_terminal()
        else:
            print 'Unknown Error saving ' + model.__class__.__name__ + ' (raising error)'
            pause_terminal()
            raise
        return False

def inspect_model_obj(model):
    inspect_str = '['
    for field in model._meta.fields:
        inspect_str += '{"' + field.name + '": "' + field.value_to_string(model) + '"}, '
    return inspect_str.rstrip(', ') + ']'

def inspect_model_collection(model_collection):
    collection_str = '{\n'
    for model in model_collection:
        collection_str += inspect_model_obj(model) + ",\n"
    return collection_str.rstrip(",\n") + '\n}'

def inspect_model_collection_and_find_related(options):
    target_model_name = None
    collection_str = '{\n'
    for src_model in options['src_collection']:
        collection_str += inspect_model_obj(src_model) + ',\n'
        target_model = get_model(options['target_model'], {options['target_key'] : getattr(src_model, options['src_key'])})
        if target_model:
            if not target_model_name:
                target_model_name = target_model.__class__.__name__
            collection_str += 'Found Target ' + target_model_name + ':' + inspect_model_obj(target_model) + ',\n'
        else:
            if target_model_name:
                collection_str += 'Could not find a target ' + target_model_name + ' where ' + options['target_key'] + ' = ' + getattr(src_model, options['src_key']) + '\n'
                collection_str += '------------------>>>>>>>>>>>>>>>>>>>>TARGET ' + target_model_name + ' NOT FOUND<<<<<<<<<<<<<<<<<<<<<<<---------------------------\n\n'
            else:
                collection_str += 'Could not find a target model where ' + options['target_key'] + ' = ' + getattr(src_model, options['src_key'])
                collection_str += '------------------>>>>>>>>>>>>>>>>>>>>TARGET MODEL NOT FOUND<<<<<<<<<<<<<<<<<<<<<<<---------------------------\n\n'

    return collection_str

def pause_terminal():
    try:
        input("Press enter to continue: ")
    except:
        pass

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return char

def load_previous_duplicate_record_choices(pickle_file):
    data = None
    f = None
    try:
        f = open(pickle_file, 'rb')
        data = pickle.load(f)
    except IOError as e:
        print 'IOError trying to load pickle file', repr(pickle_file), repr(e)
        pause_terminal()
    except pickle.PickleError as e:
        print 'PickleError trying to load pickle file', repr(pickle_file), repr(e)
        pause_terminal()
    except:
        print 'Unknown Error trying to load pickle file', repr(pickle_file)
        pause_terminal()
        raise
    finally:
        if f:
            f.close()

    return data

def store_duplicate_record_choices(pickle_file, data):
    f = None
    try:
        f = open(pickle_file, 'wb')
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print 'IOError trying to save pickle file', repr(pickle_file), repr(e)
        pause_terminal()
    except pickle.PickleError as e:
        print 'PickleError trying to save pickle file', repr(pickle_file), repr(e)
        pause_terminal()
    except:
        print 'Unknown Error trying to save pickle file', repr(pickle_file), repr(e)
        pause_terminal()
        raise
    finally:
        if f:
            f.close()

# Asks if you want to convert ('This Table', 'calls_this_function_if_yes')
CONVERSION_QUESTION_MAP = [ #('Company', 'convert_source_company'),
                            #('MEMBADD', 'convert_source_membadd'),
                            ('Company and MEMBADD', 'convert_source_company_and_membadd'),
                            ('Card Details', 'convert_source_carddetails'),
                            ('Orders and Order Detail / Order History and Details History', 'convert_source_orders'),
                            ('Borders (Back Orders)', 'convert_source_borders') ]

for source_table_name, convert_func_name in CONVERSION_QUESTION_MAP:
    answer = None
    while answer != 'y' and answer != 'Y' and answer != 'n' and answer != 'N':
        print "\nConvert source table", source_table_name, '(y/n):'
        answer = get_char()
    
    if answer == 'Y' or answer == 'y':
        locals()[convert_func_name]()

