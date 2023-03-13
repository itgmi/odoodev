from odoo import models, fields, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rfq_button_products = fields.Boolean(config_parameter='custom_rfq.rfq_button_products')
    rfq_button_cart = fields.Boolean(config_parameter='custom_rfq.rfq_button_cart')
    rfq_button_cart_website_ids = fields.Many2many('website')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        websites = params.get_param('custom_rfq.rfq_button_cart_website_ids')
        websites = literal_eval(websites) if websites else []
        res.update(
            rfq_button_cart_website_ids=[[6, False, websites]]
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('custom_rfq.rfq_button_cart_website_ids', self.rfq_button_cart_website_ids.ids)
        return res

    def rfq_button_cart_website_id(self):
        websites = self.env['ir.config_parameter'].sudo().get_param(
            'custom_rfq.rfq_button_cart_website_ids')
        websites = literal_eval(websites) if websites else []
        return websites
