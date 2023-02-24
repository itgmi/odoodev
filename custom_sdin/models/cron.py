from odoo import models, fields


class IrCron(models.Model):
    _inherit = 'ir.cron'

    record = fields.Text("Records")
    logs = fields.Text("Latest Log")
