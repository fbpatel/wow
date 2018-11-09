import odoorpc
from pprint import pprint

odoo = odoorpc.ODOO('127.0.0.1', port=8069)
print(odoo.db.list()[0])

odoo.login(odoo.db.list()[0], 'fp', 'dummy')
data = odoo.execute('mail.channel', 'init_wow')
