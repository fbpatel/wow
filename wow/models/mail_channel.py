# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
import time
from dateutil.relativedelta import relativedelta


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _message_post_after_hook(self, message, values, **kwargs):
        self.env['wow.bot']._apply_logic(self, values)
        return super(Channel, self)._message_post_after_hook(message, values, **kwargs)

