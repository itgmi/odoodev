from odoo import models, fields


class IrCron(models.Model):
    _inherit = 'ir.cron'

    refresh_logs = fields.Text("Latest Log")
