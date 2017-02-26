#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import Fbx,Contact

## Initialize and connect app.
app = Fbx('http://192.168.0.254/api/v3')
app.get_session_token()

def print_number(app, id):
    number = app.get_number(id)
    print("Id: %s" % id)
    print(number)

def print_address(app, id):
    address = app.get_address(id)
    print("Id: %s" % id)
    print(address)

def print_email(app, id):
    email = app.get_email(id)
    print("Id: %s" % id)
    print(email)

def print_url(app, id):
    url = app.get_url(id)
    print("Id: %s" % id)
    print(url)

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

#
# Create
#

# Contact

print(app.delete_contact(496))

contact = Contact()
contact.first_name = "Alain"
contact.last_name = "Bidon"
contact.display_name = "BIDON, Alain"
contact.notes = "Contact de test"

ncontact = app.new_contact(contact)
print(ncontact)

print("Delete id: %s" % ncontact.id)
print(app.delete_contact(ncontact.id))

