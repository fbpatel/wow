# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'WowBot',
    'version': '1.0',
    'category': 'Discuss',
    'summary': 'Add WowBot in discussions',
    'description': "",
    'website': 'https://www.odoo.com/page/discuss',
    'depends': ['mail', 'hr', 'account_accountant', 'sale', 'project', 'sign', 'documents'],
    'installable': True,
    'application': False,
    #'auto_install': True,
    'data': [
        'views/assets.xml',
        'views/res_users_views.xml',
        'data/wowbot_data.xml',
    ],
    'qweb': [
        'views/discuss.xml',
    ],
}
