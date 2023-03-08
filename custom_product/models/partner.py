from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_usage_sales = fields.Selection(
        selection=[
            ('G01', 'Acquisition of merchandise'),
            ('G02', 'Returns, discounts or bonuses'),
            ('G03', 'General expenses'),
            ('I01', 'Constructions'),
            ('I02', 'Office furniture and equipment investment'),
            ('I03', 'Transportation equipment'),
            ('I04', 'Computer equipment and accessories'),
            ('I05', 'Dices, dies, molds, matrices and tooling'),
            ('I06', 'Telephone communications'),
            ('I07', 'Satellite communications'),
            ('I08', 'Other machinery and equipment'),
            ('D01', 'Medical, dental and hospital expenses.'),
            ('D02', 'Medical expenses for disability'),
            ('D03', 'Funeral expenses'),
            ('D04', 'Donations'),
            ('D05',
             'Real interest effectively paid for mortgage loans (room house)'),
            ('D06', 'Voluntary contributions to SAR'),
            ('D07', 'Medical insurance premiums'),
            ('D08', 'Mandatory School Transportation Expenses'),
            ('D09',
             'Deposits in savings accounts, premiums based on pension plans.'),
            ('D10', 'Payments for educational services (Colegiatura)'),
            ('P01', 'To define'),
        ],
        string="Usage",
        default='P01',
        help="Used in CFDI 3.3 to express the key to the usage that will gives the receiver to this invoice. This "
             "value is defined by the customer.\nNote: It is not cause for cancellation if the key set is not the usage "
             "that will give the receiver of the document.")
    l10n_mx_edi_usage_purchase = fields.Selection(
        selection=[
            ('G01', 'Acquisition of merchandise'),
            ('G02', 'Returns, discounts or bonuses'),
            ('G03', 'General expenses'),
            ('I01', 'Constructions'),
            ('I02', 'Office furniture and equipment investment'),
            ('I03', 'Transportation equipment'),
            ('I04', 'Computer equipment and accessories'),
            ('I05', 'Dices, dies, molds, matrices and tooling'),
            ('I06', 'Telephone communications'),
            ('I07', 'Satellite communications'),
            ('I08', 'Other machinery and equipment'),
            ('D01', 'Medical, dental and hospital expenses.'),
            ('D02', 'Medical expenses for disability'),
            ('D03', 'Funeral expenses'),
            ('D04', 'Donations'),
            ('D05',
             'Real interest effectively paid for mortgage loans (room house)'),
            ('D06', 'Voluntary contributions to SAR'),
            ('D07', 'Medical insurance premiums'),
            ('D08', 'Mandatory School Transportation Expenses'),
            ('D09',
             'Deposits in savings accounts, premiums based on pension plans.'),
            ('D10', 'Payments for educational services (Colegiatura)'),
            ('P01', 'To define'),
        ],
        string="Usage",
        default='P01',
        help="Used in CFDI 3.3 to express the key to the usage that will gives the receiver to this invoice. This "
             "value is defined by the customer.\nNote: It is not cause for cancellation if the key set is not the usage "
             "that will give the receiver of the document.")
    l10n_mx_edi_payment_method_id_sales = fields.Many2one(
        comodel_name='l10n_mx_edi.payment.method',
        string="Payment Way",
        help="Indicates the way the payment was/will be received, where the options could be: "
             "Cash, Nominal Check, Credit Card, etc.")
    l10n_mx_edi_payment_method_purchase = fields.Many2one(
        comodel_name='l10n_mx_edi.payment.method',
        string="Payment Way",
        help="Indicates the way the payment was/will be received, where the options could be: "
             "Cash, Nominal Check, Credit Card, etc.")
    l10n_mx_edi_payment_policy_sales = fields.Selection(string='Payment Policy',
                                                  selection=[('PPD', 'PPD'),
                                                             ('PUE', 'PUE')])
    l10n_mx_edi_payment_policy_purchase = fields.Selection(
        string='Payment Policy',
        selection=[('PPD', 'PPD'),
                   ('PUE', 'PUE')])
    channel_id = fields.Many2one('channels.gr')
    types_id = fields.Many2one('types.gr', 'Type')
    city_id = fields.Many2one(comodel_name='res.city', string='City ID',
                              domain="[('state_id', '=', state_id)]")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res:
            for rec in res:
                if rec.parent_id and rec.type == 'invoice':
                    rec.unlink()
        return res

    @api.onchange('vat')
    def _on_change_vat(self):
        if self.vat:
            self.vat = self.vat.upper()

    @api.onchange('email')
    def _on_change_email(self):
        if self.email:
            self.email = self.email.lower()

    @api.onchange('website')
    def _on_change_website(self):
        if self.website:
            self.website = self.website.lower()

    @api.onchange('name')
    def _on_change_name(self):
        if self.name:
            self.name = self.name.title()

    @api.onchange('street_name')
    def _on_change_street_name(self):
        if self.street_name:
            self.street_name = self.street_name.title()

    @api.onchange('street2')
    def _on_change_street2(self):
        if self.street2:
            self.street2 = self.street2.title()

    @api.onchange('street')
    def _on_change_street(self):
        if self.street:
            self.street = self.street.title()

    @api.onchange('l10n_mx_edi_colony')
    def _on_change_l10n_mx_edi_colony(self):
        if self.l10n_mx_edi_colony:
            self.l10n_mx_edi_colony = self.l10n_mx_edi_colony.title()
