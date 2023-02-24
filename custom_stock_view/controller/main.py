from odoo import http
from odoo.http import request


class Stocks(http.Controller):

    @http.route('/stock/view', auth='user', website=True)
    def stock_view(self, **post):
        """ The goal of this controller is to make stock page view
            in website.
        """
        stocks = request.env['stock.quant'].sudo().search(['|',
            ('location_id.usage', '=', 'internal'),
            ('location_id.usage', '=', 'supplier')])
        vals = []
        for rec in stocks:
            product_tmpl = request.env['product.template'].sudo().browse(
                rec.product_id.product_tmpl_id.id)
            category = request.env['product.category'].sudo().browse(
                rec.product_id.categ_id.id)
            if rec.inventory_quantity_auto_apply > 0:
                vals.append({
                    'id': rec.id,
                    'name': product_tmpl.name,
                    'category': category.name,
                    'warehouse': rec.location_id.city,
                    'available_qty': rec.inventory_quantity_auto_apply,
                })
        return http.request.render(
            'custom_stock_view.stock_page', {'stocks': vals})

    @http.route('/search/stock', auth='user', type='json',
                website=True)
    def stock_search(self, value, **kw):
        """ The goal of this controller is to make stocks search in website
                    stocks view.
        """
        stocks = request.env['stock.quant'].sudo().search(['|',
            ('location_id.usage', '=', 'internal'),
            ('location_id.usage', '=', 'supplier'),
            ('product_id.product_tmpl_id.name', 'ilike', value)])
        vals = []
        for rec in stocks:
            product_tmpl = request.env['product.template'].sudo().browse(
                rec.product_id.product_tmpl_id.id)
            category = request.env['product.category'].sudo().browse(
                rec.product_id.categ_id.id)
            if rec.inventory_quantity_auto_apply > 0:
                vals.append({
                    'id': rec.id,
                    'name': product_tmpl.name,
                    'category': category.name,
                    'warehouse': rec.location_id.city,
                    'available_qty': rec.inventory_quantity_auto_apply,
                })
        response = http.Response(template=
                                 'custom_stock_view.stock_details',
                                 qcontext={'stocks': vals})
        return response.render()

    @http.route('/selected/stock', auth='user', type='json',
                website=True)
    def selected_stock(self, selected_id, **kw):
        """ The goal of this controller is to return data to website view
                    only selected stock.
        """
        stock = request.env['stock.quant'].sudo().browse(int(selected_id))
        product_tmpl = request.env['product.template'].sudo().browse(
            stock.product_id.product_tmpl_id.id)
        category = request.env['product.category'].sudo().browse(
            stock.product_id.categ_id.id)
        vals = [{
            'name': product_tmpl.name,
            'category': category.name,
            'warehouse': stock.location_id.city,
            'available_qty': stock.inventory_quantity_auto_apply,
        }]
        response = http.Response(template=
                                 'custom_stock_view.selected_stock',
                                 qcontext={'selected': vals})
        return response.render()
