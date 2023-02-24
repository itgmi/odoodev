from odoo import http
from odoo.http import request


class CustomRoute(http.Controller):

    @http.route('/website/<website_name>', type='http',
                auth="public", website=True)
    def website_force(self, website_name, path='/shop'):
        """ The goal of this controller is to make different route for
            multiple websites.
        """
        website = request.env['website'].sudo().search([
            ('name', '=', website_name)], limit=1)
        website._force()
        return request.redirect(path)
