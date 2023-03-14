from odoo import models, fields, api
LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'done', 'cancel'}
}
READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel'}
}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    parent_id = fields.Many2one('res.partner', related='partner_id.parent_id')
    partner_invoice_id = fields.Many2one(
        comodel_name='res.partner',
        string="Invoice Address",
        compute='_compute_partner_invoice_id',
        store=True, readonly=False, required=True, precompute=True,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id), "
               "('parent_id', '=', partner_id), "
               "('type', '=', 'invoice')]")
    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string="Delivery Address",
        compute='_compute_partner_shipping_id',
        store=True, readonly=False, required=True, precompute=True,
        states=LOCKED_FIELD_STATES,
        domain="['|', ('company_id', '=', False), "
               "('company_id', '=', company_id), '|',"
               "('parent_id', '=', partner_id), '&',  "
               "('parent_id', '=', parent_id), "
               "('parent_id', '!=', False), "
               "('type', '=', 'delivery')]")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False, change_default=True, index=True,
        tracking=1,
        states=READONLY_FIELD_STATES,
        domain="[('type', '!=', 'private'), "
               "('company_id', 'in', (False, company_id)), "
               "('type', '=', 'contact')]")

    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        super()._compute_partner_invoice_id()
        for order in self:
            if order.partner_id.parent_id:
                order.partner_invoice_id = order.partner_id.parent_id.id
            else:
                order.partner_invoice_id = order.partner_id.address_get(
                    ['invoice'])['invoice'] if order.partner_id else False

    @api.onchange('partner_shipping_id')
    def _on_change_partner_shipping_id(self):
        if self.partner_id and self.partner_shipping_id:
            if self.partner_id.id != self.partner_shipping_id.id:
                if not self.partner_shipping_id.parent_id:
                    if not self.partner_id.parent_id:
                        self.partner_shipping_id.parent_id = self.partner_id.id
                    elif self.partner_id.parent_id:
                        self.partner_shipping_id.parent_id = \
                            self.partner_id.parent_id.id
