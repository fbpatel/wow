# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
import random

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class WowBot(models.AbstractModel):
    _name = 'wow.bot'
    _description = 'Wow Bot'

    def _apply_logic(self, record, values):
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        sm_user = self.env.ref("wow.user_sm")
        if len(record) != 1 or values.get("author_id") == sm_id:
            return
        if self._is_sm_in_private_channel(record):
            # message_body = values.get("body", "").replace(u'\xa0', u' ').strip().lower().strip(".?!")
            state = self.env.user.wowbot_state
            answers = self._get_answer(state)
            if answers:
                Deferred = self.env['deferred.message'].sudo()
                now = fields.Datetime.now()
                count = 0
                self.env.user.wowbot_state = 'pending'
                for (delay, state, body) in answers:
                    count += delay
                    Deferred.create({
                        'body': body,
                        'time': now + relativedelta(seconds=count),
                        'channel_id': record.id,
                        'state': state,
                        'user_id': self.env.user.id,
                    })

    def _get_answer(self, state, key=None):
        # onboarding
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        request_id = self.env.ref('wow.fp_sign_request_item').id
        token = self.env.ref('wow.fp_sign_request_item').access_token
        url = "%s/sign/document/%s/%s" % (base_url, request_id, token)
        answers = {
            'requested': [(10, 'prices', "I already reviewed prices")],
            'prices': [(10, 'link', 'Here it is: <a href="%s">%s</a>' % (url,url))],
            'link': [(15, 'thanks', "Thanks, you saved me. I've forwarded the bill to accounting. Can we pay it before end of week?")],
            'thanks': [(5, 'good', "Thanks, good luck for your event...")],
            'good': [
                (15, 'end', "Ok, I'll let the hotel know"),
                (10, 'end', "they are nervous about having that many people coming :)")
            ],
        }
        if state in answers:
            return answers[state]
        return False

    def _is_sm_in_private_channel(self, record):
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        if record._name == 'mail.channel' and record.channel_type == 'chat':
            return sm_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False

    @api.model
    def init_wow_for_fp(self):
        fp = self.env.ref("base.user_admin")
        partner = fp.partner_id
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        sm_user = self.env.ref("wow.user_sm")
        # A little cleaning, in case of the channel already exists
        partners_to = [partner.id, sm_id]
        self.env.cr.execute("""
            SELECT P.channel_id as channel_id
            FROM mail_channel C, mail_channel_partner P
            WHERE P.channel_id = C.id
                AND C.public LIKE 'private'
                AND P.partner_id IN %s
                AND channel_type LIKE 'chat'
            GROUP BY P.channel_id
            HAVING array_agg(P.partner_id ORDER BY P.partner_id) = %s
        """, (tuple(partners_to), sorted(list(partners_to)),))
        result = self.env.cr.dictfetchall()
        if result:
            self.env['mail.channel'].browse(result[0].get('channel_id')).unlink()
        #create channel
        channel = self.env['mail.channel'].with_context({"mail_create_nosubscribe": True}).create({
            'channel_partner_ids': [(4, partner.id), (4, sm_id)],
            'public': 'private',
            'channel_type': 'chat',
            'email_send': False,
            'name': 'OdooBot'
        })
        self.sm_message(channel, "Hello")
        self.sm_message(channel, "Are you available? It's urgent.")
        self.sm_message(channel, "The hotel needs your signature for 300 extra attendees before we start. Can you sign it now, we start in an hour?")
        fp.wowbot_state = 'requested'
        return True

    def sm_message(self, channel, message):
        sm_user = self.env.ref("wow.user_sm")
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        channel.sudo(sm_user).message_post(body=message, author_id=sm_id, message_type="comment", subtype="mail.mt_comment")
