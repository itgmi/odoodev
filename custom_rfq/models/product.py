from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    request_quote = fields.Boolean(default=True)
