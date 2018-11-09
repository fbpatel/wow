# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.service import server

class Channel(models.Model):
    _name = 'deferred.message'

    body = fields.Char(string="deferred message body", required=True)
    time = fields.Datetime(string="when message should be send", required=True)
    channel_id = fields.Many2one('mail.channel', string='Channel', ondelete='cascade', required=True)
    state = fields.Char(string='State', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)

    @api.model
    def send(self):
        time = fields.Datetime.now()
        deferreds = self.search([('time', '<=', time)], order='time')
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        sm_user = self.env.ref("wow.user_sm")
        for deferred in deferreds:
            channel = deferred.channel_id
            message = deferred.body
            channel.sudo(sm_user).with_context({"mail_create_nosubscribe": True}).message_post(body=message, author_id=sm_id, message_type="comment", subtype="mail.mt_comment")
            deferred.user_id.wowbot_state = deferred.state
        deferreds.unlink()
