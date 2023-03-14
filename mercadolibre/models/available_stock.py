from odoo import models, fields, api
import base64
from io import BytesIO
from PIL import Image
import requests


class AvailableStock(models.Model):
    _name = 'available.stock'
    _description = 'Available Stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(related='product_id.name')
    product_id = fields.Many2one('product.product')
    location_id = fields.Many2one('stock.location')
    free_qty = fields.Float()
    mer_title = fields.Char('Title')
    mer_images = fields.Char('Images')
    mer_upc_ = fields.Char('UPC')
    mer_upc = fields.Selection([])
    mer_available_quantity = fields.Float('Available Quantity')
    mer_price = fields.Float('Price', compute='calculate_price', store=True)
    mer_currency = fields.Selection([
        ("MXN", "MXN"),
        ("USD", "USD"),
    ], 'Currency', default='MXN')
    mer_currency_id = fields.Many2one('res.currency', 'Currency',
                                      related='product_id.gr_currency_id')
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
    mer_brand = fields.Char('Brand', related='product_id.brand')
    mer_mlm = fields.Char('Mlm')
    mer_category = fields.Char('Category')
    sku = fields.Char(related='product_id.default_code', readonly=False)
    model = fields.Char(related='product_id.default_code', readonly=False)
    image_1928 = fields.Binary(related='product_id.image_1920')
    image_1929 = fields.Binary()
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    image_show = fields.Boolean(default=False)

    def validate_mercado(self):
        company = self.env.company
        access_token = company.access_token
        payload = {}
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        url = f"https://api.mercadolibre.com/sites/MLM/domain_discovery/search?limit=1&q={self.product_id.name}"
        if self.product_id:
            response = requests.get(url, headers=headers, data=payload)
            if response.status_code == 200:
                for rec in response.json():
                    self.mer_category = rec.get('category_id')
                self.mer_title = self.product_id.name
                self.mer_upc_ = self.product_id.barcode
                self.mer_description = self.product_id.description_sale
                self.mer_images = self.product_id.image_url
                self.mer_currency = 'MXN'
                self.mer_warranty_uom = 'meses'
                self.mer_warranty_time = 6
                self.mer_warranty_type = 'Garantía del vendedor'
                self.mer_local_pickup = 'Acepto'
                self.mer_shipping_cost = 'A cargo del comprador'
                self.mer_shipping_method = 'Mercado Envíos'
                self.mer_listing_type = 'classic'

    def change_image(self):
        if self.company_id.mlmark_image and self.image_1928:
            encoded_img2 = self.company_id.mlmark_image
            encoded_img1 = self.image_1928
            decoded_img1 = base64.b64decode(encoded_img1)
            decoded_img2 = base64.b64decode(encoded_img2)
            img1 = Image.open(BytesIO(decoded_img1))
            img2 = Image.open(BytesIO(decoded_img2))
            img2_resized = img2.resize((160, 112))
            img2_mask = img2_resized.convert('L')
            img2_mask = img2_mask.point(lambda x: 255 if x > 0 else 0,
                                        '1')
            img1.paste(img2_resized, (0, 0), mask=img2_mask)
            buffered = BytesIO()
            img1 = img1.convert('RGB')
            img1.save(buffered, format='JPEG')
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            self.image_1929 = img_str
            self.image_show = True

    def sample_function(self):
        stock = self.env['stock.quant'].search([])
        available = self.env['available.stock'].search([])
        vals = []
        for rec in available:
            vals.append(rec.product_id.id)
        for recs in stock:
            if recs.location_id.usage == 'internal':
                record = self.env['available.stock'].search([
                    ('product_id', '=', recs.product_id.id),
                    ('location_id', '=', recs.location_id.id)])
                if record:
                    record.write({
                        'free_qty': recs.available_quantity,
                    })
                else:
                    self.env['available.stock'].create({
                        'product_id': recs.product_id.id,
                        'location_id': recs.location_id.id,
                        'free_qty': recs.available_quantity,
                    })
        return {
            'name': 'MercadoLibre',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'available.stock',
            'type': 'ir.actions.act_window',
        }

    @api.depends('product_id', 'product_id.lst_price')
    def calculate_price(self):
        for rec in self:
            if rec.product_id.lst_price:
                rec.mer_price = rec.product_id.lst_price
            else:
                rec.mer_price = 0
