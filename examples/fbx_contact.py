#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import Fbx,Contact,Number

## Initialize and connect app.
app = Fbx('http://192.168.0.254/api/v3')
app.get_session_token()

def print_contact(app, id):
    contact = app.get_contact(id)
    print("Contact Id: %s" % id)
    print(unicode(contact))

def print_number(app, id):
    number = app.get_number(id)
    print("Number Id: %s" % id)
    print(unicode(number))

def print_address(app, id):
    address = app.get_address(id)
    print("Address Id: %s" % id)
    print(unicode(address))

def print_email(app, id):
    email = app.get_email(id)
    print("Email Id: %s" % id)
    print(unicode(email))

def print_url(app, id):
    url = app.get_url(id)
    print("Url: %s" % id)
    print(unicode(url))
    
'''

### Number
number = app.get_number(100)
print_number(app,100)

number.is_default = True
(success, result) = app.set_number(100,number)

print_number(app,100)
number.is_default = False
(success, result) = app.set_number(100,number)

print_number(app,100)
### Address
print_address(app,100)
address = app.get_address(100)
address.type = 'work'
(success, result) = app.set_address(100,address)
print_address(app,100)

address.type = 'home'
(success, result) = app.set_address(100,address)
print_address(app,100)
### Email
print_email(app,100)
email = app.get_email(100)
email.type = 'work'
(success, result) = app.set_email(100,email)
print_email(app,100)

email.type = 'home'
(success, result) = app.set_email(100,email)
print_url(app,100)
### Email
print_url(app,10)
url = app.get_url(10)

url.type = 'profile'
(success, result) = app.set_url(10,url)
print_url(app,10)

url.type = 'blog'
(success, result) = app.set_url(10,url)
print_url(app,10)

url.type = 'site'
(success, result) = app.set_url(10,url)
print_url(app,10)

url.type = 'other'
(success, result) = app.set_url(10,url)
print_url(app,10)

#print(app.delete_contact(496))
'''


#
# Contact
#

# contact

contact = Contact()
contact.first_name = "Alain"
contact.last_name = "Bidon"
contact.display_name = "BIDON, Alain"
contact.notes = "Contact de test"

print("\r\nCreate contact :")
print(contact)
ncontact = app.new_contact(contact)
contact_id = ncontact.id
print_contact(app,contact_id)

# number

number = Number()
number.contact_id = contact_id
number.number = '1234567890'
number.type = 'mobile'
print("\r\nCreate number :")
print(number)
nnumber = app.new_number(number)
print(nnumber)
number_id = nnumber.id
print_number(app,nnumber.id)
print_contact(app,nnumber.contact_id)
print_contact(app,contact_id)

number.number = '1234567891'
number.type = 'fixed'
print("\r\nCreate number :")
print(number)
nnumber = app.new_number(number)
number1_id = nnumber.id
print_number(app,number1_id)
print_contact(app,nnumber.contact_id)
print_contact(app,contact_id)

'''
print("\r\nDelete number id: %s" % number1_id)
print(app.delete_number(number_id))
print_contact(app,contact_id)
print("\r\nDelete number id: %s" % number_id)
print(app.delete_number(number_id))
print_contact(app,contact_id)
'''


print("\r\nDelete contact id: %s" % contact_id)
print(app.delete_contact(contact_id))
