#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import *

## Initialize and connect app.
app = Fbx('http://192.168.0.254/api/v3')
app.get_session_token()

def print_contact(app, id):
    contact = app.get_contact(id)
    print("\r\nContact Id: %s" % id)
    print(unicode(contact))

def print_number(app, id):
    number = app.get_number(id)
    print("\r\nNumber Id: %s" % id)
    print(unicode(number))

def print_address(app, id):
    address = app.get_address(id)
    print("\r\nAddress Id: %s" % id)
    print(unicode(address))

def print_email(app, id):
    email = app.get_email(id)
    print("\r\nEmail Id: %s" % id)
    print(unicode(email))

def print_url(app, id):
    url = app.get_url(id)
    print("\r\nUrl: %s" % id)
    print(unicode(url))
    

#
# Contact
#

# contact

contact = Contact(fbx=app)
contact.first_name = "John"
contact.last_name = "Doe"
contact.display_name = "DOE, John"
contact.notes = "Fake contact"

print("\r\nCreate contact :")
print(contact)
contact = app.new_contact(contact)
contact_id = ncontact.id
print_contact(app,contact_id)

# number

number = Number()
number.contact_id = contact_id
number.number = '1234567890'
number.type = 'mobile'
print("\r\nCreate number :")
print("===============")
print(number)
nnumber = contact.add_number(number)
print(nnumber)

quit()

number_id = nnumber.id
print_number(app,nnumber.id)
print_contact(app,nnumber.contact_id)
print_contact(app,contact_id)


number = Number()
number.contact_id = contact_id
number.number = '1234567891'
number.type = 'fixed'
print("\r\nCreate number :")
print("===============")
print(number)
nnumber = app.new_number(number)
number1_id = nnumber.id
print_number(app,number1_id)
print_contact(app,nnumber.contact_id)
print_contact(app,contact_id)

contact = app.get_contact(contact_id)
for number in contact.numbers:
    number_id = number.id
    print("\r\nDelete number id: %s" % number_id)
    print("=====================")
    print(number)
    print(app.delete_number(number_id))
    print_number(app,number_id)
print_contact(app,contact_id)

# address

address = Address()
address.contact_id = contact_id
address.city = 'Bordeaux'
address.country = 'France'
address.zip_code = '33000'
address.street = 'rue du Marechal Juin'
address.number = '10'
address.type = 'work'
print("\r\nCreate address :")
print("================")
print(unicode(address))
naddress = app.new_address(address)
print(unicode(naddress))
address_id = naddress.id
print_address(app,naddress.id)
print_contact(app,naddress.contact_id)
print_contact(app,contact_id)

# email

email = Email()
email.contact_id = contact_id
email.email = 'alain.bidon@free.fr'
email.type = 'work'
print("\r\nCreate email :")
print(email)
nemail = app.new_email(email)
print(nemail)
email_id = nemail.id
print_email(app,nemail.id)
print_contact(app,nemail.contact_id)
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

