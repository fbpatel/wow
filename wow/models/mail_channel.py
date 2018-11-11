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

    @api.model
    def init_wow(self):
        if self.env.user.wowbot_state == 'not_initialized':
            partner = self.env.user.partner_id
            sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
            sm_user = self.env.ref("wow.user_sm")
            channel = self.with_context({"mail_create_nosubscribe": True}).create({
                'channel_partner_ids': [(4, partner.id), (4, sm_id)],
                'public': 'private',
                'channel_type': 'chat',
                'email_send': False,
                'name': 'OdooBot'
            })
            Deferred = self.env['deferred.message'].sudo()
            now = fields.Datetime.now()
            self.env.user.wowbot_state = 'pending'
            Deferred.create({
                'body': "Hello",
                'time': now,
                'channel_id': channel.id,
                'state': 'writing',
                'sound': True,
                'user_id': self.env.user.id,
            })
            Deferred.create({
                'body': "Are you available? It's urgent.",
                'time': now + relativedelta(seconds=15),
                'channel_id': channel.id,
                'state': 'writing',
                'sound': True,
                'user_id': self.env.user.id,
            })
            Deferred.create({
                'body': "The hotel needs your signature for 300 extra attendees before we start. Can you sign it now, we start in an hour?",
                'time': now + relativedelta(seconds=40),
                'sound': True,
                'channel_id': channel.id,
                'state': 'requested',
                'user_id': self.env.user.id,
            })
        return True
