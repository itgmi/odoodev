from odoo import models, fields


class CreateQuotation(models.TransientModel):
    _name = 'create.quotation'
    _description = 'Create Quotation'

    partner_id = fields.Many2one('res.partner', 'Customer')

    def action_create_quotation(self):
        products = self._context.get('active_ids')
        partner = self.partner_id.id
        vals = []
        for record in products:
            product = self.env['product.product'].search([
                ('product_tmpl_id', '=', int(record))], limit=1)
            vals.append((0, 0, {
                'product_id': product.id,
            }))
        sale_order = self.env['sale.order'].create({
            'partner_id': partner,
            'order_line': vals,
        })
        return {
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': sale_order.id,
            'type': 'ir.actions.act_window',
        }
