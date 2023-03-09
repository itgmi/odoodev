from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    request_quote = fields.Boolean(default=True)
    request_website_ids = fields.Many2many('website',
                                           'product_template_request_website_rel',
                                           'product_template_id',)
