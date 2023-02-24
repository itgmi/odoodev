from odoo import models, fields, api
import json
from Crypto.Cipher import AES
from zeep import Client
import datetime
import ast


class ConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char('SDIN Url', config_parameter='custom_sdin.url')
    customer_nymber_SAP = fields.Char('Customer Nymber SAP',
                                      config_parameter=
                                      'custom_sdin.customer_nymber_SAP')
    encryption_key = fields.Char('Encryption Key',
                                 config_parameter='custom_sdin.encryption_key')
    iv = fields.Char('IV', config_parameter='custom_sdin.iv')
    category = fields.Many2one('product.public.category',
                               config_parameter='custom_sdin.category')
    frequency = fields.Integer('Frequency',
                               config_parameter='custom_sdin.frequency')
    store_location = fields.Char("Store Location",
                                 config_parameter='custom_sdin.store_location')
    store_name = fields.Char("Store Name",
                             config_parameter='custom_sdin.store_name')

    def sdin_post(self):
        sdin_url = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.url')
        customer_nymber_SAP = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.customer_nymber_SAP')
        encryption_key = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.encryption_key')
        iv = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.iv')
        category = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.category')
        store_location = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.store_location')
        store_name = self.env[
            'ir.config_parameter'].sudo().get_param(
            'custom_sdin.store_name')
        val = []
        res = []
        if sdin_url and customer_nymber_SAP and encryption_key and iv and category and store_location and store_name:
            stocks = self.env['stock.quant'].sudo().search([
                ('location_id.usage', '=', 'internal')])
            for rec in stocks:
                product_tmpl = self.env['product.template'].sudo().browse(
                    rec.product_id.product_tmpl_id.id)
                if int(category) in product_tmpl.public_categ_ids.ids:
                    val.append({
                        'CustomerNumberSAP': customer_nymber_SAP,
                        'ProductoId': product_tmpl.default_code,
                        'PartNumber': product_tmpl.default_code,
                        'NetExistence': rec.inventory_quantity_auto_apply,
                        'DateExtraction': datetime.date.today().strftime('%Y-%m-%d'),
                        'StoreLocation': store_location,
                        'StoreName': store_name,
                    })
            count = 0
            for rec in stocks:
                product_tmpl = self.env['product.template'].sudo().browse(
                    rec.product_id.product_tmpl_id.id)
                if int(category) in product_tmpl.public_categ_ids.ids and \
                        count < 5:
                    count += 1
                    res.append({
                        'CustomerNumberSAP': customer_nymber_SAP,
                        'ProductoId': product_tmpl.default_code,
                        'PartNumber': product_tmpl.default_code,
                        'NetExistence': rec.inventory_quantity_auto_apply,
                        'DateExtraction': datetime.date.today().strftime('%Y-%m-%d'),
                        'StoreLocation': store_location,
                        'StoreName': store_name,
                    })
            val = json.dumps(val).encode('utf-8')
            ENC_KEY = bytes(ast.literal_eval(encryption_key))
            IV = bytes(ast.literal_eval(iv))
            cipher = AES.new(ENC_KEY, AES.MODE_CBC, IV)
            length = 16 - (len(val) % 16)
            val += bytes([length]) * length
            encrypted = cipher.encrypt(val)
            url = sdin_url
            client = Client(url)
            result = client.service.RegisterPartnerInventoryT(customer_nymber_SAP,
                                                              encrypted)
            cron_job = self.env['ir.cron'].search(
                [('name', '=', 'SDIN Cron Job')])
            cron_job.write({
                'logs': result,
                'record': str(res)
            })

    @api.constrains('frequency')
    def change_interval(self):
        cron_job = self.env['ir.cron'].search([('name', '=', 'SDIN Cron Job')])
        cron_job.write({
            'interval_number': int(self.frequency)
        })
