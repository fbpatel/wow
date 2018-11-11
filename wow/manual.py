#!/usr/bin/python

import xmlrpclib
import csv

db       = 'trunk'
url      = 'localhost:8069'
username = 'admin'
password = 'admin'

common = xmlrpclib.ServerProxy('http://'+url+'/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('http://'+url+'/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password, 'mail.channel', 'init_wow', [])

