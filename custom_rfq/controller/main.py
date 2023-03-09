from odoo import http
from odoo.http import request
import ast


class RequestQuote(http.Controller):
    @http.route(['/request/quote'], type="json", auth="public")
    def product_return(self, **kw):
        response = kw['vals']
        vals = []
        for record in response:
            vals.append((0, 0,
                         {'product_id': int(record.get('product')),
                          'product_uom_qty': 1,
                          }))
        partner = request.env['res.partner'].sudo().search([
            ('email', '=', record.get('email'))])
        price_list = request.env['product.pricelist'].sudo().browse(
            int(record.get('price_list_id')))
        channel = request.env['channels.gr'].sudo().search([
            ('name', '=', 'Tienda en linea')])
        if channel:
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'name': record.get('name'),
                    'email': record.get('email'),
                    'phone': record.get('phone'),
                    'channel_id': channel.id,
                })
        else:
            channel = request.env['channels.gr'].sudo().create({
                'name': 'Tienda en linea',
            })
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'name': record.get('name'),
                    'email': record.get('email'),
                    'phone': record.get('phone'),
                    'channel_id': channel.id,
                })
        website = int(record.get('website'))
        quote = request.env["sale.order"].sudo().create({
            'partner_id': partner.id,
            'pricelist_id': price_list.id,
            'website_id': website,
            'order_line': vals
        })
        if quote:
            return True
        else:
            return False

    @http.route(['/request/quote/user'], type="json", auth="public")
    def product_return_user(self, **kw):
        response = kw['product']
        website = kw['website']
        partner = request.env.user.partner_id
        vals = [(0, 0,
                 {'product_id': int(response),
                  'product_uom_qty': 1,
                  })]
        quote = request.env["sale.order"].sudo().create({
            'partner_id': partner.id,
            'website_id': int(website),
            'order_line': vals
        })
        if quote:
            return True
        else:
            return False

    @http.route(['/request/quote/cart'], type="json", auth="public")
    def request_quote_cart(self, **kw):
        response = kw['vals']
        for rec in response:
            lines = ast.literal_eval(rec.get('product'))
        vals = []
        for record in lines:
            line = request.env['sale.order.line'].sudo().browse(int(record))
            vals.append((0, 0,
                         {'product_id': line.product_id.id,
                          'product_uom_qty': line.product_uom_qty,
                          }))
        for recs in response:
            partner = request.env['res.partner'].sudo().search([
                ('email', '=', recs.get('email'))])
            price_list = request.env['product.pricelist'].sudo().browse(
                int(recs.get('price_list_id')))
            channel = request.env['channels.gr'].sudo().search(
                [('name', '=', 'Tienda en linea')])
            if channel:
                if not partner:
                    partner = request.env['res.partner'].sudo().create({
                        'name': recs.get('name'),
                        'email': recs.get('email'),
                        'phone': recs.get('phone'),
                        'channel_id': channel.id,
                    })
            else:
                channel = request.env['channels.gr'].sudo().create({
                    'name': 'Tienda en linea',
                })
                if not partner:
                    partner = request.env['res.partner'].sudo().create({
                        'name': recs.get('name'),
                        'email': recs.get('email'),
                        'phone': recs.get('phone'),
                        'channel_id': channel.id,
                    })
            website = int(recs.get('website'))
        quote = request.env["sale.order"].sudo().create({
            'partner_id': partner.id,
            'pricelist_id': price_list.id,
            'website_id': website,
            'order_line': vals
        })
        if quote:
            return True
        else:
            return False

    @http.route(['/request/quote/cart/user'], type="json", auth="public")
    def request_quote_cart_user(self, **kw):
        response = kw['lines']
        website = kw['website']
        partner = request.env.user.partner_id
        lines = ast.literal_eval(response)
        vals = []
        for record in lines:
            line = request.env['sale.order.line'].sudo().browse(int(record))
            vals.append((0, 0,
                         {'product_id': line.product_id.id,
                          'product_uom_qty': line.product_uom_qty,
                          }))
        quote = request.env["sale.order"].sudo().create({
            'partner_id': partner.id,
            'website_id': int(website),
            'order_line': vals
        })
        if quote:
            return True
        else:
            return False
