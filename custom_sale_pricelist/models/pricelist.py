from odoo import models, fields


class PriceList(models.Model):
    _inherit = 'product.pricelist'

    partner_id = fields.Many2one('res.partner')
