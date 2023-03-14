from odoo import models, fields


class AvailableStock(models.Model):
    _name = 'available.stock'
    _description = 'Available Stock'

    product_id = fields.Many2one('product.product')
    location_id = fields.Many2one('stock.location')
    free_qty = fields.Float()

    def sample_function(self):
        stock = self.env['product.product'].search([])
        available = self.env['available.stock'].search([])
        vals = []
        for rec in available:
            vals.append(rec.product_id.id)
        for recs in stock:
            if recs.id not in vals:
                self.env['available.stock'].create({
                    'product_id': recs.id,
                    'free_qty': recs.free_qty,
                })
            else:
                record = self.env['available.stock'].search([
                    ('product_id', '=', recs.id)])
                record.write({
                    'free_qty': recs.free_qty,
                })
        return {
            'name': 'Available Quantity',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'available.stock',
            'type': 'ir.actions.act_window',
        }
