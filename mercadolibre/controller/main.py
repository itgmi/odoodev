from odoo import http
from odoo.http import request
from mercadolibre.client import Client


class CallBack(http.Controller):
    @http.route(['/mali_login'], type='http', auth="user",
                methods=['GET'], website=True)
    def call_back(self, **codes):
        company = request.env.company
        company.sudo().write({
            'code': codes.get('code')
        })
        client = Client(company.api_id, company.secret_key, site='MCO')
        token = client.exchange_code(company.redirect_uri, company.code)
        company.sudo().write({
            'access_token': token.get('access_token'),
            'refresh_token': token.get('refresh_token')
        })
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return request.redirect(base_url)

