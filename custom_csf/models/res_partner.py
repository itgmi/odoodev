from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    schedule_for_delivery = fields.Html()
