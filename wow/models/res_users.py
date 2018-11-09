# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'
    wowbot_state = fields.Selection(
        [
            ('not_initialized', 'Not initialized'),
            ('writing', 'Writing'),
            ('pending', 'Pending'),
            ('requested', '1re'),
            ('prices', '2pr'),
            ('link', '3li'),
            ('thanks', '4th'),
            ('good', '5go'),
            ('end', '6en'),
            ('disabled', 'Disabled'),
        ], string="Wow Status", readonly=True, required=True, default="disabled")
