from odoo import models, fields


class User(models.Model):
    _inherit = 'res.users'

    upload_stock = fields.Boolean()
    location_id = fields.Many2one('stock.location', 'Stock Location')
