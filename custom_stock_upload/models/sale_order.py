from odoo import models, api, fields, _
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quoted_check = fields.Boolean()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    quoted_price_one = fields.Float(compute='_compute_quoted_price_one')
    quote_currency_one = fields.Char()
    quoted_price_two = fields.Float(compute='_compute_quoted_price_two')
    quote_currency_two = fields.Char()

    @api.depends('product_id')
    def _compute_quoted_price_one(self):
        for rec in self:
            rec.quoted_price_one = 0
            rec.quote_currency_one = ''
            if rec.product_id.id:
                product_id = rec.product_id.id
                quoted_orders = self.env['sale.order.line'].search([
                    ('product_id', '=', product_id)], limit=2)
                quoted_count = self.env['sale.order.line'].search_count([
                    ('product_id', '=', product_id)], limit=2)
                if int(quoted_count) >= 1:
                    if quoted_orders:
                        count = 0
                        for recs in quoted_orders:
                            if count == 0:
                                rec.quoted_price_one = recs.price_unit
                                rec.quote_currency_one = recs.currency_id.name
                            count += 1

    @api.depends('product_id')
    def _compute_quoted_price_two(self):
        for rec in self:
            rec.quoted_price_two = 0
            rec.quote_currency_two = ''
            if rec.product_id.id:
                product_id = rec.product_id.id
                quoted_orders = self.env['sale.order.line'].search([
                    ('product_id', '=', product_id)], limit=2)
                quoted_count = self.env['sale.order.line'].search_count([
                    ('product_id', '=', product_id)], limit=2)
                if int(quoted_count) == 2:
                    if quoted_orders:
                        count = 0
                        for recs in quoted_orders:
                            if count == 1:
                                rec.quoted_price_two = recs.price_unit
                                rec.quote_currency_two = recs.currency_id.name
                            count += 1

    @api.onchange('product_id')
    def _onchange_order_line(self):
        today = fields.Datetime.today()
        datetime_min = today + relativedelta(hours=00, minutes=00, seconds=00)
        datetime_max = today + relativedelta(hours=23, minutes=59, seconds=59)
        if self.product_id.id:
            product_id = self.product_id.id
            quoted_orders = self.env['sale.order.line'].search([
                ('product_id', '=', product_id),
                ('create_date', '>=', datetime_min),
                ('create_date', '<=', datetime_max)], limit=2)
            quoted_count = self.env['sale.order.line'].search_count([
                ('product_id', '=', product_id),
                ('create_date', '>=', datetime_min),
                ('create_date', '<=', datetime_max)], limit=2)
            if int(quoted_count) == 2:
                if quoted_orders:
                    count = 0
                    for rec in quoted_orders:
                        if count == 0:
                            date = rec.create_date
                            date_ = date.strftime('%Y-%m-%d %H:%M:%S')
                            quote_price_one = rec.price_unit,
                            quote_sale_one = rec.salesman_id.name,
                            quote_currency_one = rec.currency_id.name,
                            quote_customer_one = rec.order_partner_id.name,
                            quote_time_one = date_,
                        else:
                            date = rec.create_date
                            date_ = date.strftime('%Y-%m-%d %H:%M:%S')
                            quote_price_two = rec.price_unit,
                            quote_sale_two = rec.salesman_id.name,
                            quote_currency_two = rec.currency_id.name,
                            quote_customer_two = rec.order_partner_id.name,
                            quote_time_two = date_,
                        count += 1
                    message = _('Price   :   ') + str(quote_price_one[0]) \
                              + ' ' + str(quote_currency_one[0]) + \
                              _('        Sales Person   :   ') + \
                              str(quote_sale_one[0]) + \
                              _('        Customer   :   ') + \
                              str(quote_customer_one[0]) + \
                              _('      Date Time   :   ') + \
                              quote_time_one[0] + '\n' + \
                              _('Price   :   ') + str(quote_price_two[0]) \
                              + ' ' + str(quote_currency_two[0]) +  \
                              _('        Sales Person   :   ') + \
                              str(quote_sale_two[0]) +  \
                              _('        Customer   :   ') + \
                              str(quote_customer_two[0]) + \
                              _('      Date Time   :   ') + \
                              quote_time_two[0]
                    if rec.product_id.product_tmpl_id.prices_warning:
                        return {'warning': {'title': _('Quoted Prices'),
                                            'message': message}}
            elif int(quoted_count) == 1:
                if quoted_orders:
                    for rec in quoted_orders:
                        date = rec.create_date
                        date_ = date.strftime('%Y-%m-%d %H:%M:%S')
                        quote_price_one = rec.price_unit,
                        quote_sale_one = rec.salesman_id.name,
                        quote_currency_one = rec.currency_id.name,
                        quote_customer_one = rec.order_partner_id.name,
                        quote_time_one = date_,
                    message = _('Price   :   ') + str(quote_price_one[0]) \
                              + ' ' + str(quote_currency_one[0]) + \
                              _('      Sales Person   :   ') + \
                              str(quote_sale_one[0]) + \
                              _('      Customer   :   ') + \
                              str(quote_customer_one[0]) + \
                              _('      Date Time   :   ') + \
                              quote_time_one[0]
                    if rec.product_id.product_tmpl_id.prices_warning:
                        return {'warning': {'title': _('Quoted Prices'),
                                            'message': message}}
