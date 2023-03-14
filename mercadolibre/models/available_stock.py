from odoo import models, fields


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
    mer_price = fields.Float('Price')
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
