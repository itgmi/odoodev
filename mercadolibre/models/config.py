from odoo import models, fields
import requests
import json


class Company(models.Model):
    _inherit = 'res.company'

    api_id = fields.Char('App id')
    secret_key = fields.Char()
    redirect_uri = fields.Char()
    vendor_id = fields.Char()
    access_token = fields.Char()
    refresh_token = fields.Char()
    code = fields.Char()
    response_categories = fields.Text()
    price_list_id = fields.Many2one('product.pricelist')

    def authenticate(self):
        url = 'https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=' + self.api_id + '&redirect_uri=' + self.redirect_uri
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def refresh_token_action(self):
        url = 'https://api.mercadolibre.com/oauth/token'
        headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded'
            }
        companies = self.env['res.company'].search([])
        for rec in companies:
            if rec.api_id and rec.secret_key and rec.refresh_token:
                params = {
                    "grant_type": "refresh_token",
                    "client_id": rec.api_id,
                    "client_secret": rec.secret_key,
                    "refresh_token": rec.refresh_token
                }
                response = requests.post(url, headers=headers, data=params)
                res = json.loads(response.text)
                rec.sudo().write({
                    'access_token': res.get('access_token'),
                    'refresh_token': res.get('refresh_token')
                })
                cron_job = self.env['ir.cron'].sudo().search(
                    [('name', '=', 'Refresh Token Cron Job')])
                cron_job.sudo().write({
                    'refresh_logs': response.text
                })

    def get_categories(self):
        company = self.env.company
        access_token = company.access_token
        headers = {
            'Authorization': f"Bearer {access_token}"}
        url = 'https://api.mercadolibre.com/sites/MLM/categories'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.response_categories = response.text
        else:
            self.response_categories = response.text
