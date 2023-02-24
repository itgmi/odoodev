from odoo import models, fields, api
from odoo.http import request


class ProductTemp(models.Model):
    _inherit = 'product.template'

    public_url_sp = fields.Char(string='Public URL', compute='_compute_public_url', store=True)

    @api.depends('image_1920')
    def _compute_public_url(self):
        url = f"{request.httprequest.host_url[:-1]}"
        for record in self:
            if record.image_1920:
                attachment = self.env['ir.attachment'].create({
                    'name': str(record.id),
                    'type': 'binary',
                    'public': True,
                    'datas': record.image_1920,
                    'res_model': self._name,
                    'res_id': record.id,
                })
                public_url = '{}/web/image/ir.attachment/{}/datas'.format(url,
                                                                          attachment.id)
                record.public_url_sp = public_url
            else:
                record.public_url_sp = ''
