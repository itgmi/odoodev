from odoo import models, fields, api
import json
import requests
import re
from bs4 import BeautifulSoup


class ProductTemp(models.Model):
    _inherit = 'product.template'

    mlm = fields.Char(help='Store product mlm value.')
    dashless_code = fields.Char(help='Store product dashless code.')
    ecommerce_description = fields.Text(help='Enter detailed '
                                             'description to show in product '
                                             'view in website.')
    datasheet_url = fields.Char(help='Enter datasheet url '
                                     'to show in product '
                                     'view in website.')
    technical_info_url = fields.Char(help='Enter technical info url '
                                          'to show in product '
                                          'view in website.')
    manual_url = fields.Char(help='Enter manual_url to show in product '
                                  'view in website.')
    support_url = fields.Char(help='Enter support_url to show in product '
                                   'view in website.')
    image_url = fields.Char()
    product_downloads_url = fields.Char(help='Enter product_downloads_url '
                                             'to show in product '
                                             'view in website.')
    allowed_website_ids = fields.Many2many('website', help='Only shows '
                                           'product in selected websites')
    related_product_ids = fields.Many2many('product.product', help='Selected '
                                           'related products to show in '
                                           'sale order line')
    brand = fields.Char('Brand', readonly=True, store=True)
    long_default_code = fields.Char('Long Part#')
    name = fields.Char('Name', index='trigram', required=True, translate=True, readonly=False, store=True, compute='_name_perfect')
    description_gr = fields.Text('Description')

    def product_url_open(self):
        def google_search(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            results = soup.find_all("div", class_="g")
            for result in results:
                link = result.find("a")["href"]
                if not "webcache.googleusercontent.com" in link:
                    if marca in link:
                        return link
                    else:
                        return link

            return None
        if self.brand and self.default_code:
            marca = self.brand.lower() + '.com'
            partnum = self.default_code
            query = marca + ' ' + partnum
            result = google_search(query)
            if result:
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': result,
                }

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_default_code(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.default_code = template.product_variant_ids.default_code
        if self.product_variant_ids:
            for rec in self.product_variant_ids:
                rec.default_code = rec.product_tmpl_id.default_code

    def _set_default_code(self):
        for template in self:
            if len(template.product_variant_ids) >= 1:
                for rec in template.product_variant_ids:
                    rec.default_code = template.default_code

    @api.onchange('product_tag_ids')
    def _on_change_product_tag_ids(self):
        if self.product_tag_ids:
            for rec in self.product_tag_ids:
                rec._origin.name = rec._origin.name.lower()

    @api.onchange('description_gr')
    def _on_change_description(self):
        if self.description_gr:
            self.description_sale = self.description_gr
            self.description_purchase = self.description_sale

    @api.onchange('categ_id')
    def _on_change_categ_id(self):
        if self.categ_id:
            if self.categ_id.complete_name:
                name = self.categ_id.complete_name
                match = re.search(r"(?<=Active)\s*/\s*(\w+(?:\s+\w+)*)", name)
                if match:
                    siemens = match.group(1)
                    self.brand = siemens
                else:
                    match = re.search(r"(?<=Obsoleto)\s*/\s*(\w+(?:\s+\w+)*)", name)
                    if match:
                        siemens = match.group(1)
                        self.brand = siemens
                    else:
                        self.brand = ''

    @api.depends('brand', 'default_code', 'long_default_code')
    def _name_perfect(self):
        for rec in self:
            if rec.brand and rec.default_code and rec.long_default_code:
                rec.name = rec.brand + ' - ' + rec.default_code + ' - ' + rec.long_default_code
            elif rec.brand and rec.default_code and not rec.long_default_code:
                rec.name = rec.brand + ' - ' + rec.default_code
            elif rec.brand and rec.long_default_code and not rec.default_code:
                rec.name = rec.brand + ' - ' + rec.long_default_code
            elif rec.long_default_code and rec.default_code and not rec.brand:
                rec.name = rec.default_code + ' - ' + rec.long_default_code
            elif rec.brand and not rec.default_code and not rec.long_default_code:
                rec.name = rec.brand
            elif rec.default_code and not rec.brand and not rec.long_default_code:
                rec.name = rec.default_code
            elif rec.long_default_code and not rec.default_code and not rec.brand:
                rec.name = rec.long_default_code

    @api.onchange('brand')
    def _on_change_brand(self):
        if self.brand:
            self.brand = self.brand.upper()

    @api.onchange('default_code')
    def _on_change_default_code(self):
        if self.default_code:
            self.default_code = self.default_code.upper()
            self.dashless_code = self.default_code.replace("-", "")

    @api.onchange('long_default_code')
    def _on_change_long_default_code(self):
        if self.long_default_code:
            self.long_default_code = self.long_default_code.upper()

    @api.onchange('list_price')
    def http_request(self):
        """ The goal of this function is to post price update data
                    into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
                """
        url = "http://remoto.grupomi.com.mx:3000/api/odoo"
        price = self.list_price
        mlm = self.mlm
        default_code = self.default_code
        dashless_code = self.dashless_code
        payload = json.dumps({
            "change": "price",
            "value": price,
            "mlm": mlm,
            "internal": default_code,
            "dashless": dashless_code
        })
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("PUT", url, headers=headers, data=payload,
                         verify=False)


class Product(models.Model):
    _inherit = 'product.product'

    def product_url_open_pd(self):
        def google_search(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            results = soup.find_all("div", class_="g")
            for result in results:
                link = result.find("a")["href"]
                if not "webcache.googleusercontent.com" in link:
                    if marca in link:
                        return link
                    else:
                        return link

            return None

        if self.brand and self.default_code:
            marca = self.brand.lower() + '.com'
            partnum = self.default_code
            query = marca + ' ' + partnum
            result = google_search(query)
            if result:
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': result,
                }

    @api.onchange('product_tag_ids')
    def _on_change_product_tag_ids(self):
        if self.product_tag_ids:
            for rec in self.product_tag_ids:
                rec._origin.name = rec._origin.name.lower()

    @api.onchange('description_gr')
    def _on_change_description(self):
        if self.description_gr:
            self.description_sale = self.description_gr
            self.description_purchase = self.description_sale

    @api.onchange('categ_id')
    def _on_change_categ_id(self):
        if self.categ_id:
            if self.categ_id.complete_name:
                name = self.categ_id.complete_name
                match = re.search(r"(?<=Active)\s*/\s*(\w+(?:\s+\w+)*)", name)
                if match:
                    siemens = match.group(1)
                    self.brand = siemens
                else:
                    match = re.search(r"(?<=Obsoleto)\s*/\s*(\w+(?:\s+\w+)*)",
                                      name)
                    if match:
                        siemens = match.group(1)
                        self.brand = siemens
                    else:
                        self.brand = ''

    @api.onchange('brand')
    def _on_change_brand(self):
        if self.brand:
            self.brand = self.brand.upper()

    @api.onchange('default_code')
    def _on_change_default_code(self):
        if self.default_code:
            self.default_code = self.default_code.upper()
            self.dashless_code = self.default_code.replace("-", "")

    @api.onchange('long_default_code')
    def _on_change_long_default_code(self):
        if self.long_default_code:
            self.long_default_code = self.long_default_code.upper()

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        if name:
            products = self.env['product.product'].search(
                ['|', '|', '|', ('name', operator, name),
                                ('default_code', operator, name),
                                ('dashless_code', operator, name),
                                ('long_default_code', operator, name)],
                limit=limit).ids
            product_ids = set(products)
        else:
            products = self.env['product.product'].search([], limit=limit).ids
            product_ids = set(products)
        return product_ids

    @api.onchange('lst_price')
    def http_request(self):
        """ The goal of this function is to post price update data
                    into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
                """
        url = "http://remoto.grupomi.com.mx:3000/api/odoo"
        price = self.lst_price
        mlm = self.mlm
        default_code = self.default_code
        dashless_code = self.dashless_code
        payload = json.dumps({
            "change": "price",
            "value": price,
            "mlm": mlm,
            "internal": default_code,
            "dashless": dashless_code
        })
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("PUT", url, headers=headers, data=payload,
                         verify=False)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    related_product_ids = fields.Many2many('product.product',
                                           related='product_template_id.'
                                                   'related_product_ids',
                                           help='To show related products '
                                                'in sale order line')


class StockValuationInherit(models.Model):
    _inherit = 'stock.valuation.layer'

    @api.model_create_multi
    def create(self, vals_list):
        """ The goal of this function super is to post stock update data
            into "http://remoto.grupomi.com.mx:3000/api/odoo" this url.
        """
        for vals in vals_list:
            product_id = vals.get('product_id')
            product = self.env['product.product'].browse(product_id)
            product_tmpl = self.env['product.template'].browse(product.product_tmpl_id.id)
            url = "http://remoto.grupomi.com.mx:3000/api/odoo"
            qty_available = product.qty_available
            mlm = product_tmpl.mlm
            payload = json.dumps({
                "change": "stock",
                "value": qty_available,
                "mlm": mlm,
                "internal": product_tmpl.default_code,
                "dashless": product_tmpl.dashless_code
            })
            headers = {
                'Content-Type': 'application/json'
            }

            requests.request("PUT", url, headers=headers, data=payload,
                             verify=False)
        return super(StockValuationInherit, self).create(vals_list)
