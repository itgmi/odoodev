from odoo import models, fields, api
import json
import requests


class ProductTemp(models.Model):
    _inherit = 'product.template'

    mlm = fields.Char(help='Store product mlm value.')
    dashless_code = fields.Char(help='Store product dashless code.')
    ecommerce_description = fields.Text(help='Enter detailed '
                                             'description to show in product '
                                             'view in website.')
    datasheet_url = fields.Char(help='Enter datasheet url '
                                     'to show in product '
                                     'view in website.')
    technical_info_url = fields.Char(help='Enter technical info url '
                                          'to show in product '
                                          'view in website.')
    manual_url = fields.Char(help='Enter manual_url to show in product '
                                  'view in website.')
    support_url = fields.Char(help='Enter support_url to show in product '
                                   'view in website.')
    image_url = fields.Char()
    product_downloads_url = fields.Char(help='Enter product_downloads_url '
                                             'to show in product '
                                             'view in website.')
    allowed_website_ids = fields.Many2many('website', help='Only shows '
                                           'product in selected websites')
    related_product_ids = fields.Many2many('product.product', help='Selected '
                                           'related products to show in '
                                           'sale order line')
    brand = fields.Char('Brand')
    long_default_code = fields.Char('Long Reference number')
    name = fields.Char('Name', index='trigram', required=True, translate=True, readonly=False, store=True, compute='_name_perfect')

    @api.depends('brand', 'default_code', 'long_default_code')
    def _name_perfect(self):
        for rec in self:
            if rec.brand and rec.default_code and rec.long_default_code:
                rec.name = rec.brand + ' - ' + rec.default_code + ' - ' + rec.long_default_code
            elif rec.brand and rec.default_code and not rec.long_default_code:
                rec.name = rec.brand + ' - ' + rec.default_code
            elif rec.brand and rec.long_default_code and not rec.default_code:
                rec.name = rec.brand + ' - ' + rec.long_default_code
            elif rec.long_default_code and rec.default_code and not rec.brand:
                rec.name = rec.default_code + ' - ' + rec.long_default_code
            elif rec.brand and not rec.default_code and not rec.long_default_code:
                rec.name = rec.brand
            elif rec.default_code and not rec.brand and not rec.long_default_code:
                rec.name = rec.default_code
            elif rec.long_default_code and not rec.default_code and not rec.brand:
                rec.name = rec.long_default_code

    @api.onchange('brand')
    def _on_change_brand(self):
        if self.brand:
            self.brand = self.brand.upper()

    @api.onchange('default_code')
    def _on_change_default_code(self):
        if self.default_code:
            self.default_code = self.default_code.upper()

    @api.onchange('long_default_code')
    def _on_change_long_default_code(self):
        if self.long_default_code:
            self.long_default_code = self.long_default_code.upper()

    @api.onchange('list_price')
    def http_request(self):
        """ The goal of this function is to post price update data
                    into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
                """
        url = "http://remoto.grupomi.com.mx:3000/api/odoo"
        price = self.list_price
        mlm = self.mlm
        default_code = self.default_code
        dashless_code = self.dashless_code
        payload = json.dumps({
            "change": "price",
            "value": price,
            "mlm": mlm,
            "internal": default_code,
            "dashless": dashless_code
        })
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("PUT", url, headers=headers, data=payload,
                         verify=False)


class Product(models.Model):
    _inherit = 'product.product'

    @api.onchange('lst_price')
    def http_request(self):
        """ The goal of this function is to post price update data
                    into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
                """
        url = "http://remoto.grupomi.com.mx:3000/api/odoo"
        price = self.lst_price
        mlm = self.mlm
        default_code = self.default_code
        dashless_code = self.dashless_code
        payload = json.dumps({
            "change": "price",
            "value": price,
            "mlm": mlm,
            "internal": default_code,
            "dashless": dashless_code
        })
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("PUT", url, headers=headers, data=payload,
                         verify=False)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    related_product_ids = fields.Many2many('product.product',
                                           related='product_template_id.'
                                                   'related_product_ids',
                                           help='To show related products '
                                                'in sale order line')


class StockValuationInherit(models.Model):
    _inherit = 'stock.valuation.layer'

    @api.model_create_multi
    def create(self, vals_list):
        """ The goal of this function super is to post stock update data
            into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
        """
        for vals in vals_list:
            product_id = vals.get('product_id')
            product = self.env['product.product'].browse(product_id)
            product_tmpl = self.env['product.template'].browse(product.product_tmpl_id.id)
            url = "http://remoto.grupomi.com.mx:3000/api/odoo"
            qty_available = product.qty_available
            mlm = product_tmpl.mlm
            payload = json.dumps({
                "change": "stock",
                "value": qty_available,
                "mlm": mlm,
                "internal": product_tmpl.default_code,
                "dashless": product_tmpl.dashless_code
            })
            headers = {
                'Content-Type': 'application/json'
            }

            requests.request("PUT", url, headers=headers, data=payload,
                             verify=False)
        return super(StockValuationInherit, self).create(vals_list)
