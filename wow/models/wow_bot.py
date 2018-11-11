# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
import random

from dateutil.relativedelta import relativedelta
from odoo import models, fields


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
