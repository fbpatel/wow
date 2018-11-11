from odoo import fields, models

from odoo.addons.base.models import ir_cron
from odoo.service import server
from dateutil.relativedelta import relativedelta

server.SLEEP_INTERVAL = 8  # we need ultra fast crons
ir_cron._intervalTypes['seconds'] = lambda interval: relativedelta(seconds=interval)


class ir_cron(models.Model):
    _inherit = 'ir.cron'
    interval_type = fields.Selection(selection_add=[('seconds', 'Seconds')])

