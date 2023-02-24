from odoo import http
import xlrd
import base64
from odoo.http import request


class StockUpload(http.Controller):
    @http.route(['/stck/upload'], type="json", auth="user")
    def product_return(self, value, **kw):
        res = bytes(value, 'utf-8')
        book = xlrd.open_workbook(file_contents=base64.decodebytes(res))
        sheet = book.sheet_by_index(0)
        user = request.env.user
        for row in range(sheet.nrows):
            if row > 0:
                product = request.env['product.product'].sudo().search([
                    ('default_code', '=', sheet.cell_value(row, colx=0))])
                if product:
                    stock = request.env['stock.quant'].sudo().search([
                        ('location_id', '=', user.location_id.id),
                        ('product_id', '=', product.id)])
                    if stock:
                        stock.sudo().write({
                            'quantity':
                                float(sheet.cell_value(row, colx=1))
                        })
                    else:
                        request.env['stock.quant'].sudo().create({
                            'location_id': user.location_id.id,
                            'product_id': product.id,
                            'quantity':
                                float(sheet.cell_value(row, colx=1))
                        })
        return True
