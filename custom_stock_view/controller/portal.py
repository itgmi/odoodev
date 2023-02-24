from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class StockWebsite(http.Controller):

    @http.route('/Stocks', auth='user', type='http', website=True)
    def stocks_website(self, **kw):
        """ The goal of this controller is to make stocks view in customer
            portal view.
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
            url = '/Stocks/' + str(rec.id)
            if rec.inventory_quantity_auto_apply > 0:
                vals.append({
                    'url': url,
                    'name': product_tmpl.name,
                    'category': category.name,
                    'warehouse': rec.location_id.city,
                    'available_qty': rec.inventory_quantity_auto_apply,
                })
        return http.request.render('custom_stock_view.portal_stocks',
                                   {'records': vals,
                                    'page_name': 'stocks_view'})

    @http.route('/Stocks/<int:current_id>', auth='user', website=True)
    def single_view_stock(self, current_id):
        """ The goal of this controller is to make selected stock view in
            customer portal view.
            """
        stock = request.env['stock.quant'].sudo().browse(int(current_id))
        product_tmpl = request.env['product.template'].sudo().browse(
            stock.product_id.product_tmpl_id.id)
        category = request.env['product.category'].sudo().browse(
            stock.product_id.categ_id.id)
        product = [{
            'image': product_tmpl.image_1920,
        }]
        return http.request.render('custom_stock_view.portal_single_stocks',
                                   {'page_name': 'stocks_single_view',
                                    'name': product_tmpl.name,
                                    'location':
                                        stock.location_id.city,
                                    'Quantity':
                                        stock.inventory_quantity_auto_apply,
                                    'category': category.name,
                                    'mlm': product_tmpl.mlm,
                                    'dashless': product_tmpl.dashless_code,
                                    'product': product,
                                    })

    @http.route('/search/portal/stock', auth='user', type='json',
                website=True)
    def stock_portal_search(self, value, **kw):
        """ The goal of this controller is to render stocks search data
            into stocks view in portal.
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
            url = '/Stocks/' + str(rec.id)
            if rec.inventory_quantity_auto_apply > 0:
                vals.append({
                    'url': url,
                    'name': product_tmpl.name,
                    'category': category.name,
                    'warehouse': rec.location_id.city,
                    'available_qty': rec.inventory_quantity_auto_apply,
                })
        response = http.Response(template=
                                 'custom_stock_view.portal_search_stock',
                                 qcontext={'records': vals})
        return response.render()


class StockVals(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """ The goal of this function super is to return the count of stocks
            portal view.
        """
        values = super(StockVals, self)._prepare_home_portal_values(counters)
        count = request.env['stock.quant'].sudo().search_count(['|',
            ('location_id.usage', '=', 'internal'),
            ('location_id.usage', '=', 'supplier'),
            ('inventory_quantity_auto_apply', '>', 0)])
        values.update({
            'stock_count': count
        })
        return values
