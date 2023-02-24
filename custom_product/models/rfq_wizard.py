from odoo import models, fields


class CreateRfq(models.TransientModel):
    _name = 'create.rfq'
    _description = 'Create Rfq'

    partner_id = fields.Many2one('res.partner', 'Customer')

    def action_create_rfq(self):
        products = self._context.get('active_ids')
        partner = self.partner_id.id
        vals = []
        for record in products:
            product = self.env['product.product'].search([
                ('product_tmpl_id', '=', int(record))], limit=1)
            vals.append((0, 0, {
                'product_id': product.id,
            }))
        purchase_order = self.env['purchase.order'].create({
            'partner_id': partner,
            'order_line': vals,
        })
        return {
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': purchase_order.id,
            'type': 'ir.actions.act_window',
        }
