from odoo import models, fields, api
import os
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_order = fields.Char()


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_order = fields.Char(related='line_ids.sale_line_ids.order_id.customer_order')
    carrier_tracking_ref = fields.Char(compute='_load_carrier_tracking_ref',
                                       store=True)

    @api.depends('partner_id')
    def _load_carrier_tracking_ref(self):
        for rec in self:
            if rec:
                if rec.line_ids.sale_line_ids.order_id.picking_ids:
                    list = []
                    count = 0
                    for recs in rec.line_ids.sale_line_ids.order_id.picking_ids:
                        count += 1
                        self.carrier_tracking_ref = recs.carrier_tracking_ref
                    if count > 1:
                        for recs in rec.line_ids.sale_line_ids.order_id.picking_ids:
                            list.append(recs.carrier_tracking_ref)
                        self.carrier_tracking_ref = list


class UploadDocs(models.Model):
    _name = 'upload.docs'
    _description = 'Upload Docs'

    file = fields.Binary()
    file_name = fields.Char()

    def upload_docs(self):
        split_tup = os.path.splitext(self.file_name)
        name = split_tup[0]
        file_extension = split_tup[1]
        if file_extension != '.pdf':
            raise ValidationError('Choose Valid File')
        else:
            record = (self.env['sale.order'].browse(
                [self._context.get('active_id')]))
            if record:
                record.customer_order = name
                attachment = self.env['ir.attachment'].create({
                    'name': self.file_name,
                    'type': 'binary',
                    'datas': self.file,
                    'res_model': record._name,
                    'res_id': record.id,
                    'mimetype': 'application/pdf'
                })
                record.message_post(body=self.file_name,
                                    attachment_ids=attachment.ids)
