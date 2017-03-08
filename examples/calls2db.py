#!/usr/bin/env python
# -*- coding: utf8 -*-

from fbxtools.fbx import *
import time
import datetime

import mysql.connector
from mysql.connector import errorcode

import sys

mute = False

for arg in sys.argv :
	if arg == "--mute" :
		mute = True

## Initialize and connect app.
#app = Fbx('http://192.168.0.254/api/v3')
app = Fbx('https://afer77.freeboxos.fr:1459/api/v3')
app.get_session_token()


def get_cursor() :
	try :
		cnx = mysql.connector.connect(user='freebox', password='freebox',host='192.168.0.6', database='FREEBOX')
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
		return (0,0)
	else :
		cursor = cnx.cursor()
	return (cnx,cursor)



if __name__ == "__main__":

	#
	# update calls
	#

	nbcalls = 0
	nbinserts = 0
		
	(cnx,cursor) = get_cursor()
	
	query = "SELECT `id` FROM `calls` ORDER BY `id` DESC LIMIT 1;"
	cursor.execute(query)
	for row in cursor :
		last_id = row[0]
	
	for call in app.calls:
		nbcalls += 1
		st = str(call.datetime)
		curr_id = int(call.id)
		if curr_id > last_id :
			nbinserts += 1
			query = "INSERT INTO `FREEBOX`.`calls` (`id`, `type`, `datetime`, `number`, `name`, `duration`, `new`, `contact_id`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');"\
				% (call.id,call.type,st,call.number,call.name,call.duration,call.new,call.contact_id)
			print (query)
			cursor.execute(query)
	cnx.commit()
	cnx.close()
	
	if mute == False :
		print ("\r\nNb calls: %d, nb inserts: %d\r\n" % (nbcalls,nbinserts))
		
	quit()
	
'''
--
-- Structure de la table `calls`
--

CREATE TABLE IF NOT EXISTS `calls` (
  `id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `number` varchar(40) NOT NULL,
  `name` varchar(80) NOT NULL,
  `duration` int(11) NOT NULL,
  `new` tinyint(1) NOT NULL,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

