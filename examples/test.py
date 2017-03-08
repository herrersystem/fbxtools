#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import Fbx
from fbxtools.fbxo import Contact,Number,Email,Address,Url,Contacts,Calls,Call,Groups,Group,LanHost,LanHosts

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
	
@app.api.call('/contact/')
def get_contacts(data):
    return {'data': data, 'is_json': True}


def test_api(url,args={},data={},method='GET'):	
	@app.api.call(url,method=method)
	def wrapper():
		if data == {}:
			if args == {}:
				return {}
			else:
				return {'args':args}
		else:
			if args == {}:
				return {'data': data, 'is_json': True}
			else:
				return {'args':args,'data': data, 'is_json': True}

	return wrapper()


def compare_obj(obj1,obj2):
	testOk = True
	for field_name in obj1._attribs:
		try:
			value = getattr(obj1,field_name)
		except:
			continue
		try:
			nvalue = getattr(obj2,field_name)
			if nvalue != value:
				testOk = False
		except:
			testOk = False
	return testOk

def main():

	# Permissions
	print("\r\nPermisssions:")
	print("=============")
	print(app.permissions)
	
	# Etat Freebox
	print("\r\nEtat Freebox:")
	print("=============")
	print(app.boxinfos)
	print("")
	
	# Interfaces
	print("\r\nInterfaces reseau:")
	print("==================")
	for interface in app.interfaces:
		print(interface)
	print("")
	
	# Lan hosts
	interface = app.interfaces[0].name
	print("\r\nHosts interface %s (active):\r\n" % interface)
	lanhosts = app.get_lanhosts(args={'interface': interface})
	for lanhost in lanhosts:
		if lanhost.active:
			print("%s: %s, %s" % (lanhost.l2ident.id,lanhost.primary_name,lanhost.vendor_name))

	# Test contacts and related objects
	print("\r\nTest contacts and related objects")
	print("=================================")
	
	# Group
	
	for group in app.groups:
		if not (group.id in (1,2)):
			#app.delete_group(group.id)
			pass

	# test create group
	group = Group()
	group.name = "Test"
	ngroup = app.new_group(group)
	testOk = compare_obj(group,ngroup)
	if testOk:
		testOk = False
		groups = app.groups
		for agroup in groups:
			if compare_obj(group,agroup):
				testOk = True
				print("Get groups: %s" % testOk)
				break
	print("Create group: %s" % testOk)
	if testOk:
		# test update group
		group.name = "Groupe_test"
		app.set_group(ngroup.id,group)
		ngroup = app.get_group(ngroup.id)
		testOk = compare_obj(group,ngroup)
		print("Update group: %s" % testOk)
		# test delete group
		testOk = app.delete_group(ngroup.id)
		if testOk:
			for agroup in groups:
				if compare_obj(group,agroup):
					testOk = False
		print("Delete group: %s" % testOk)
			
	# Call
	
	# test get calls
	calls = app.calls
	if len(calls)>1:
		print("Get calls: %s" % True)
		# test update call
		call = calls[0]
		new = call.new
		ncall = Call()
		ncall.new = not call.new
		app.set_call(call.id,ncall)
		call = app.get_call(call.id)
		if call.new == ncall.new:
			testOk = True
		else:
			testOk = False
		ncall.new = new
		app.set_call(call.id,ncall)
		call = app.get_call(call.id)
		print("Update call: %s" % testOk)
		
	# Contact

	# test create contact
	contact = Contact()
	contact.first_name = "John"
	contact.last_name = "DOE"
	contact.display_name = "DOE, John"
	contact.notes = "Contact de test"
	contact.company = "A world Company"
	ncontact = app.new_contact(contact)
	testOk = compare_obj(contact,ncontact)
	print("Create contact: %s" % testOk)
	# test update contact
	contact.notes = "Contact de test : John DOE"
	app.set_contact(ncontact.id,contact)
	ncontact = app.get_contact(ncontact.id)
	testOk = compare_obj(contact,ncontact)
	print("Update contact: %s" % testOk)
	# test delete contact
	testOk = app.delete_contact(ncontact.id)
	print("Delete contact: %s" % testOk)

	# Number

	# test create number
	number = Number()
	ncontact = app.new_contact(contact)
	number.type = 'fixed'
	number.number = '1234567890'
	number.contact_id = ncontact.id
	nnumber = app.new_number(number)
	testOk = compare_obj(number,nnumber)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		nnumber = ncontact.numbers[0]
		testOk =  compare_obj(number,nnumber)
	print("Create number: %s" % testOk)
	# test update number
	number.number = '1234567891'
	app.set_number(nnumber.id,number)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		nnumber = ncontact.numbers[0]
		testOk =  compare_obj(number,nnumber)
	print("Update number: %s" % testOk)
	# test delete contact
	testOk = app.delete_number(nnumber.id)
	print("Delete number: %s" % testOk)

	# Address

	# test create address
	address = Address()
	address.contact_id = ncontact.id
	address.city = 'Bordeaux'
	address.country = 'France'
	address.zip_code = '33000'
	address.street = 'rue du Marechal Juin'
	address.number = '10'
	address.type = 'work'
	naddress = app.new_address(address)
	testOk = compare_obj(address,naddress)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		naddress = ncontact.addresses[0]
		testOk =  compare_obj(address,naddress)
	print("Create address: %s" % testOk)
	# test update address
	address.number = '10bis'
	app.set_address(naddress.id,address)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		naddress = ncontact.addresses[0]
		testOk =  compare_obj(address,naddress)
	print("Update address: %s" % testOk)
	# test delete contact
	testOk = app.delete_address(naddress.id)
	print("Delete address: %s" % testOk)

	# Email

	# test create email
	email = Email()
	email.contact_id = ncontact.id
	email.email = 'john.doe@free.fr'
	email.type = 'work'
	nemail = app.new_email(email)
	testOk = compare_obj(email,nemail)
	print("Create email: %s" % testOk)
	# test update email
	email.type = 'home'
	app.set_email(nemail.id,email)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		nemail = ncontact.emails[0]
		testOk =  compare_obj(email,nemail)
	print("Update email: %s" % testOk)
	# test delete email
	testOk = app.delete_email(nemail.id)
	print("Delete email: %s" % testOk)

	# Url

	# test create url
	url = Url()
	url.contact_id = ncontact.id
	url.url = 'http://john.doe.free.fr'
	url.type = 'profile'
	nurl = app.new_url(url)
	testOk = compare_obj(url,nurl)
	print("Create url: %s" % testOk)
	# test update url
	url.type = 'site'
	app.set_url(nurl.id,url)
	if testOk:
		ncontact = app.get_contact(ncontact.id)
		nurl = ncontact.urls[0]
		testOk =  compare_obj(url,nurl)
	print("Update url: %s" % testOk)
	# test delete url
	testOk = app.delete_url(nurl.id)
	print("Delete url: %s" % testOk)

	# Contacts
	
	# test get contacts
	testOk = False
	contacts = app.contacts
	for acontact in contacts:
		if acontact.id == ncontact.id:
			testOk = True
	print("Get contacts: %s" % testOk)
	

	# Clean
	
	testOk = app.delete_contact(ncontact.id)


if __name__ == "__main__":

    main()

    quit()

