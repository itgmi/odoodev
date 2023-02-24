from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_available = fields.Float(compute='_compute_stock_available')

    def _compute_stock_available(self):
        stocks = self.env['stock.quant'].search([])
        for record in self:
            count = 0
            for rec in stocks:
                if rec.product_id.product_tmpl_id.id == record.id:
                    if rec.location_id.usage == 'supplier':
                        count += rec.inventory_quantity_auto_apply
            record.stock_available = count

    def action_open_stocks_vendor(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.quant',
            'name': self.name,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [('location_id.usage', '=', 'supplier'),
                       ('product_id', '=', self.product_variant_ids.id)]
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock_available = fields.Float(compute='_compute_stock_available_line')

    @api.depends(
        'product_id', 'customer_lead', 'product_uom_qty', 'product_uom',
        'order_id.commitment_date',
        'move_ids', 'move_ids.forecast_expected_date',
        'move_ids.forecast_availability')
    def _compute_stock_available_line(self):
        for rec in self:
            rec.stock_available = rec.product_template_id.stock_available
