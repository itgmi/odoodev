from odoo import models, fields
import requests


class Product(models.Model):
    _inherit = 'product.template'

    mer_title = fields.Char('Title')
    mer_images = fields.Char('Images')
    mer_upc_ = fields.Char('UPC')
    mer_upc = fields.Selection([])
    mer_available_quantity = fields.Float('Available Quantity')
    mer_price = fields.Float('Price')
    mer_currency = fields.Selection([
        ("MXN", "MXN"),
        ("USD", "USD"),
    ], 'Currency', default='MXN')
    mer_currency_id = fields.Many2one('res.currency')
    mer_shipping_method = fields.Many2one('delivery.carrier')
    mer_condition = fields.Selection([
        ("new", "New"),
        ("used", "Used"),
        ("refurbished", "Refurbished")
        ], 'Condition')
    mer_description = fields.Text('Description')
    mer_listing_type = fields.Selection([
        ("classic", "Classic"),
        ("premium", "Premium")
        ], 'Listing Type', default='classic')
    mer_shipping_method = fields.Selection([
        ("Mercado Envíos", "Mercado Envíos")
    ], default='Mercado Envíos')
    mer_shipping_cost = fields.Selection([
        ("A cargo del comprador", "A cargo del comprador"),
        ("Ofreces envío gratis", "Ofreces envío gratis")
        ], 'Shipping Cost', default='A cargo del comprador')
    mer_local_pickup = fields.Selection([
        ("Acepto", "Acepto"),
        ("No Acepto", "No Acepto")
        ], 'Local Pickup', default='Acepto')
    mer_warranty_type = fields.Selection([
        ("Garantía del vendedor", "Garantía del vendedor"),
        ("Garantía de fábrica", "Garantía de fábrica"),
        ("Sin garantía", "Sin garantía")
        ], 'Warranty Type', default='Garantía del vendedor')
    mer_warranty_time = fields.Float('Warranty Time', default=6)
    mer_warranty_uom = fields.Selection([
        ("dias", "dias"),
        ("meses", "meses"),
        ("años", "años")
        ], 'Warranty Uom', default='meses')
    mer_brand = fields.Char('Brand')
    mer_mlm = fields.Char('Mlm')
    mer_category = fields.Char('Category')
    response = fields.Text('Response')

    def validate_product(self):
        company = self.env.company
        access_token = company.access_token
        payload = {}
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        url = f"https://api.mercadolibre.com/sites/MLM/domain_discovery/search?limit=1&q={self.name}"
        if self.name:
            response = requests.get(url, headers=headers, data=payload)
            if response.status_code == 200:
                self.response = response.text
                for rec in response.json():
                    self.mer_category = rec.get('category_id')
                self.mer_title = self.name
                self.mer_upc_ = self.barcode
                self.mer_price = self.list_price
                self.mer_available_quantity = self.qty_available
                self.mer_description = self.description_sale
                self.mer_images = self.image_url
                self.mer_currency = 'MXN'
                self.mer_warranty_uom = 'meses'
                self.mer_warranty_time = 6
                self.mer_warranty_type = 'Garantía del vendedor'
                self.mer_local_pickup = 'Acepto'
                self.mer_shipping_cost = 'A cargo del comprador'
                self.mer_shipping_method = 'Mercado Envíos'
                self.mer_listing_type = 'classic'
                self.mer_brand = self.name.split(" ")[0]

