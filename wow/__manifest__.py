# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'WOW Bot',
    'version': '1.0',
    'category': 'Discuss',
    'summary': 'Add WowBot in discussions',
    'description': "",
    'website': 'https://www.odoo.com/page/discuss',
    'depends': ['hr_expense', 'account_accountant', 'sale_management', 'hr_timesheet', 'sign', 'documents', 'account_invoice_extract', 'website'],
    'installable': True,
    'application': False,
    #'auto_install': True,
    'data': [
        'views/res_users_views.xml',
        'data/wowbot_data.xml',
    ],
    'qweb': [
        'views/discuss.xml',
    ],
}
