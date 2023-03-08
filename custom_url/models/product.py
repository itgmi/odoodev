from odoo import models, fields, api
from odoo.http import request
from bs4 import BeautifulSoup
import requests
import base64


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

    def get_image_from_mall(self):
        if self.default_code:
            if self.categ_id:
                name = self.categ_id.complete_name
                condition = 'SIEMENS'
                if condition in name:
                    mlfb = self.default_code
                    url = f"https://mall.industry.siemens.com/mall/es/MX/Catalog/Product/?mlfb={mlfb}&SiepCountryCode=MX"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        img_element = soup.find('div', {'class':
                                                            'pictureArea'})
                        img_url = img_element.find('img')['src']
                    if img_url:
                        data = base64.b64encode(
                            requests.get(img_url.strip(), headers=headers).content).replace(b'\n', b'')
                        self.image_1920 = data

