# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import io
import time
import uuid

from email.utils import formataddr
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from werkzeug.urls import url_join
from random import randint

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    @api.multi
    def action_completed(self):
        super(SignRequestItem, self).action_completed()
        if self.id == self.env.ref('wow.fp_sign_request_item').id:
            user_channels = self.env['mail.channel.partner'].sudo().search([
                ('partner_id', '=', self.env.ref('base.partner_admin').id),
            ]).mapped('channel_id')
            sm_channels = self.env['mail.channel.partner'].sudo().search([
                ('partner_id', '=', self.env.ref('wow.partner_sm').id),
            ]).mapped('channel_id')
            channel = (user_channels & sm_channels).filtered(lambda chan: chan.channel_type == 'chat')
            self.env['wow.bot'].sudo(self.env.ref('base.user_admin'))._apply_logic(channel, {})
