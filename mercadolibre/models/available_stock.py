from odoo import models, fields


class AvailableStock(models.Model):
    _name = 'available.stock'
    _description = 'Available Stock'

    product_id = fields.Many2one('product.product')
    location_id = fields.Many2one('stock.location')
    free_qty = fields.Float()

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
            'name': 'Available Quantity',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'available.stock',
            'type': 'ir.actions.act_window',
        }
