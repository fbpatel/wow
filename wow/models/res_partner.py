# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    def _compute_im_status(self):
        super(Partner, self)._compute_im_status()
        sm_id = self.env['ir.model.data'].xmlid_to_res_id("wow.partner_sm")
        for partner in self:
            if partner.id == sm_id:
                partner.im_status = 'online'
